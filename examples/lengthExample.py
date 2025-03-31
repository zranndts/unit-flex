import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# IGNORE THAT

from unitflex import length

# Convert 5 kilometers to meters without delimiter and default precision and format
print(length.convert(5, "km", "m"))
# If delim = True, uses underscore "_" as the default separator because the result can still be processed with arithmetic operations.

# Convert 12 inches to centimeters with precision 1, verbose (detail output) delim (delimiter) ',' as separator 
print(length.convert(49, "km", "cm", "1", "verbose", ","))
print(length.convert(1, "cm", "nm", "2", "tag", ","))
