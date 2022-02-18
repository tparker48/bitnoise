from bitnoise.adsr import *
from bitnoise.core import *

class Oscillator:
	def __init__(self, wave_function):
		self.wave_function = wave_function
		self.noteOn = False
		self.attack_gain = 1.0
		self.hz = 0.0
		self.gain = 1.0
		self.adsr = ADSR(ADSR_Params(0.1,0.1,0.1,0.1))
	
	def set_hz(self, hz):
		self.hz = hz

		self.noteOn = (hz != 0.0)

		if not self.noteOn:
			self.attack_gain = 0.0

	def get_sample(self, i):
		out = self.attack_gain * self.wave_function(i, self.hz)
		if self.noteOn:
			self.attack_gain = saturate(self.attack_gain + 0.0002)
		return out * self.gain

	def noCallback(osc, sample, callback_params):
		return 0

	def get_note_buffer(self, note_length, callback=noCallback, callback_params=None):
		note_buffer = []
		note_samples = (note_length)*SAMPLE_RATE
		release_samples = (self.adsr.get_params().release)*SAMPLE_RATE

		# generate output
		for sample in range(int(note_samples+release_samples)):
			callback(self, sample, callback_params)
			note_buffer.append(self.gain*self.wave_function(sample, self.hz))

		# apply adsr
		self.adsr.apply_adsr(note_buffer, 0, note_samples)
		return note_buffer
