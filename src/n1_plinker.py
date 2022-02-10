'''
no. 1
 * The code is a mess and the output doesn't sound great
 * Just a proof-of-concept
'''

from bitnoise.core import *
from bitnoise.filter import Filter
from bitnoise.oscillator import Oscillator

TITLE = "n1_plinker"
NUM_SECONDS = 10
NUM_SAMPLES = NUM_SECONDS * SAMPLE_RATE

# 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'

hi_scale = scale(['E4', 'D4', 'A4', 'G4', 'E3', 'D3', 'A3', 'G3'])
lo_scale = scale(['E0', 'E1'])
lo_scale[0]/=2

# audio output buffers
chord_out = []
bass_out = []

# low pass filters
filter1 = Filter()
filter2 = Filter()

# oscillators
low_osc = Oscillator(saw)
hi_osc1 = Oscillator(saw)
hi_osc2 = Oscillator(saw)
hi_osc3 = Oscillator(saw)
hi_osc = [hi_osc1, hi_osc2, hi_osc3]

# lfo
lfo = Oscillator(saw)
lfo.set_hz(5)

# noise
noise = Oscillator(rand)

# low pass filter 4 noise
fnoise = Filter()

for t in range(NUM_SAMPLES):

	# hard coded rates for notes (created before the Scheduler class)
	# -----------------------------------------------------------------
	if t % 8000 == 0:
		low_osc.set_hz(lo_scale[0])
	if t % (8000 + 1000) == 0:
		low_osc.set_hz(lo_scale[1])

	if t % 90000 == 0:
		note_len = int( random.random() * 5000 )
		for i in range(len(hi_osc)):
			hi_osc[i].set_hz(random_note(hi_scale)) 
	if t % (90000 +  note_len) == 0:
		for i in range(len(hi_osc)):
			hi_osc[i].set_hz(0.0)
	# ----------------------------------------------------------------

	bass_output = low_osc.get_sample(t)
	bass_output = apply_gain(bass_output, 1.6)
	bass_output = saturate(bass_output)
	bass_output = filter1.filter_sample(bass_output, 0.065, 0.0)

	chord_output = 0.0
	for i in range(len(hi_osc)):
		chord_output += (hi_osc[i].get_sample(t)) / float(len(hi_osc))

	chord_output = apply_gain(chord_output, 0.6)
	chord_output = mixer(fnoise.filter_sample(noise.get_sample(i), 0.3, 0.0), chord_output, 0.1)
	chord_output = apply_gain(chord_output, lfo.get_sample(t))
	chord_output = filter2.filter_sample(chord_output, 0.7, 0.0)

	bass_out.append(bass_output)
	chord_out.append(chord_output)

rev_amt = 0.8
chord_out_rev = reverb(chord_out)
chord_out = [mixer(chord_out_rev[i], chord_out[i], rev_amt) for i in range(len(chord_out))]

bass_amt = 0.4
output = [mixer(bass_out[i], chord_out[i], bass_amt) for i in range(len(chord_out))]

rev_amt = 0.5
output_rev = reverb(output)
output = [mixer(output_rev[i], output[i], rev_amt) for i in range(len(output))]

# write output to WAV
write_buffer_to_wav(output, RENDER_PATH+TITLE+".wav")
