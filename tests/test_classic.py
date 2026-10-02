import hashlib,importlib,json,tempfile,unittest,wave
from pathlib import Path
from paper_video.demo import create_fixture,CONFIG
from paper_video.grounding import quote_boxes,ground
from paper_video.render import Film
from paper_video.timing import bind_native

class ClassicTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.config=create_fixture(self.root/'fixture');self.cfg=json.loads(self.config.read_text());self.base=self.config.parent
 def tearDown(self):self.tmp.cleanup()
 def test_exact_quote_and_bounds(self):
  hits=ground(self.cfg,self.base);self.assertEqual(len(hits),3)
  for h in hits:self.assertTrue(h['line_boxes']);self.assertEqual(h['page'],1)
 def test_missing_quote_is_error(self):
  with self.assertRaisesRegex(ValueError,'Quote not found'):quote_boxes(self.base/'source.pdf',1,'This sentence is not present')
 def test_repeated_quote_is_error(self):
  with self.assertRaisesRegex(ValueError,'Ambiguous quote'):quote_boxes(self.base/'source.pdf',1,'source')
 def test_outside_crop_is_error(self):
  self.cfg['crop']=[0,0,100,100]
  with self.assertRaisesRegex(ValueError,'outside crop'):ground(self.cfg,self.base)
 def test_seek_order(self):
  film=Film(self.cfg,self.base);times=[3.1,10.2,18.4,0]
  a={t:hashlib.sha256(film.frame(t).tobytes()).hexdigest() for t in times}
  for t in reversed(times):self.assertEqual(a[t],hashlib.sha256(film.frame(t).tobytes()).hexdigest())
 def test_underlines_add_visible_red_pixels(self):
  film=Film(self.cfg,self.base)
  for mark in film.marks:
   def count(img):
    return sum(r>150 and r>g*1.5 and r>b*1.35 for r,g,b in img.crop((65,220,1080,910)).getdata())
   t=mark['cue']+1.3
   self.assertGreater(count(film.frame(t)),count(film.frame(t,annotations=False))+20)
 def test_refuse_fixture_overwrite(self):
  with self.assertRaises(FileExistsError):create_fixture(self.base)
 def test_native_audio_hash_mismatch_rejected(self):
  # Explicit synthetic UNIT TEST data, never claimed as service output.
  with wave.open(str(self.base/'test.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE','not compressed'));f.writeframes(bytes(48000))
  manifest={'audio':'test.wav','audio_sha256':'0'*64,'text':self.cfg['narration'],'words':[]}
  p=self.base/'test.json';p.write_text(json.dumps(manifest))
  with self.assertRaisesRegex(ValueError,'hash mismatch'):bind_native(self.cfg,p,self.base)
 def test_no_private_or_machine_paths_in_config(self):
  raw=json.dumps(CONFIG)
  self.assertNotIn('C:/',raw);self.assertNotIn('Q:/',raw);self.assertNotIn('api_key',raw.lower())

if __name__=='__main__':unittest.main()
