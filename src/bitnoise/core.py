import wave, struct, random, math
from bitnoise.constants import *

def sin(i, freq):
	return math.sin(float(i) * freq * FIXED_DELTA)


def sq(i, freq):
	if math.sin(float(i) * freq * FIXED_DELTA) < 0:
		return -1.0
	else:
		return 1.0


def saw(i, freq):
    value = math.atan(math.tan(float(freq) * (float(i) * FIXED_DELTA)))
    return value


def noise(i, freq):
	return random.random()*2.0 - 1.0


def comb(buffer, g, M):
	output = [0.0]*len(buffer)

	for i in range(len(buffer)):
		if i - M < 0:
			output[i] = buffer[i]
		else:
			output[i] = buffer[i] + g*output[i-M]
	
	return output


def all_pass(buffer, g, M):
	output = [0.0]*len(buffer)

	for i in range(len(buffer)):
		if i - M < 0:
			output[i] = buffer[i]
		else:
			output[i] = (-g*buffer[i]) + buffer[i-M] + (g*output[i-M])
	
	return output

def reverb(buffer):
	comb1 = comb(buffer, 0.762, 2599)
	comb2 = comb(buffer, 0.683, 3599)
	comb3 = comb(buffer, 0.765, 3399)
	comb4 = comb(buffer, 0.517, 3801)
	comb_result = [(comb1[i] + comb2[i] + comb3[i] + comb4[i])/4.0 for i in range(len(buffer))]

	allpass1 = all_pass(comb_result, 0.7, 1051)
	allpass2 = all_pass(allpass1, 0.7, 337)
	return allpass2


def write_buffer_to_wav(buffer, fname):
	num_channels = 1
	sample_width = 2
	max_sample = 2**(sample_width*8 - 1) - 1

	f = wave.open(fname, 'wb')
	f.setnchannels(num_channels)
	f.setsampwidth(sample_width)
	f.setframerate(SAMPLE_RATE)
	f.setnframes(len(buffer))

	for sample in buffer:
		sample = int(max_sample*saturate(sample))
		data = struct.pack('<h', sample)
		f.writeframesraw(data)

	f.close()


def saturate(value):
	if value > 1.0:
		return 1.0
	elif value < -1.0:
		return -1.0
	return value


def apply_gain(value, gain_amt):
	return value * gain_amt


def mix_buffer(input1, input2, mix):
	return [(mix)*input1[i] + (1.0-mix)*input2[i] for i in range(len(input1))]


def mixer(input1, input2, mix):
	return (mix)*input1 + (1.0-mix)*input2


def note_to_hz(note):
	notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

	if len(note) == 3:
		octave = int(note[2])
	else:
		octave = int(note[1])

	key_number = notes.index(note[0:-1]) + ((octave-1) * 12) + 1
	if key_number < 3:
		key_number += 12
	if octave == 0:
		key_number -= 12

	return 440 * pow(2, (key_number-49) / 12)


def scale(notes):
	return [note_to_hz(note) for note in notes]


def random_note(scale):
	return scale[int(len(scale)*(random.random()))]