import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -- IGNORE THAT --

from unitflex import (
    length,
    mass,
    temper,
    data,
    vol,
    press,
    speed,
    time
)

# Length conversion
print(length.convert(12.3200912, "nm", "m", prec="17", mode="engineering", format="verbose"))
# Output: 12.3200912 nm = 0.00000001232009120 m

# Mass conversion
print(mass.convert(2.5, "kg", "lb", format="tag", prec=3))  
# Output: 2.5_kg = 5.512_lb

# Temperature conversion
print(temper.convert(100, "C", "F", format="verbose", prec=1))  
# Output: 100 °C = 212.0 °F

# Data conversion
print(data.convert(1024, "MiB", "GiB", format="raw", prec=2))  
# Output: 1.0GiB

# Volume conversion
print(vol.convert(3.785, "liter", "gallon", prec=4, format="verbose", delim=True))  
# Output: 3.785 liter = 1.0 gallon

# Pressure conversion
print(press.convert(1, "atm", "Pa", format="verbose", prec=0, delim="."))  
# Output: 1 atm = 101.325.Pa

# Speed conversion
print(speed.convert(120, "km/h", "m/s", prec=2, format="tag"))  
# Output: 120_km/h = 33.33_m/s

# Time conversion
print(time.convert(1, "day", "second", format="verbose", prec=0))  
# Output: 1 day = 86400 second

# Engineering mode example (high precision)
print(mass.convert(1.23456789, "kilogram", "gram", prec="25", mode="engineering"))  
# Output: 1.23456789 kilogram = 1234.5678900000000000000000000 gram
