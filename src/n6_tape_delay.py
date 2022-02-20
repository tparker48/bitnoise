'''
no. 6
 * attempt tape delay effect
'''

from bitnoise.core import *
from bitnoise.filter import Filter
from bitnoise.adsr import *
from bitnoise.delay import *
from bitnoise.oscillator import Oscillator
from bitnoise.scheduler import Scheduler

TITLE = "n6_tape_delay"
NUM_SECONDS = 8
NUM_SAMPLES = NUM_SECONDS * SAMPLE_RATE
BPM = 83

output = [0.0]*NUM_SAMPLES

# Voices
osc1 = Oscillator(saw)
osc1.set_hz(110)
osc1.adsr.set_params(ADSR_Params(0.03,0.06,0.3,0.03))
osc1.gain = 0.7

filt = Filter()

td = TapeDelay(0.2, 0.6, 0.05, 0.3, 0.5)

scheduler = Scheduler(BPM, NUM_SAMPLES, SAMPLE_RATE)

notes = scale(['E3', 'A3', 'D3','D2'])

def note(t, params):
    osc = params[0]
    note_len = params[1]
    note_buf = osc.get_note_buffer(note_len)

    hz = random_note(notes)
    osc.set_hz(hz)

    for i in range(len(note_buf)):
        if t+i >= len(output):
            break
        output[t+i] = note_buf[i]

scheduler.create_schedule(note, [osc1, 0.15], 0.35, 0, 8)
scheduler.run()

td.apply_to_buffer(output)

output = filt.filter_buffer(output, 0.2, 0.0)

# write output to WAV
write_buffer_to_wav(output, RENDER_PATH+TITLE+".wav")