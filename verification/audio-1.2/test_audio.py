import importlib.util,unittest,math
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'plugins/motion-director/skills/motion-director/scripts/mix_audio.py'
spec=importlib.util.spec_from_file_location('mix',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TimingTests(unittest.TestCase):
 def test_anchor_at_contact(self):
  self.assertEqual(m.cue_start(60,60,.125,48000),42000)
  self.assertEqual(m.cue_start(0,60,.125,48000),-6000)
 def test_noninteger_frame_time(self):
  self.assertEqual(m.cue_start(1000,29.97,0,48000),round(1000*48000/29.97))
 def test_db_gain(self):
  self.assertAlmostEqual(m.db_gain(-6.020599913),.5,places=8)
 def test_duck_attack_hold_release(self):
  d=[{'start_frame':60,'end_frame':120,'gain_db':-12,'attack_seconds':.1,'release_seconds':.2}]
  self.assertEqual(m.duck_gain(.8,d,60),1)
  self.assertAlmostEqual(m.duck_gain(1.5,d,60),m.db_gain(-12))
  self.assertEqual(m.duck_gain(2.3,d,60),1)
  self.assertGreater(m.duck_gain(2.1,d,60),m.db_gain(-12))
 def test_overlapping_ducks_do_not_multiply(self):
  d={'start_frame':60,'end_frame':120,'gain_db':-12}
  self.assertAlmostEqual(m.duck_gain(1.5,[d,d],60),m.db_gain(-12))
 def test_fades_at_edges(self):
  self.assertEqual(m.fade_gain(0,48000,480,480),0)
  self.assertEqual(m.fade_gain(47999,48000,480,480),0)
  self.assertEqual(m.fade_gain(24000,48000,480,480),1)
 def test_manifest_rejects_invalid_inputs(self):
  for bad in [0,-1,float('nan')]:
   with self.assertRaises(ValueError):m.validate({'fps':bad,'duration_seconds':8,'cues':[]})
  with self.assertRaises(ValueError):m.validate({'fps':60,'duration_seconds':8,'cues':[{'file':'a.wav','event_frame':480,'gain_db':0}]})
if __name__=='__main__':unittest.main()
