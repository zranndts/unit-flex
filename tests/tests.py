import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unitflex import length
from unitflex import mass
from unitflex import temper
from unitflex import data

# Length Test
print(length.convert(12, fromUnit="km", toUnit="m", format="verbose"))
print(length.convert(5, fromUnit="mi", toUnit="km", precision="1", format="compact"))   
print(length.convert(160, fromUnit="cm", toUnit="ft", precision="4", format="compact"))
print(length.convert(160, fromUnit="cm", toUnit="ft", precision="1"))
print(length.convert(150, fromUnit="ft", toUnit="cm", precision="2", format="raw"))
print(length.convert(6, "ft", "cm", "2", "compact"))
print(length.convert(5.9, "ft", "cm"))
print(length.convert(12, "nm", "um", "3", "verbose"))

print("\n------\n")

# Mass Test
print(mass.convert(120, fromUnit="kg", toUnit="lb", precision="2", format="verbose"))
print(mass.convert(275, fromUnit="lb", toUnit="kg", precision="3", format="compact"))
print(mass.convert(150650, fromUnit="mg", toUnit="lb", precision="1", format="raw"))
print(mass.convert(12123, "g", "kg", "2", "compact"))
print(mass.convert(24, "carat", "g"))

print("\n------\n")

# Temperature Test
print(temper.convert(36, fromUnit="c", toUnit="f", precision="2", format="verbose"))
print(temper.convert(12, fromUnit="f", toUnit="k", precision="2", format="compact"))
print(temper.convert(128, fromUnit="K", toUnit="C", precision="2", format="compact"))
print(temper.convert(128, fromUnit="Kelvin", toUnit="celcius", precision="2", format="compact"))
print(temper.convert(128, fromUnit="°r", toUnit="°c", precision="2", format="verbose"))
print(temper.convert(38, fromUnit="c", toUnit="re", precision="2", format="verbose"))

print("\n------\n")

# Data Test 
print(data.convert(100, fromUnit="gb", toUnit="pb", format="verbose"))
print(data.convert(10, fromUnit="byte", toUnit="bit", format="verbose"))
print(data.convert(80, fromUnit="mbps", toUnit="mbyte", format="verbose"))
print(data.convert(80, fromUnit="mbps", toUnit="gbps", format="verbose"))