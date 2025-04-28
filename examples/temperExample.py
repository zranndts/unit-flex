import unitflex as uf
from unitflex import temper

# Convert 100 Celsius to Fahrenheit, tag dan raw output
print(temper.convert(100, "celsius", "fahrenheit", prec=2, format="tag", delim="default")) # OR //
print(temper.convert(100, "celsius", "fahrenheit", prec=2, format="raw", delim="default")) # raw = no delimiter

# Or
print(temper.convert(77, "f", "k", prec="3", format="verbose", delim=True))        # uses default ','
print(temper.convert(77, "f", "k", prec="3", format="verbose", delim="default"))   # uses default ','
print(temper.convert(77, "f", "k", prec="3", format="verbose", delim="."))         # use '.' as delimiter

# Engineering Mode - extremely high precision
result = temper.convert(451, "fahrenheit", "k", prec="30", mode="engineering", format="verbose")
print(result)

print(f"\nUnitflex version: {uf.__version__}")