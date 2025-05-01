import unitflex as uf
from unitflex import temperature as temp

# Convert 100 Celsius to Fahrenheit, tag dan raw output
print(temp.convert(100, "celsius", "fahrenheit", prec=2, format="tag", delim="default")) # OR //
print(temp.convert(100, "celsius", "fahrenheit", prec=2, format="raw", delim="default")) # raw = no delimiter

# Or
print(temp.convert(77, "f", "k", prec="3", format="verbose", delim=True))        # uses default ','
print(temp.convert(77, "f", "k", prec="3", format="verbose", delim="default"))   # uses default ','
print(temp.convert(77, "f", "k", prec="3", format="verbose", delim="."))         # use '.' as delimiter

# Engineering Mode - extremely high precision
result = temp.convert(451, "fahrenheit", "k", prec="30", mode="engineering", format="verbose")
print(result)

print(f"\nUnitflex version: {uf.__version__}")