from bitnoise.core import *

# attack: number of seconds to approach full volume after noteOn
# decay: number of seconds to reach secondary volume after reaching full volume
# sustain: the secondary volume
# release: number of seconds to reach 0 after noteOff
class ADSR_Params:
	def __init__(self, a=0.1, d=0.1, s=1.0, r=0.1):
		self.attack = a
		self.decay = d
		self.sustain = s
		self.release = r
		

class ADSR:
	def __init__(self, params):
		self.params=params
	
	def get_params(self):
		return self.params

	def set_params(self, params):
		self.params = params

	# return a buffer of gain values
	# apply these values to an audio buffer to create ADSR
	def get_gain_buffer(self, num_samples, note_on_sample, note_off_sample):
		gain_buffer = []
		level = 0.0

		num_attack_samples = self.params.attack * SAMPLE_RATE
		num_decay_samples = self.params.decay * SAMPLE_RATE
		num_release_samples = self.params.release * SAMPLE_RATE

		attack_end = note_on_sample + num_attack_samples
		decay_end = attack_end + num_decay_samples
		sustain_level = self.params.sustain
		
		attack_rate = 1.0 / num_attack_samples
		decay_rate = (sustain_level - 1.0) / num_decay_samples
		release_rate = -sustain_level / num_release_samples

		for sample in range(num_samples):
			if sample < note_on_sample:
				gain_buffer.append(0.0)

			elif sample < note_off_sample:

				if sample < attack_end:
					level += attack_rate
					if level > 1.0:
						level = 1.0

				elif sample < decay_end:
					level += decay_rate
					if level < sustain_level:
						level = sustain_level
			else:
				level += release_rate
				if level < 0.0:
					level = 0.0

			gain_buffer.append(level)
			
		return gain_buffer

	def apply_adsr(self, buffer, note_on_sample, note_off_sample):
		gain_buffer = self.get_gain_buffer(len(buffer), note_on_sample, note_off_sample)
		for sample in range(len(buffer)):
			buffer[sample] = apply_gain(buffer[sample], gain_buffer[sample])