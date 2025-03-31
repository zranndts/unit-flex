import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# IGNORE THAT

from unitflex import mass

# Convert 2.5 kilograms to grams with raw output
print(mass.convert(2.65, fromUnit="kg", toUnit="g", precision=2, format="raw", delim=True)) # OR //
print(mass.convert(2.65, "kg", "g", "2", "raw", True))
# If delim = True, uses underscore "_" as the default separator because the result can still be processed with arithmetic operations.

# Or
print(mass.convert(1000, "quintal", "kg", "2", "verbose", True)) # set delimiter True == uses default separator '_'
print(mass.convert(1000, "quintal", "kg", "2", "verbose", ".")) # Set '.' as separator
