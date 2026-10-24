"""Regression controls for exact classification flags, not display rounding."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_ring_properties import derive,perron_integrality
class ExactProperties(unittest.TestCase):
 def test_fibonacci(self):
  p=derive([[[1,0],[0,1]],[[0,1],[1,1]]])['properties']
  self.assertTrue(p['simple']and p['perfect']and p['self_dual']and p['multiplicity_free'])
  self.assertFalse(p['integral']or p['weakly_integral']or p['pointed'])
 def test_ising_and_rep_s3(self):
  tensor=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,0],[0,0,1]],[[0,0,1],[0,0,1],[1,1,0]]]
  p=derive(tensor)['properties'];self.assertTrue(p['weakly_integral']);self.assertFalse(p['integral']or p['perfect']or p['simple'])
  tensor[2][2][2]=1;p=derive(tensor)['properties'];self.assertTrue(p['integral']and p['weakly_integral'])
 def test_pointed_prime_group(self):
  tensor=[[[int(k==(i+j)%3)for k in range(3)]for j in range(3)]for i in range(3)]
  p=derive(tensor)['properties'];self.assertTrue(p['simple']and p['pointed']and p['integral']);self.assertFalse(p['perfect']or p['self_dual'])
 def test_largest_real_root_not_integer_eigenvalue(self):
  # (t-1)(t^2-t-1): the integer eigenvalue 1 must not imply integral PF dimension.
  self.assertFalse(perron_integrality((1,-2,0,1))['integer'])
 def test_rational_is_not_integer(self):
  self.assertFalse(perron_integrality((2,-3))['integer'])
if __name__=='__main__':unittest.main()
