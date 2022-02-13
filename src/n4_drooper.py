'''
no. 4
 * more scheduler
'''

from doctest import master
import sched
from bitnoise.core import *
from bitnoise.filter import Filter
from bitnoise.oscillator import Oscillator
from bitnoise.scheduler import Scheduler

TITLE = "n4_drooper"
NUM_SECONDS = 10
NUM_SAMPLES = NUM_SECONDS * SAMPLE_RATE
BPM = 100

# 3 tracks
line_out = [[0.0]*NUM_SAMPLES, [0.0]*NUM_SAMPLES, [0.0]*NUM_SAMPLES]

# Voices
voice1 = Oscillator(saw)
voice2 = Oscillator(tri)
noise1 = Oscillator(noise)

# LFOs
lfo1 = Oscillator(sq)
lfo2 = Oscillator(sq)

# Filters
voice1_filter = Filter()
voice2_filter = Filter()
voice3_filter = Filter()
noise1_filter = Filter()
master_filter = Filter()


notes = scale(['A3','B3','C3','D3','E3','F#3','G3', 'A4'])

scheduler = Scheduler(BPM, NUM_SAMPLES, SAMPLE_RATE)


class noter:
	def __init__(self):
		self.voice1NoteIndex = 0

	def note(self, t, params):
		track = params[0]
		voice = params[1]
		octave = params[2]
		note_jump = params[3]
		gain_amt = params[4]
		duration = params[5]

		note_duration = 60.0 * (1.0/BPM) * duration
		note_samples = note_duration * SAMPLE_RATE
		hz = notes[self.voice1NoteIndex]
		voice.set_hz(hz * octave)

		ramp = 0.0
		for i in range(t, int(min((t+note_samples), NUM_SAMPLES))):
			sample = voice.get_sample(i)
			sample = apply_gain(sample, ramp)
			sample = apply_gain(sample, gain_amt)
			sample = saturate(sample)
			line_out[track][i] += sample
			ramp = saturate(ramp + 0.003)

		if len(params) == 7:
			self.voice1NoteIndex = (self.voice1NoteIndex+note_jump) % 3
		else:
			self.voice1NoteIndex = (self.voice1NoteIndex+note_jump) % len(notes)

v1 = noter()
v2 = noter()
v3 = noter()

params1 = [0, voice1, 0.25, 6, 1.0, 0.75]
params2 = [1, voice2, 2.0, 2, 1.0, 0.25]
params3 = [1, voice2, 4.0, 1, 0.4, 0.05, 0]

scheduler.create_schedule(func=v1.note,
						  params=params1,
						  beats_per_call=.75,
						  start_beat=0.0,
						  num_beats=16)
				  
scheduler.create_schedule(func=v3.note,
						  params=params3,
						  beats_per_call=0.25,
						  start_beat=0.125,
						  num_beats=16)

scheduler.create_schedule(func=v2.note,
						  params=params2,
						  beats_per_call=0.25,
						  start_beat=0.0,
						  num_beats=16)

scheduler.run()

# modulate and filter line0
lfo2.set_hz(0)
for i in range(len(line_out[0])):
	line_out[0][i] = voice1_filter.filter_sample(line_out[0][i], 0.03+0.02*lfo2.get_sample(i), 0.0)

line_out[1] = noise1_filter.filter_buffer(line_out[1], 0.46, 0.0)
line_out[1] = mix_buffer(reverb(line_out[1]), line_out[1], 1.0)

line_out[2] = voice3_filter.filter_buffer(line_out[2], 0.66, 0.0)
line_out[2] = mix_buffer(reverb(line_out[2]), line_out[2], 1.0)

# mix
output = mix_buffers(line_out)

goutput = output.copy()
goutput = apply_gain(goutput, 2)
goutput = [saturate(goutput[i]) for i in range(len(goutput))]
goutput = voice2_filter.filter_buffer(goutput, 0.05, 0.0)

output = mix_buffer(goutput, output,  0.3)
output = [saturate(output[i]) for i in range(len(output))]
output = master_filter.filter_buffer(output, 0.65, 0.0)

# write output to WAV
write_buffer_to_wav(output, RENDER_PATH+TITLE+".wav")