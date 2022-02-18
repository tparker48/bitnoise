from bitnoise.core import *

class Filter:
	def __init__(self):
		self.buf0 = 0.0000
		self.buf1 = 0.0000
	
	def filter_sample(self, inp, f, q):
		fb = q + q/(1.0 - f)
		self.buf0 = self.buf0 + f * (inp - self.buf0 + fb * (self.buf0 - self.buf1))
		self.buf1 = self.buf1 + f * (self.buf0 - self.buf1)
		return self.buf1
	
	def filter_buffer(self, inp_buff, f, q):
		for i in range(len(inp_buff)):
			inp_buff[i] = self.filter_sample(inp_buff[i], f, q)
		return inp_buff