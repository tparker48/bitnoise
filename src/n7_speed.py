'''
no. 7
 * ...
'''

from bitnoise.core import *
from bitnoise.filter import Filter
from bitnoise.adsr import *
from bitnoise.delay import *
from bitnoise.oscillator import Oscillator
from bitnoise.scheduler import Scheduler

TITLE = "n7_speed"
NUM_SECONDS = 25
NUM_SAMPLES = NUM_SECONDS * SAMPLE_RATE
BPM = 22

output = []
hi_out = [0.0]*NUM_SAMPLES
bass_out = [0.0]*NUM_SAMPLES
snare_out = [0.0]*NUM_SAMPLES
bdrum_out = [0.0]*NUM_SAMPLES

osc1 = Oscillator(saw)
osc1.adsr.set_params(ADSR_Params(0.03,0.06,0.3,0.03))
osc1.gain = 0.7

osc2 = Oscillator(sq)
osc2.adsr.set_params(ADSR_Params(0.001,0.01,1.0,0.01))
osc2.gain = 0.5

snare = Oscillator(noise)
snare.adsr.set_params(ADSR_Params(0.001,0.01,1.0,0.01))
snare.gain = 2.0

hh = Oscillator(noise)
hh.adsr.set_params(ADSR_Params(0.001,0.01,1.0,0.01))
hh.gain = 0.6

bdrum = Oscillator(tri)
bdrum.adsr.set_params(ADSR_Params(0.00001,0.1,0.2,0.67))
bdrum.gain = 1.5

filt = Filter()
bass_filt = Filter()
td = TapeDelay(0.2325, 0.4, 0.08, 0.2, 0.5)
vib = TapeDelay(0.0001, 0.0, 0.69, 2.0, 0.3)
vib2 = TapeDelay(0.0001, 0.0, 0.49, 3.0, 0.3)
scheduler = Scheduler(BPM, NUM_SAMPLES, SAMPLE_RATE)
notes1 = scale(['E3','B3','G3','D3'])
notes2 = scale(['E1'])
bdrum_note = scale(['E1'])


def note(t, params):
    osc = params[0]
    note_len = params[1]
    notes = params[2]
    output = params[3]

    hz = random_note(notes)
    osc.set_hz(hz)

    if random.random() < 0.0:
        return

    note_buf = osc.get_note_buffer(note_len)

    for i in range(len(note_buf)):
        if t+i >= len(output):
            break
        output[t+i] = note_buf[i]

scheduler.create_schedule(note, [osc1, 0.1, notes1, hi_out], 0.125, 0, 8)
scheduler.create_schedule(note, [osc2, 0.5, notes2, bass_out], 0.5, 2, 6)
scheduler.create_schedule(note, [snare, 0.06, notes2, snare_out], 0.5, 0.25, 8)
scheduler.create_schedule(note, [hh, 0.01, notes2, snare_out], 0.125, 4, 4)
scheduler.create_schedule(note, [bdrum, 0.1, bdrum_note, bdrum_out], 0.25, 0, 8)

scheduler.run()

td.apply_to_buffer(hi_out)
vib.apply_to_buffer(bass_out)
bass_filt.filter_buffer(bass_out, 0.08, 0.0)

output = mix_buffers([hi_out, bass_out, bdrum_out, snare_out])
output = filt.filter_buffer(output, 0.4, 0.0)

#output = apply_gain(output, 64.0)

#output = [output[i]*1.0*(1.5+sin(i,0.4)) for i in range(len(output))]
output = apply_gain(output, 5.0)
output = [saturate(x) for x in output]
output = apply_gain(output, 0.6)

output = filt.filter_buffer(output, 0.40, 0.0)
output = mix_buffer(reverb(output), output, 0.1)
vib2.apply_to_buffer(output)

# write output to WAV
write_buffer_to_wav(output, RENDER_PATH+TITLE+".wav")
