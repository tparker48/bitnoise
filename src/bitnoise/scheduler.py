from bitnoise.core import *

class Process:
    def __init__(self, function, params):
        self.func = function
        self.params = params
    
    def call(self, t):
        self.func(t, self.params)

class Scheduler:
    def __init__(self, bpm, num_samples, sample_rate, ticks_per_beat = 128):
        ticks_per_second = (bpm * ticks_per_beat) / 60
        self.ticks_per_beat = ticks_per_beat
        self.samples_per_tick = int(sample_rate / ticks_per_second)
        self.beat_counter = 0.0
        self.tick_counter = 0
        self.num_samples = num_samples * sample_rate
        self.schedule = {}

    def create_schedule(self, func, params, beats_per_call, start_beat, num_beats):
        process = Process(func, params)

        ticks_per_call = int(beats_per_call * self.ticks_per_beat)
        samples_per_call = ticks_per_call * self.samples_per_tick
        start_sample = int(self.samples_per_tick * (start_beat * self.ticks_per_beat))
        end_sample = int(self.samples_per_tick * ((start_beat + num_beats) * self.ticks_per_beat))

        for t in range(start_sample, min(end_sample, self.num_samples), samples_per_call):
            if t in self.schedule:
                self.schedule[t].append(process)
            else:
                self.schedule[t] = [process]
                

        return
    
    def run(self):
        for t in self.schedule.keys():
            for process in self.schedule[t]:
                process.call(t)
