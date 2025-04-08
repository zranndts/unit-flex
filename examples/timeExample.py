import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -- IGNORE THAT --

from unitflex import time

# Convert 2.65 hours to seconds with raw output
print(time.convert(2.65, "h", "s", prec=2, format="tag", delim="default")) # OR //
print(time.convert(2.65, "h", "s", prec=2, format="raw", delim="default")) # if format="raw" delimiter will not be used

# Or
print(time.convert(1000, "min", "h", prec="2", format="verbose", delim=True))        # set delimiter True, uses default separator ','
print(time.convert(1000, "min", "h", prec="2", format="verbose", delim="default"))   # set delimiter "default", uses default separator ','
print(time.convert(1000, "min", "h", prec="2", format="verbose", delim="."))         # Set '.' as separator

# Engineering Mode
result = time.convert(1.0052, "decade", "y", prec="10", mode="engineering", format="verbose")
print(result)
