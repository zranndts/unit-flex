import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# IGNORE THAT

from unitflex import mass

# Convert 2.5 kilograms to grams with raw number output
print(mass.convert(2.65, fromUnit="kg", toUnit="g", precision=2, format="raw"))

# Or 
print(mass.convert(24, "carat", "gram", "2", "verbose"))
