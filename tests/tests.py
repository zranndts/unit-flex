import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unitflex import length, mass, temper, data, vol, press, speed, time

print("\n------ Length\n")

# Length Test

# Use precision, adjust format and delim (delimeter)
print(length.convert(12, fromUnit="miles", toUnit="cm", precision="2", format="verbose", delim=True))
print(length.convert(12, fromUnit="miles", toUnit="cm", precision="2", format="verbose", delim="default"))
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
print(mass.convert(120_000, fromUnit="kg", toUnit="lb", precision="2", format="verbose"))
print(mass.convert(1, fromUnit="ton", toUnit="mg", precision="2", format="verbose", delim=","))
print(mass.convert(275, fromUnit="lb", toUnit="kg", precision="3", format="tag"))
print(mass.convert(15_650, fromUnit="g", toUnit="lb", precision="4", format="raw"))
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
print(data.convert(80, fromUnit="MBps", toUnit="Mbps", format="verbose"))
print(data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw"))
gb1 = data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw")
print(data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw"))
gb2 = data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw")
print(gb1 + gb2)
print(data.convert(1, "gbps", "mbps", "2", "tag", ","))

print("\n------ Volume\n")

# Volune Test
print(vol.convert(1_000_000, fromUnit="ml", toUnit="m3", precision="2", format="tag"))
print(vol.convert(1_000_000, fromUnit="milliliter", toUnit="cubic meter", precision="2", format="tag", delim=","))
print(vol.convert(2.5, fromUnit="l", toUnit="gal", precision="4", format="verbose"))
print(vol.convert(5, fromUnit="gallon", toUnit="liter", precision="3", format="verbose"))
print(vol.convert(10, fromUnit="tbsp", toUnit="ml", precision="2", format="raw"))
raw1 = vol.convert(1, "pt", "ml", "3", "raw")
raw2 = vol.convert(2, "qt", "ml", "3", "raw")
print(raw1 + raw2)
print(vol.convert(999999, fromUnit="ml", toUnit="l", precision="0", format="tag", delim="_"))
print(vol.convert(750, "ml", "cup", "3", "verbose"))
print(vol.convert(10, "cup", "tsp", "0", "tag"))
print(vol.convert(3.78541, "l", "gal", "5", "verbose"))
print(vol.convert(2, "in3", "cl", "2"))

print("\n------ Pressure\n")

# Pressure Test
print(press.convert(1_000_000, fromUnit="pa", toUnit="mpa", precision="2", format="tag"))
print(press.convert(1_000_000, fromUnit="pascal", toUnit="megapascal", precision="2", format="tag", delim=","))
print(press.convert(2.5, fromUnit="bar", toUnit="psi", precision="4", format="verbose"))
print(press.convert(14.7, fromUnit="psi", toUnit="bar", precision="3", format="verbose"))
print(press.convert(10, fromUnit="atm", toUnit="pa", precision="2", format="raw"))
raw1 = press.convert(1, "torr", "pa", "3", "raw")
raw2 = press.convert(2, "inHg", "pa", "3", "raw")
print(raw1 + raw2)
print(press.convert(101325, fromUnit="pa", toUnit="atm", precision="0", format="tag", delim=True))
print(press.convert(750, "mmHg", "psi", "3", "verbose"))
print(press.convert(10, "psi", "torr", "0", "tag"))
print(press.convert(29.92, "inHg", "hpa", "5", "verbose"))
print(press.convert(1013.25, "mbar", "bar", "2"))

print("\n------ Speed\n")

# Speed Test
print(speed.convert(120, fromUnit="km/h", toUnit="m/s", precision=2, format="tag"))
print(speed.convert(100, fromUnit="km per hour", toUnit="meter per second", precision="3", format="verbose", delim=","))
print(speed.convert(60, fromUnit="mph", toUnit="fps", precision=3, format="verbose"))
print(speed.convert(30, fromUnit="kt", toUnit="km/h", precision=2, format="verbose"))
print(speed.convert(20, fromUnit="knot", toUnit="m/s", precision=4, format="tag"))
print(speed.convert(1, "mach", "km/h", "2", "verbose"))
print(speed.convert(343, "m/s", "mach", "4", "verbose"))
print(speed.convert(10, "km/h", "mph", "3", "raw")) 
print(speed.convert(10000, "cm/s", "km/h", "5", "raw", ","))
print(speed.convert(999_999, "mm/s", "m/s", "1", "tag"))
raw_speed = speed.convert(100, "km/h", "m/s", "2", "raw")
raw_speed2 = speed.convert(36, "km/h", "m/s", "2", "raw")
print(raw_speed + raw_speed2)
print(speed.convert(100, "mph", "km/h", "2", "verbose", True))
print(speed.convert(88, "ft/s", "km/h", "3", "tag"))
print(speed.convert(5, "m/s", "cm/s", "0", "tag"))
print(speed.convert(60, "km/h", "ft/s", "2", "verbose"))
print(speed.convert(1, "c", "mach", "6", "verbose", delim=","))
print(speed.convert(1, "speed of light", "km/h", "1", "verbose", delim=","))

print("\n------ Time")

# Time Test
print(time.convert(3600, "s", "h", 2, "tag"))
print(time.convert(1, "day", "h", 2, "tag", ","))
print(time.convert(1, "year", "mo", 4, "verbose"))
print(time.convert(90, "minute", "hr", 2, "verbose"))
print(time.convert(5, "week", "d", 0, "raw"))
r1 = time.convert(2, "hr", "sec", 0, "raw")
r2 = time.convert(30, "min", "sec", 0, "raw")
print(r1 + r2)
print(time.convert(1000000, "ms", "s", 1, "tag", True))
print(time.convert(2500000000, "ns", "ms", 4, "verbose"))
print(time.convert(2, "triwulan", "mo", 2))
print(time.convert(1, "semester", "days", 2))
print(time.convert(1, "decade", "yr", 0))
print(time.convert(2, "century", "windu", 2))
print(time.convert(1, "millennium", "year", 0))