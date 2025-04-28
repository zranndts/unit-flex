from unitflex import config
config.DEBUG = True 

from unitflex import time

time.convert(1, "s", "century", mode="engineering", prec=12)
time.convert(1, "s", "millennium", mode="engineering", prec=25)
time.convert(0.0000000000316880878140290, "millennium", "s", mode="engineering")
