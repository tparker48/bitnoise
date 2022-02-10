from bitnoise.core import *

class Oscillator:
	def __init__(self, wave_function):
		self.wave_function = wave_function
		self.noteOn = False
		self.attack_gain = 1.0
		self.hz = 0.0
	
	def set_hz(self, hz):
		self.hz = hz

		self.noteOn = (hz != 0.0)

		if not self.noteOn:
			self.attack_gain = 0.0

	def get_sample(self, i):
		out = self.attack_gain * self.wave_function(i, self.hz)
		if self.noteOn:
			self.attack_gain = saturate(self.attack_gain + 0.0002)
		return out