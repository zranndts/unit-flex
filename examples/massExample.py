import unitflex as uf
from unitflex import mass

# Convert 1500 grams to pounds, menggunakan tag dan raw output
print(mass.convert(1500, "grams", "pounds", prec=4, format="tag", delim="default"))  # OR //
print(mass.convert(1500, "grams", "pounds", prec=4, format="raw", delim="default"))  # raw = no delimiter

# Or
print(mass.convert(5, "kg", "stone", prec="3", format="verbose", delim=True))         # uses default ','
print(mass.convert(5, "kg", "stone", prec="3", format="verbose", delim="default"))    # uses default ','
print(mass.convert(5, "kg", "stone", prec="3", format="verbose", delim="."))          # use '.' as delimiter

# Engineering Mode - extremely high precision
result = mass.convert(5.001232123, "mg", "ons", prec="16", mode="engineering", format="verbose")
print(result)

print(f"\nUnitflex version: {uf.__version__}")