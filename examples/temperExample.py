import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# IGNORE THAT

from unitflex import temper

# Convert celcius fahrenheit to fahrenheit with tag output
print(temper.convert(100, fromUnit="f", toUnit="c", precision=2, format="verbose", delim=True)) # OR //
print(temper.convert(100, "f", "c", "2", "tag", True))
# If delim = True, uses underscore "_" as the default separator because the result can still be processed with arithmetic operations.

# Or
print(temper.convert(250, "reaumur", "rankine", "2", "verbose", True)) 
print(temper.convert(300, "celcius", "rankine", "2", "verbose", ",")) # Set ',' as separator
