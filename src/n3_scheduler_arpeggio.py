'''
no. 3
 * Demonstration of new Scheduler class, timing sounds a lot cleaner
 * Scheduler allows for easy, precise, and flexible control
'''

from bitnoise.core import *
from bitnoise.filter import Filter
from bitnoise.oscillator import Oscillator
from bitnoise.scheduler import Scheduler

TITLE = "n3_scheduler_arpeggio"
NUM_SECONDS = 15
NUM_SAMPLES = NUM_SECONDS * SAMPLE_RATE
BPM = 60

# a note-playing function for the scheduler
# functions for scheduling take arguments as a list
def note(t, params):
	osc = params[0]
	note_seconds = params[1] / (BPM / 60)
	out_buffer  = params[2]
	mode = params[3]
	gain = params[4]
	end_sample = int(t + SAMPLE_RATE * note_seconds)

	if type(mode) == type([]):
		osc.set_hz(random_note(mode))
	else:
		osc.set_hz(mode)

	for i in range(t, min(end_sample, NUM_SAMPLES)):
		out_buffer[i] += gain*osc.get_sample(i)

# scales for random note generation
hi_scale1 = scale(['E4', 'D4', 'A4', 'E3', 'D3', 'A3'])
hi_scale2 = scale(['D4', 'A4', 'C4', 'A3', 'D3', 'C3'])
hi_scale = [hi_scale1, hi_scale2]

lo_scale1 = scale(['E0', 'E1'])
lo_scale2 = scale(['D0', 'D1'])
lo_scale = [lo_scale1, lo_scale2]

#components
scheduler = Scheduler(BPM, NUM_SAMPLES, SAMPLE_RATE)
osc = Oscillator(saw)
bass_LPF = Filter()
arp_LPF = Filter()

# output buffers
arp_out = [0.0] * NUM_SAMPLES
bass_out = [0.0] * NUM_SAMPLES

# scheduling parameters
num_beats = 8
bass_gain = 0.5
bass_note_duration = 1
bass_beats_per_note = 2
arp_gain = 0.5 / 2.0
arp_note_duration = 0.1
arp_beats_per_note = 1
arp_offsets = [0, 1/3, 2/3]

for i in range(2):
	start_beat = num_beats * i

	# schedule bass
	scheduler.create_schedule(note, [osc, bass_note_duration, bass_out, lo_scale[i], bass_gain], bass_beats_per_note, start_beat, num_beats)

	# schedule arp
	scheduler.create_schedule(note, [osc, arp_note_duration, arp_out, hi_scale[i][0]/4.0, arp_gain], 1, start_beat + arp_offsets[0], num_beats)
	scheduler.create_schedule(note, [osc, arp_note_duration, arp_out, hi_scale[i][0]/2.0, arp_gain], 1, start_beat + arp_offsets[1], num_beats)
	scheduler.create_schedule(note, [osc, arp_note_duration, arp_out, hi_scale[i],        arp_gain], 1, start_beat + arp_offsets[2], num_beats)

# render audio generated by schedules
scheduler.run()
	
# bass channel effects
bass_out = bass_LPF.filter_buffer(bass_out, 0.035, 0.0)
bass_out = mix_buffer(reverb(bass_out), bass_out, 0.3)

# arp channel effects
arp_out = arp_LPF.filter_buffer(arp_out, 0.185, 0.0)
arp_out = mix_buffer(reverb(arp_out), arp_out, 0.7)
arp_out = mix_buffer(reverb(arp_out), arp_out, 0.4)

# mix bass and arp channels
output = mix_buffer(bass_out, arp_out, 0.5)

# write output to WAV
write_buffer_to_wav(output, RENDER_PATH+TITLE+".wav")