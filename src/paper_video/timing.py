"""Native cue binding. Do not estimate spoken timing from character counts."""
import hashlib,json,re,wave
from pathlib import Path

def normalize(text):return ''.join(c.casefold() for c in text if c.isalnum())

def bind_native(config,manifest,root):
    data=json.loads(Path(manifest).read_text(encoding='utf-8'))
    audio=(Path(manifest).parent/data['audio']).resolve()
    if hashlib.sha256(audio.read_bytes()).hexdigest()!=data['audio_sha256']:raise ValueError('Audio hash mismatch')
    if normalize(config['narration'])!=normalize(data['text']):raise ValueError('Narration differs from speech text')
    with wave.open(str(audio),'rb') as f:
        duration=f.getnframes()/f.getframerate()
        if f.getsampwidth()!=2 or f.getnchannels()!=1:raise ValueError('Expected mono 16-bit PCM WAV')
    words=data['words'];native=normalize(''.join(w['word'] for w in words))
    if native!=normalize(data['text']):raise ValueError('Native word coverage mismatch')
    chars=[];last=-1
    for w in words:
        start,end=float(w['startTime']),float(w['endTime'])
        if not (0<=start<=end<=duration+.25 and start>=last):raise ValueError('Invalid native boundary')
        last=start;chars.extend([(start,min(duration,end))]*len(normalize(w['word'])))
    result=json.loads(json.dumps(config));result['duration']=duration+1.0
    result['timing_source']='native_word_boundaries';result['audio']=str(audio)
    result['audio_sha256']=data['audio_sha256']
    for mark in result['marks']:
        phrase=normalize(mark['cue_phrase']);i=native.find(phrase)
        if i<0:raise ValueError('Cue not present in native speech: '+mark['cue_phrase'])
        mark['cue']=chars[i][0]
    captions=[];cursor=0
    for sentence in re.split(r'(?<=[.!?。！？])\s*',data['text']):
        phrase=normalize(sentence)
        if not phrase:continue
        i=native.find(phrase,cursor)
        if i<0:raise ValueError('Caption/native mismatch')
        captions.append({'text':sentence,'start':chars[i][0],'end':chars[i+len(phrase)-1][1]});cursor=i+len(phrase)
    result['captions']=captions
    return result
