"""Generate our own clearly-labelled fixture; no third-party paper is bundled."""
from pathlib import Path
import json

TEXT=[
 (48,742,21,'Evidence-first paper explanations'),
 (48,713,11,'Paper Video Classic - runnable demonstration source'),
 (48,685,10,'This is a demo fixture, not a published research paper or benchmark.'),
 (48,640,16,'1. Keep the paper in view'),
 (48,611,12,'Show the original passage at a readable size.'),
 (48,591,12,'Keep its colors, wording and surrounding context unchanged.'),
 (48,538,16,'2. Tie visual cues to spoken words'),
 (48,509,12,'Use actual speech boundaries when narration is present.'),
 (48,489,12,'A silent preview may use explicitly authored editorial timing.'),
 (48,436,16,'3. Separate evidence from explanation'),
 (48,407,12,'A teaching panel can explain a relationship beside the source.'),
 (48,387,12,'The panel is editorial; it is not an original figure or a measured result.'),
 (48,332,12,'Source location  ->  quote boxes  ->  speech cue  ->  rendered frame'),
 (48,275,10,'No scientific results are reported in this fixture.'),
 (48,255,10,'Written for this open-source example by Thomas Li.'),
]

def make_pdf(path):
    def esc(s): return s.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
    commands=['1 1 1 rg 0 0 612 792 re f','0.08 0.10 0.12 rg']
    for x,y,size,text in TEXT:
        commands.append(f'BT /F1 {size} Tf {x} {y} Td ({esc(text)}) Tj ET')
    stream='\n'.join(commands).encode('ascii')
    objects=[b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
             b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
             b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',b'<< /Length '+str(len(stream)).encode()+b' >>\nstream\n'+stream+b'\nendstream']
    result=bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n');offsets=[0]
    for i,obj in enumerate(objects,1):
        offsets.append(len(result));result.extend(f'{i} 0 obj\n'.encode()+obj+b'\nendobj\n')
    xref=len(result);result.extend(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]:result.extend(f'{offset:010d} 00000 n \n'.encode())
    result.extend(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    Path(path).write_bytes(result)

NARRATION=('Keep the paper in view. The original document remains readable while the explanation unfolds beside it. '
'Tie visual cues to spoken words. A highlight starts at a native speech boundary, not at an estimated reading speed. '
'Separate evidence from explanation. The teaching panel is ours; the source text stays unchanged.')

CONFIG={
 'title':'Explain the idea. Keep the evidence.', 'source_label':'Demo source / page 1',
 'pdf':'source.pdf','page':1,'crop':[35,35,580,465],
 'duration':24,'fps':24,'width':1920,'height':1080,
 'timing_source':'authored_silent_demo','narration':NARRATION,
 'marks':[
  {'id':'source','quote':'Keep the paper in view','cue':2.0,'cue_phrase':'Keep the paper in view','caption':'Start with the original passage, not a replacement slide.',
   'note_title':'Read the source','note':'The paper remains visible and readable.','nodes':['Original PDF','Exact quote','Explanation']},
  {'id':'timing','quote':'Tie visual cues to spoken words','cue':9.0,'cue_phrase':'Tie visual cues to spoken words','caption':'Bind highlights to real speech timing when narration is present.',
   'note_title':'One shared clock','note':'Speech, captions and annotations use the same cues.','nodes':['Audio','Word boundary','Visual cue']},
  {'id':'boundary','quote':'Separate evidence from explanation','cue':16.0,'cue_phrase':'Separate evidence from explanation','caption':'Keep editorial teaching layers distinct from source evidence.',
   'note_title':'Evidence and teaching','note':'A source-linked panel explains; it does not replace the paper.','nodes':['Source evidence','Teaching panel','Return to source']}
 ]}

def create_fixture(out):
    out=Path(out)
    if out.exists():raise FileExistsError(f'Refusing to overwrite {out}')
    out.mkdir(parents=True)
    make_pdf(out/'source.pdf')
    (out/'config.json').write_text(json.dumps(CONFIG,indent=2),encoding='utf-8')
    return out/'config.json'
