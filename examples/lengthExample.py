from unitflex.length import LengthConverter

# Convert 5 kilometers to meters with default precision and format
print(LengthConverter.convert(5, "km", "m"))

# Convert 12 inches to centimeters with precision 1 and full format
print(LengthConverter.convert(12, "in", "cm", precission=1, formatStyle="verbose"))
