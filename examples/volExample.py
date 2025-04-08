import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -- IGNORE THAT --

from unitflex import vol

# Convert 2.65 gallons to milliliters with tag output
print(vol.convert(2.65, fromUnit="gal", toUnit="ml", precision=2, format="tag", delim=True)) # OR //
print(vol.convert(2.65, "gal", "ml", "2", "tag", "default"))
# If delim == True or "default", uses underscore "_" as the default separator because the result can still be processed with arithmetic operations.

# Or
print(vol.convert(1, "l", "tsp", "2", "verbose", " default ")) # You can use "default" or True for default delimiter
print(vol.convert(1, "m3", "cup", "2", "verbose", "."))        # Set '.' as separator
print(vol.convert(200, "ml", "tbsp", "2", "verbose", ","))     # Set ',' as separator
