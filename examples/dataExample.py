import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# IGNORE THAT

from unitflex import data

# Convert 2.5 Petabytes to megabytes with tag output
print(data.convert(2.65, fromUnit="pb", toUnit="mb", precision=2, format="tag", delim=True)) # OR //
print(data.convert(2.65, "pb", "mb", "2", "tag", "default"))
# If delim == True or "default", uses underscore "_" as the default separator because the result can still be processed with arithmetic operations.

# Or
print(data.convert(1, "gb", "bit", "2", "verbose", " default ")) #You can use "default" or True for default delimiter
print(data.convert(1, "mb", "bit", "2", "verbose", ".")) # Set '.' as separator
print(data.convert(200, "kilobyte", "bit", "2", "verbose", ",")) # Set ',' as separator
