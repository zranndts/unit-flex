import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -- IGNORE THAT --

from unitflex import data

# Basic conversion
print(data.convert(8_000_000, "bits", "megabyte", prec=2, format="tag"))          # Output: 1.0_MB
print(data.convert(8_000_000, "bits", "megabyte", prec=2, format="raw"))          # Output: 1.0MB

# Verbose format with default delimiter (comma)
print(data.convert(3.5, "GB", "MB", format="verbose", prec=4, delim=True))        # Output: 3.5 GB = 3,500 MB

# Verbose format with period delimiter
print(data.convert(3.5, "GB", "MB", format="verbose", prec=4, delim="."))         # Output: 3.5 GB = 3.500 MB

# Using binary units
print(data.convert(1, "GiB", "MiB", format="verbose", prec=0))                    # Output: 1 GiB = 1024 MiB

# Engineering mode – very high precision
print(data.convert(1.21, "exabyte", "megabyte", prec="30", mode="engineering"))   # Output: 1.21 exabyte = 1210000000.0000000000000000000000000000 megabyte