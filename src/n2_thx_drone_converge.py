'''
no. 2
 * Attempt at recreating the THX sound effect
 * Not very close, but good practice
'''

from bitnoise.core import *
from bitnoise.filter import Filter
from bitnoise.oscillator import Oscillator

TITLE = "n2_thx_drone_converge"
NUM_OSCS = 15
NUM_SECONDS = 13
NUM_SAMPLES = NUM_SECONDS * SAMPLE_RATE

note = scale(['D1'])[0]
oscs = []
filter1 = Filter()
out = []

for i in range(NUM_OSCS):
	oscs.append(Oscillator(saw))
	oscs[i].set_hz(100.0 + random.random() * 700.0)

for t in range(NUM_SAMPLES):
	sample = 0.0

	for i in range(NUM_OSCS):
		sample += oscs[i].get_sample(t)
		oscs[i].set_hz(oscs[i].hz + (note - oscs[i].hz)*0.000018)
	
	sample *= (1.0 / float(NUM_OSCS))
	sample = filter1.filter_sample(sample, 0.25, 0.0)
	out.append(sample)


r_amt = 0.8
rout = reverb(out)
out = [mixer(rout[i],out[i], r_amt) for i in range(len(out))]

# write output to WAV
write_buffer_to_wav(out, RENDER_PATH+TITLE+".wav")