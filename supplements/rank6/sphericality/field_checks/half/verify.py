"""Recompute both exact searches to trace one million."""
from half24 import run as run24
from half16 import run as run16
from screen import process
for c,run,expected,num in [(24,run24,[3,1,0,0],2615),(16,run16,[1,1,0,0],1031)]:
    candidates=run(1_000_000)
    tally,remaining=process(candidates,c)
    assert len(candidates)==num and tally==expected and not remaining
    print('conductor',c,'minimum, moments, Fourier',*tally[:3],flush=True)
