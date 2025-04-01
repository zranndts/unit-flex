import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unitflex import length, mass, temper, data

print("\n------ Length\n")

# Length Test

# Use precision, adjust format and delim (delimeter)
print(length.convert(12, fromUnit="miles", toUnit="cm", precision="2", format="verbose", delim=True))
print(length.convert(12, fromUnit="miles", toUnit="cm", precision="2", format="verbose", delim=True))
print(length.convert(10, fromUnit="miles", toUnit="cm", precision="2", format="tag", delim=","))
print(length.convert(10, fromUnit="miles", toUnit="cm", precision="2", format="tag", delim="."))
print(length.convert(10, fromUnit="miles", toUnit="cm", precision="2", format="tag", delim="-"))

# Round result 
print(length.convert(1.609, fromUnit="km", toUnit="miles", precision="2", format="tag", delim=","))
print(length.convert(1.609, fromUnit="km", toUnit="miles", precision="2", format="tag", delim=True))

# Decimal or Float Result
print(length.convert(100, "yard", "cm", "2", "tag", "."))

# Use precision, and format adjust 
print(length.convert(5, fromUnit="mi", toUnit="km", precision="1", format="verbose"))   
print(length.convert(160, fromUnit="cm", toUnit="ft", precision="4", format="tag"))
print(length.convert(180, fromUnit="cm", toUnit="ft", precision="1", format= "tag"))
print(length.convert(158, fromUnit="cm", toUnit="ft", precision="2", format= "tag"))
num1 = length.convert(180, fromUnit="cm", toUnit="ft", precision="2", format="raw")
num2 = length.convert(158, "cm", "ft", "2", "raw")
result = num1 - num2
print(f"Our height difference is {round(result, 2)} ft")

# Use precision only
print(length.convert(150, fromUnit="ft", toUnit="cm", precision="2"))
print(length.convert(150, fromUnit="ft", toUnit="cm", precision="2"))

# Just convert without any output adjustment
print(length.convert(175, fromUnit="cm", toUnit="ft"))

# Simple usage
print(length.convert(1, "cm", "nm", "1", "tag", ","))
print(length.convert(1, "cm", "nm", "1", "tag", ","))
print(length.convert(5.9, "ft", "cm", "2", "verbose"))
print(length.convert(12, "nm", "um"))

print("\n------ Mass\n")

# Mass Test
print(mass.convert(120, fromUnit="kg", toUnit="lb", precision="2", format="verbose"))
print(mass.convert(1, fromUnit="ton", toUnit="mg", precision="2", format="verbose", delim=","))
print(mass.convert(275, fromUnit="lb", toUnit="kg", precision="3", format="tag"))
print(mass.convert(150650, fromUnit="g", toUnit="lb", precision="4", format="raw"))
lb1 = mass.convert(15065, fromUnit="g", toUnit="lb", precision="4", format="raw")
print(mass.convert(12321, fromUnit="g", toUnit="lb", precision="4", format="raw"))
lb2 = mass.convert(12321, fromUnit="g", toUnit="lb", precision="4", format="raw")
print(lb1 - lb2)
print(mass.convert(12123, "g", "kg", "2", "tag"))
print(mass.convert(24, "carat", "g"))

print("\n------ Temper\n")

# Temperature Test
print(temper.convert(1000, fromUnit="c", toUnit="f", precision="2", format="verbose", delim=","))
print(temper.convert(36, fromUnit="c", toUnit="f", precision="2", format="verbose"))
print(temper.convert(12, fromUnit="f", toUnit="k", precision="2", format="tag"))
print(temper.convert(128, fromUnit="K", toUnit="C", precision="2", format="tag"))
print(temper.convert(128, fromUnit="Kelvin", toUnit="celcius", precision="2", format="tag", delim=","))
print(temper.convert(128, fromUnit="°r", toUnit="°c", precision="2", format="verbose"))
print(temper.convert(38, fromUnit="c", toUnit="re", precision="2", format="verbose"))
print(temper.convert(38, fromUnit="r", toUnit="re", precision="2", format="raw"))
re = temper.convert(38, "r", "re", "2", "raw")
print(temper.convert(380, "c", "re", "2", "raw"))
re2 = temper.convert(380, "c", "re", "2", "raw")
print(re + re2)
print(temper.convert(38, fromUnit="r", toUnit="f", precision="2", format="verbose"))
print(temper.convert(666, "celcius", "fahrenheit", "2", "verbose", ","))
print(temper.convert(36, "c", "k", "2"))

print("\n------ Data\n")

# Data Test 
print(data.convert(1, fromUnit="pb", toUnit="gb", format="verbose", delim=","))
print(data.convert(10, fromUnit="bytes", toUnit="bit", format="tag"))
print(data.convert(1, fromUnit="gbyte", toUnit="bit", format="tag", delim=","))
print(data.convert(80, fromUnit="mbps", toUnit="mbyte", format="verbose"))
print(data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw"))
gb1 = data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw")
print(data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw"))
gb2 = data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw")
print(gb1 + gb2)
print(data.convert(1, "gbps", "mbps", "2", "tag", ","))