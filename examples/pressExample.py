import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -- IGNORE THAT --

from unitflex import press

# Convert 2.65 atmospheres to pascals with raw output
print(press.convert(2.65, "atm", "pa", prec=2, format="tag", delim="default")) # OR //
print(press.convert(2.65, "atm", "pa", prec=2, format="raw", delim="default")) # if format="raw" delimiter will not be used

# Or
print(press.convert(1000, "kpa", "mpa", prec="2", format="verbose", delim=True))        # set delimiter True, uses default separator ','
print(press.convert(1000, "kpa", "mpa", prec="2", format="verbose", delim="default"))   # set delimiter "default", uses default separator ','
print(press.convert(1000, "kpa", "mpa", prec="2", format="verbose", delim="."))         # Set '.' as separator

# Engineering Mode
result = press.convert(1.0052, "psi", "mpa", prec="12", mode="engineering", format="verbose")
print(result)
