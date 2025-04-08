import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -- IGNORE THAT --

from unitflex import speed

# Convert 75 km/h to m/s with tag and raw output
print(speed.convert(75, "km/h", "m/s", prec=2, format="tag", delim="default")) # OR //
print(speed.convert(75, "km/h", "m/s", prec=2, format="raw", delim="default")) # raw = no delimiter

# Or
print(speed.convert(1234567.89, "mm/min", "km/h", prec=3, format="verbose", delim=True))        # uses default ','
print(speed.convert(1234567.89, "mm/min", "km/h", prec=3, format="verbose", delim="default"))   # uses default ','
print(speed.convert(1234567.89, "mm/min", "km/h", prec=3, format="verbose", delim="."))         # use '.' as delimiter

# Engineering Mode - extremely high precision
result = speed.convert(1.23456789, "mach", "m/s", prec=11, mode="engineering", format="verbose")
print(result)
