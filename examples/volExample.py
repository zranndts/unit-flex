import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -- IGNORE THAT --

from unitflex import vol

# Convert 2.65 gallons to milliliters with tag output
print(vol.convert(2.65, "gal", "ml", prec=2, format="tag", delim=True)) # OR //
print(vol.convert(2.65, "gal", "ml", prec=2, format="tag", delim="default"))
# If delim == True or "default", uses underscore "_" as the default separator because the result can still be processed with arithmetic operations.

# Or
print(vol.convert(1, "l", "tsp", prec=2, format="verbose", delim=" default ")) # You can use "default" or True for default delimiter
print(vol.convert(1, "m3", "cup", prec=2, format="verbose", delim="."))        # Set '.' as separator
print(vol.convert(200, "ml", "tbsp", prec=2, format="verbose", delim="default"))     # Set ',' as separator

# Engineering Mode
result = vol.convert(0.9982123, "ml", "m3", prec="10", mode="engineering", format="verbose")
print(result)