// Explicit paid-service adapter. No .env file is loaded or copied by this script.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const sdk=require('microsoft-cognitiveservices-speech-sdk');
const [configPath,outArg]=process.argv.slice(2);
if(!configPath||!outArg)throw Error('Usage: node synthesize.cjs CONFIG_JSON NEW_OUTPUT_DIR');
const key=process.env.AZURE_SPEECH_KEY,region=process.env.AZURE_SPEECH_REGION;
if(!key||!region)throw Error('Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION in your environment');
const voice=process.env.AZURE_SPEECH_VOICE||'en-US-JennyNeural';
const language=process.env.AZURE_SPEECH_LANGUAGE||'en-US';
const config=JSON.parse(fs.readFileSync(configPath,'utf8')),out=path.resolve(outArg);
if(fs.existsSync(out))throw Error('Refusing to overwrite '+out);
if(typeof config.narration!=='string'||!config.narration.trim())throw Error('config.narration is required');
const escape=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
async function main(){
 const settings=sdk.SpeechConfig.fromSubscription(key,region);settings.speechSynthesisVoiceName=voice;
 settings.speechSynthesisOutputFormat=sdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm;
 settings.setProperty(sdk.PropertyId.SpeechServiceResponse_RequestWordBoundary,'true');
 const synthesizer=new sdk.SpeechSynthesizer(settings,null),words=[];
 synthesizer.wordBoundary=(_,e)=>{if(/[\p{L}\p{N}]/u.test(e.text))words.push({word:e.text,startTime:e.audioOffset/1e7,endTime:(e.audioOffset+e.duration)/1e7});};
 try{
  const ssml=`<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="${escape(language)}"><voice name="${escape(voice)}">${escape(config.narration)}</voice></speak>`;
  const result=await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('Speech timed out after 90 seconds')),90000);synthesizer.speakSsmlAsync(ssml,r=>{clearTimeout(timer);resolve(r);},e=>{clearTimeout(timer);reject(Error(String(e)));});});
  if(result.reason!==sdk.ResultReason.SynthesizingAudioCompleted)throw Error(result.errorDetails||'Speech did not complete');
  const audio=Buffer.from(result.audioData);
  if(audio.toString('ascii',0,4)!=='RIFF'||!words.length)throw Error('Missing real WAV or native word boundaries');
  fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'speech.wav'),audio);
  const manifest={provider:'azure-speech',voice,language,text:config.narration,audio:'speech.wav',audio_sha256:crypto.createHash('sha256').update(audio).digest('hex'),timing_source:'native_word_boundaries',words};
  fs.writeFileSync(path.join(out,'speech.json'),JSON.stringify(manifest,null,2));
  console.log(JSON.stringify({manifest:path.join(out,'speech.json'),word_boundaries:words.length,voice,audio_sha256:manifest.audio_sha256}));
 }finally{synthesizer.close();}
}
main().catch(e=>{console.error(String(e.message).split(key).join('[REDACTED]'));process.exitCode=1;});
