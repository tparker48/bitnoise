from bitnoise.core import *

class Delay:
	def __init__(self, delay_time, feedback, wet):
		self.delay_time = delay_time
		self.feedback = feedback
		self.wet = wet
	
	def apply_to_buffer(self, buffer):
		delay_buffer_len = int(self.delay_time*SAMPLE_RATE)
		delay_buffer = [0.0]*delay_buffer_len
		pre_delay_in = 0.0
		for sample in range(len(buffer)):
			pre_delay_in = buffer[sample]
			buffer[sample] = (1.0-self.wet)*pre_delay_in + self.wet*delay_buffer[sample % delay_buffer_len]
			delay_buffer[sample % delay_buffer_len] += pre_delay_in
			delay_buffer[sample % delay_buffer_len] *= self.feedback
			