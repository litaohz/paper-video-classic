"""Classic flat-paper compositor, adapted from the retired source-first pipeline."""
from pathlib import Path
import bisect,hashlib,json,math,shutil,subprocess
from functools import lru_cache
from PIL import Image,ImageDraw,ImageFont
from .grounding import ground,render_region,sha256
INK='#151515';PAPER='#fffef7';TEAL='#00635d';RED=(216,41,51);PINK='#f8cdf0';MINT='#c8f0df'
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def partial(points,f):
    budget=sum(math.dist(a,b) for a,b in zip(points,points[1:]))*max(0,min(1,f));out=[points[0]]
    for a,b in zip(points,points[1:]):
        n=math.dist(a,b)
        if budget>=n:out.append(b);budget-=n
        else:
            if n:out.append(tuple(a[i]+(b[i]-a[i])*budget/n for i in (0,1)))
            break
    return out
class Film:
    def __init__(self,config,root,font_path=None):
        self.config=config;self.root=Path(root);self.W=config.get('width',1920);self.H=config.get('height',1080)
        if (self.W,self.H)!=(1920,1080):raise ValueError('This classic layout currently supports 1920x1080')
        self.fps=config.get('fps',24);self.duration=float(config['duration']);self.font_path=font_path
        if self.duration<=0 or self.fps<=0:raise ValueError('Positive duration and fps required')
        self.marks=ground(config,self.root);self.marks.sort(key=lambda m:m['cue']);self.starts=[m['cue'] for m in self.marks]
        if not self.marks:raise ValueError('At least one grounded highlight is required')
        if any(not 0<=c<self.duration for c in self.starts):raise ValueError('Cue outside duration')
        self.source=render_region(self.root/config['pdf'],config['page'],config['crop'],scale=2.4)
        scale=min(1000/self.source.width,667/self.source.height)
        self.image=self.source.resize((round(self.source.width*scale),round(self.source.height*scale)),Image.Resampling.LANCZOS)
        self.x=70+(1000-self.image.width)/2;self.y=228+(667-self.image.height)/2
        crop=config['crop'];self.scale=self.image.width/(crop[2]-crop[0])
    @lru_cache(maxsize=100)
    def font(self,size):
        return ImageFont.truetype(self.font_path,size) if self.font_path else ImageFont.load_default(size=size)
    def text(self,draw,xy,text,size=32,color=INK,maxw=None):
        while maxw and draw.textlength(text,font=self.font(size))>maxw and size>15:size-=1
        draw.text(xy,text,font=self.font(size),fill=color)
    def wrapped(self,draw,text,width,size):
        lines=[];line=''
        for word in text.split():
            cand=(line+' '+word).strip()
            if draw.textlength(cand,font=self.font(size))>width and line:lines.append(line);line=word
            else:line=cand
        if line:lines.append(line)
        return lines
    def card(self,d,rect,fill=PAPER,shadow=True):
        if shadow:d.rounded_rectangle(tuple(v+8 for v in rect),radius=12,fill=INK)
        d.rounded_rectangle(rect,radius=12,fill=fill,outline=INK,width=3)
    def point(self,x,y):
        crop=self.config['crop'];return(self.x+(x-crop[0])*self.scale,self.y+(y-crop[1])*self.scale)
    def frame(self,t,annotations=True):
        im=Image.new('RGB',(self.W,self.H),PAPER);d=ImageDraw.Draw(im)
        d.rectangle((0,0,self.W,139),fill=PINK);d.line((0,139,self.W,139),fill=INK,width=3)
        self.text(d,(64,37),self.config['title'],48,maxw=1780)
        self.text(d,(70,167),self.config['source_label'],27,TEAL)
        x,y=self.x,self.y;w,h=self.image.size
        d.rectangle((x+8,y+8,x+w+8,y+h+8),fill=INK);im.paste(self.image,(round(x),round(y)));d.rectangle((x-2,y-2,x+w+2,y+h+2),outline=INK,width=3)
        idx=bisect.bisect_right(self.starts,t)-1
        if idx>=0:
            m=self.marks[idx];age=t-m['cue'];nextcue=self.starts[idx+1] if idx+1<len(self.starts) else self.duration
            end=min(nextcue,self.duration);p=max(0,min(1,age/1.1))
            if annotations:
                for j,r in enumerate(m['line_boxes']):
                    pts=partial([self.point(r[0],r[3]+1),self.point(r[2],r[3]+1)],p*len(m['line_boxes'])-j)
                    if len(pts)>1:d.line(pts,fill=RED,width=4)
                if age<1.5:
                    r=m['line_boxes'][0];px,py=self.point(r[0],r[3]+7);d.ellipse((px-4,py-4,px+4,py+4),fill=TEAL)
            opened=ease((age-.7)/.65)*(1-ease((t-(end-.65))/.6))
            if opened>0:
                px,py,pw,ph=1140,286,696,544;aw=round(pw*opened);ah=round(ph*opened)
                r=m['line_boxes'][0];sx,sy=self.point(r[2],(r[1]+r[3])/2)
                d.line([(x+w+6,sy),(1100,sy),(1100,py+ph/2),(px,py+ph/2)],fill=TEAL,width=3)
                self.card(d,(px,py,px+aw,py+ah),MINT)
                if opened>.99:
                    self.text(d,(px+27,py+30),m['note_title'],38,TEAL,maxw=pw-54)
                    for k,line in enumerate(self.wrapped(d,m['note'],pw-58,28)):
                        self.text(d,(px+29,py+103+k*40),line,28)
                    for k,label in enumerate(m['nodes']):
                        yy=py+230+k*82;appear=ease((age-1.5-k*.45)/.4)
                        if appear>0:
                            xx=px+40+20*(1-appear);self.card(d,(xx,yy,xx+pw-88,yy+54),PAPER,False)
                            self.text(d,(xx+17,yy+10),label,27,TEAL,maxw=pw-128)
                            if k:self.text(d,(px+pw/2-10,yy-29),'v',22,TEAL)
                    self.text(d,(px+22,py+ph+20),'Teaching explanation - not a source figure',20,TEAL,maxw=pw)
            caps=self.config.get('captions')
            caption=next((c['text'] for c in caps if c['start']<=t<c['end']),'') if caps else m['caption']
            if caption:
                size=37;lines=self.wrapped(d,caption,1710,size)
                if len(lines)>2:
                    size=30;lines=self.wrapped(d,caption,1710,size)
                if len(lines)>2:raise ValueError('Caption too long: split at native boundaries')
                top=971 if len(lines)==1 else 957
                self.card(d,(70,top-8,1850,1060),PAPER,False)
                for j,line in enumerate(lines):
                    length=d.textlength(line,font=self.font(size));self.text(d,((1920-length)/2,top+j*(size+5)),line,size,TEAL)
        return im

def render(config_path,out,font=None,native=None):
    config_path=Path(config_path);config=json.loads(config_path.read_text(encoding='utf-8'));root=config_path.parent
    if native:
        from .timing import bind_native
        config=bind_native(config,native,root)
    if config.get('timing_source')!='authored_silent_demo' and not native:
        raise ValueError('Narrated projects require --native manifest, not estimated speech timing')
    out=Path(out)
    if out.exists():raise FileExistsError(f'Refusing to overwrite {out}')
    for tool in ('ffmpeg','ffprobe'):
        if not shutil.which(tool):raise RuntimeError(f'{tool} must be installed and on PATH')
    out.mkdir(parents=True)
    film=Film(config,root,font);frames=math.ceil(film.duration*film.fps);duration=frames/film.fps
    # Prove that sample frames do not depend on previous renders.
    probes=[0.,min(3.,film.duration/3),film.duration*.6];hashes={t:hashlib.sha256(film.frame(t).tobytes()).hexdigest() for t in probes}
    for t in reversed(probes):
        if hashlib.sha256(film.frame(t).tobytes()).hexdigest()!=hashes[t]:raise AssertionError('Non-deterministic renderer')
    (out/'grounding.json').write_text(json.dumps(film.marks,indent=2),encoding='utf-8')
    public_timeline={k:v for k,v in config.items() if k!='audio'}
    (out/'timeline.json').write_text(json.dumps(public_timeline,indent=2),encoding='utf-8')
    video=out/'video.mp4';args=['ffmpeg','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r',str(film.fps),'-i','pipe:0']
    if config.get('audio'):args+=['-i',config['audio'],'-map','0:v:0','-map','1:a:0','-af','apad','-c:a','aac','-b:a','128k']
    else:args+=['-an']
    args+=['-frames:v',str(frames),'-t',str(duration),'-c:v','libx264','-threads','4','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
    with (out/'encode.log').open('wb') as log:
        proc=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=log)
        try:
            for n in range(frames):proc.stdin.write(film.frame(n/film.fps).tobytes())
            proc.stdin.close();code=proc.wait()
            if code:raise RuntimeError(f'FFmpeg failed; inspect {out/"encode.log"}')
        except BaseException:
            proc.kill();proc.wait();raise
    decode=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],capture_output=True)
    (out/'decode.log').write_bytes(decode.stderr)
    if decode.returncode or decode.stderr:raise RuntimeError('Full decode failed')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert v['width']==1920 and v['height']==1080 and int(v['nb_frames'])==frames
    marks=[]
    for m in film.marks:
        t=min(m['cue']+1.3,film.duration-1/film.fps);fn=f'mark-{m["id"]}.png'
        subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(out/fn)],check=True)
        marks.append({'id':m['id'],'time':t,'encoded_frame':fn})
    for t,label in [(min(film.duration-1,film.starts[0]+4),'preview'),(min(film.duration-1,film.starts[-1]+3),'end')]:film.frame(t).save(out/f'{label}.png')
    report={'status':'PASS','scope':'Source search/crop, deterministic sample frames, dimensions/frame count and full media decode. No aesthetic or scientific-review claim.',
      'frames':frames,'fps':film.fps,'duration':duration,'width':1920,'height':1080,
      'video_sha256':sha256(video),'pdf_sha256':sha256(root/config['pdf']),'config_sha256':sha256(config_path),
      'timing_source':config['timing_source'],'audio_present':bool(config.get('audio')),
      'marks':marks,'grounding_count':len(film.marks),'aesthetic_review':'NOT_CHECKED','probe':probe}
    (out/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return {k:report[k] for k in ['status','frames','fps','duration','video_sha256','timing_source','audio_present']}
