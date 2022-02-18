'''
no. 5
 * improve osc class to remove pops
 * add delay effect
 * add adsr
'''

from bitnoise.core import *
from bitnoise.filter import Filter
from bitnoise.adsr import *
from bitnoise.delay import *
from bitnoise.oscillator import Oscillator
from bitnoise.scheduler import Scheduler

TITLE = "n5_soupa"
NUM_SECONDS = 20
NUM_SAMPLES = NUM_SECONDS * SAMPLE_RATE
BPM = 35

output = [0.0]*NUM_SAMPLES

# Voices
osc1 = Oscillator(sq)
osc1.set_hz(880)
osc1.adsr.set_params(ADSR_Params(0.001,0.1,1.0,0.00005))
osc1.gain = 0.05

osc2 = Oscillator(saw)
osc2.set_hz(55/2)
osc2.adsr.set_params(ADSR_Params(0.0001,0.1,1.0,0.2))
osc2.gain = 0.3

osc3 = Oscillator(noise)
osc3.adsr.set_params(ADSR_Params(0.0001,0.1,1.0,0.0005))
osc3.gain = 0.6

filt = Filter()
delay1 = Delay(0.33, 0.6, 0.5)
delay2 = Delay(0.7, 0.5, 0.2)

scheduler = Scheduler(BPM, NUM_SAMPLES, SAMPLE_RATE)

def note(t, params):
    osc = params[0]
    note_len = params[1]
    note_buf = osc.get_note_buffer(note_len)

    for i in range(len(note_buf)):
        if t+i >= len(output):
            break
        output[t+i] = note_buf[i]

scheduler.create_schedule(note, [osc1, 0.25], 0.5, 0, 16)
scheduler.create_schedule(note, [osc2, 0.26], 1, 0, 16)
scheduler.create_schedule(note, [osc3, 0.025], 0.25, 0.125, 16)
scheduler.run()


delay1.apply_to_buffer(output)
#delay2.apply_to_buffer(output)

output = apply_gain(output, 55.5)
output = [saturate(s) for s in output]
output = apply_gain(output, 0.4)


cutoff_start = 0.0001
cutoff_end = 0.15
for s in range(NUM_SAMPLES):
    output[s] = filt.filter_sample(output[s], cutoff_start + (s/NUM_SAMPLES)*(cutoff_end-cutoff_start), 0.0)

output = reverb(output)

# write output to WAV
write_buffer_to_wav(output, RENDER_PATH+TITLE+".wav")