import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -- IGNORE THAT --

from unitflex import length
from unitflex import mass
from unitflex import temper
from unitflex import data

print("Mass conversion with all output adjustment parameters; precision, format and delim.")
print(mass.convert(24, "ton", "kg", "2", "verbose", True))
print(mass.convert(24, "ton", "g", "2", "tag", ","))

print("\nLength conversion with all output adjustment parameters; precision, format and delim.")
print(length.convert(10, "mi", "cm", "2", "verbose", True))
print(length.convert(10, "mi", "cm", "2", "tag", ","))

print("\nTemper (temperature) conversion with all output adjustment parameters; precision, format and delim.")
print(temper.convert(1000, "c", "k", "2", "tag", True))
print(temper.convert(1000, "c", "k", "2", "verbose", ","))

print("\nData conversion with all output adjustment parameters; precision, format and delim.")
print(data.convert(1, "gigabit", "bit", "2", "verbose", True))
print(data.convert(48, "gigabyte", "kbps", "2", "tag", ","))

print("------")

# Use precision, adjust format and delim (delimiter)
print("\nUse precision, adjust format and delim (delimiter)")
print(length.convert(12, "miles", "cm", "2", "verbose", True))
print(mass.convert(12, "ton", "g", "2", "verbose", True))
print(data.convert(1, "petabyte", "megabyte", "2", "tag", ","))
print(data.convert(1, "gigabyte", "bit", "3", "tag", "."))
print(temper.convert(500, "c", "k", "2", "tag", "."))
print(length.convert(10, "miles", "cm", "2", "raw", "."))

# Round result
print("\nRound result")
print(length.convert(1.609, "km", "miles", "2", "tag", ",")) #Output < 1000, delimiter is not used
print(mass.convert(1000, "kg", "ton", "2", "tag", True)) # Output < 1000, delimiter is not used

# Decimal or Float result
print("\nDecimal or Float result")
print(data.convert(1000, "byte", "bit", "2", "tag", ","))
print(data.convert(899, "megabyte", "megabit", "2", "tag", ","))

# Use precision, and format adjust
print("\nUse precision, and format adjust ")
print(mass.convert(24, "carat", "gram", "2", "verbose"))   
print(length.convert(160, "cm", "ft", "4", "tag"))
print(temper.convert(16, "c", "f", "3",  "tag"))
print(length.convert(180, "cm", "ft", "2",  "raw"))

# Use precision only
print("\nUse precision only")
print(length.convert(150, "ft", "cm", "2"))

# Just convert without any output adjustment
print("convert without any output adjustment (default output)")
print(mass.convert(10, "ons", "kg"))
