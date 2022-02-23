import math
import time

SAMPLE_RATE = 40
DURATION = 1500
SECONDS_PER_SAMPLE = 1.0/SAMPLE_RATE
NUM_SAMPLES = DURATION * SAMPLE_RATE
CONSTANT_DELTA = 2*math.pi / SAMPLE_RATE

WIDTH = 60
STAMP = '     BITNOISE     '
EMT = '||'*(WIDTH-15)


def sin(t, freq):
    raw_sin = math.sin(t * freq * CONSTANT_DELTA)
    adjusted = (raw_sin + 1.0) / 2.0
    x_value = int(adjusted * WIDTH)
    return x_value

def paint(canvas, brush, x):
    return canvas[:x] + brush + canvas[x + len(brush):]


f1 = 0.05
f2 = 1.5

prefix = ' ' * 50
for t in range(int(NUM_SAMPLES)):

    s = time.time()
    c1 = EMT

    for i in range(10):
        x1 = int(0.5*(sin(t+i, f1) + sin(t, f1*8)))
        x2 = sin(t+i*2, f2)
        x3 = int(0.5*(x1+x2))
        c1 = paint(c1, '/                          \\', x3-5)

    print(prefix + c1)
    e = time.time()
    time.sleep(SECONDS_PER_SAMPLE - (s-e))