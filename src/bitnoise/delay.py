from bitnoise.core import *
from bitnoise.filter import *
from bitnoise.oscillator import *

class Delay:
	def __init__(self, delay_time, feedback, wet):
		self.delay_time = delay_time
		self.feedback = feedback
		self.wet = wet
	
	def apply_to_buffer(self, buffer):
		delay_buffer_len = int(self.delay_time*SAMPLE_RATE)
		delay_buffer = [0.0]*delay_buffer_len
		for sample in range(len(buffer)):
			pre_delay_in = buffer[sample]
			buffer[sample] = (1.0-self.wet)*pre_delay_in + self.wet*delay_buffer[sample % delay_buffer_len]
			delay_buffer[sample % delay_buffer_len] *= self.feedback
			delay_buffer[sample % delay_buffer_len] += pre_delay_in
			
			

class TapeDelay:
	def __init__(self, delay_time, feedback, flutter_amount, flutter_speed, wet):
		self.delay_time = delay_time
		self.feedback = feedback
		self.wet = wet
		self.flutter_amount = flutter_amount
		self.flutter_speed = flutter_speed
	
	def apply_to_buffer(self, buffer):
		delay_buffer = buffer.copy()
		reg_delay = Delay(self.delay_time, self.feedback, 1.0)
		reg_delay.apply_to_buffer(delay_buffer)

		lfo = Oscillator(sin)
		lfo.set_hz(self.flutter_speed)

		delay_sample_increment = 1.0
		delay_sample = 0.0
		filt = Filter()
		for sample in range(len(buffer)):
			delay_sample_increment = 1.0 + self.flutter_amount*(-0.05*lfo.get_sample(sample))
			delay_sample += delay_sample_increment
			delay_out = linear_interpolate(delay_buffer, delay_sample)

			delay_out = filt.filter_sample(delay_out, 0.85, 0.0)

			buffer[sample] = (1.0-self.wet)*buffer[sample] + (self.wet)*delay_out