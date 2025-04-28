import unitflex as uf
from unitflex import length

# Convert 1000000 micrometers to meters
print(length.convert(1_000_000, "micrometers", "meters", prec=2, format="tag", delim="default"))  # OR //
print(length.convert(1_000_000, "micrometers", "meters", prec=2, format="raw", delim="default"))  # raw = no delimiter

# Or
print(length.convert(2.5, "km", "mile", prec="4", format="verbose", delim=True))        # uses default ','
print(length.convert(2.5, "km", "mile", prec="4", format="verbose", delim="default"))   # uses default ','
print(length.convert(2.5, "km", "mile", prec="4", format="verbose", delim="."))         # use '.' as delimiter

# Engineering Mode - high precision
result = length.convert(12.3200912, "nm", "m", prec="17", mode="engineering", format="verbose")
print(result)

print(f"\nUnitflex version: {uf.__version__}")