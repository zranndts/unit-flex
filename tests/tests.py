import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unitflex import length, mass, temper, data, vol, press, speed, time

print("\n------ Length\n")

# Length Test

# Use precision, adjust format and delim (delimeter), and engineering mode
print(length.convert(12, fromUnit="miles", toUnit="cm", prec=2, format="verbose", delim="default"))
print(length.convert(12, "miles", "cm", prec=2, format="verbose", delim="default"))
print(length.convert(10, "miles", "cm", prec=2, format="tag", delim=","))
print(length.convert(10, "miles", "cm", prec=2, format="tag", delim="."))
print(length.convert(10, "miles", "cm", prec=2, format="tag", delim="-"))
num1 = length.convert(1.23456789, "miles", "km", prec=12,format="raw", delim="_", mode="engineering")
num2 = length.convert(9.87654321, "miles", "km", prec=12,format="raw", delim="_", mode="engineering")
print(f"{num1 + num2} km")


# Round result 
print(length.convert(1.609, fromUnit="km", toUnit="miles", prec=2, format="tag", delim=","))
print(length.convert(1.609, "km", "miles", prec=2, format="tag", delim=True))

# Decimal or Float Result
print(length.convert(100, "yard", "cm", prec=2, format="tag", delim="."))

# Use prec, and format adjust 
print(length.convert(5, fromUnit="mi", toUnit="km", prec=1, format="verbose"))   
print(length.convert(160, "cm", "ft", prec=4, format="tag"))
print(length.convert(180, "cm", "ft", prec=1, format="tag"))
print(length.convert(158, "cm", "ft", prec=2, format="tag"))
num1 = length.convert(180, "cm", "ft", prec=2, format="raw")
num2 = length.convert(158, "cm", "ft", prec=2, format="raw")
result = num1 - num2
print(f"Our height difference is {round(result, 2)} ft")

# Use prec only
print(length.convert(150, fromUnit="ft", toUnit="cm", prec=2))
print(length.convert(150, fromUnit="ft", toUnit="cm", prec=2))

# Just convert without any output adjustment
print(length.convert(175, fromUnit="cm", toUnit="ft"))

# Simple usage
print(length.convert(1, "cm", "nm", prec=1, format="tag", delim=","))
print(length.convert(1, "cm", "nm", prec=1, format="tag", delim=","))
print(length.convert(5.9, "ft", "cm", prec=2, format="verbose"))
print(length.convert(12, "nm", "um"))

print("\n------ Mass\n")

# Mass Test
print(mass.convert(120_000, fromUnit="kg", toUnit="lb", prec=2, format="verbose"))
print(mass.convert(1, "ton", "mg", prec=2, format="verbose", delim=","))
print(mass.convert(275, "lb", "kg", prec=4, format="tag"))
print(mass.convert(15_650, "g", "lb", prec=4, format="raw"))
lb1 = mass.convert(15, "g", "lb", prec=12, format="raw", mode="engineering")
print(mass.convert(12, "g", "lb", prec=4, format="raw", ))
lb2 = mass.convert(14.46005, "g", "lb", prec=12, format="raw", mode="engineering")
print(lb1 - lb2)
print(mass.convert(12123, "g", "kg", prec=2, format="tag"))
print(mass.convert(24, "carat", "g"))

print("\n------ Temper\n")

# Temperature Test
print(temper.convert(1000, fromUnit="c", toUnit="f", prec=2, format="verbose", delim=","))
print(temper.convert(36, "c", "f", prec=2, format="verbose"))
print(temper.convert(12, "f", "k", prec=2, format="tag"))
print(temper.convert(128, "K", "C", prec=2, format="tag"))
print(temper.convert(128, "Kelvin", "celcius", prec=2, format="tag", delim=","))
print(temper.convert(128, "°r", "°c", prec=2, format="verbose"))
print(temper.convert(38, "c", "re", prec=2, format="verbose"))
print(temper.convert(38, "r", "re", prec=2, format="raw"))
re = temper.convert(38, "r", "re", prec=2, format="raw")
print(temper.convert(380, "c", "re", prec=2, format="raw"))
re2 = temper.convert(380, "c", "re", prec=2, format="raw")
print(re - re2)
print(temper.convert(38, "r", "f", prec=2, format="verbose"))
print(temper.convert(666.1234567898, "celcius", "fahrenheit", prec=7, format="verbose", delim=",", mode="engineering"))
print(temper.convert(36, "c", "k", prec=2))

print("\n------ Data\n")

# Data Test 
print(data.convert(1, fromUnit="pb", toUnit="gb", format="verbose", delim=","))
print(data.convert(10, fromUnit="bytes", toUnit="bit", format="tag"))
print(data.convert(1, fromUnit="gbyte", toUnit="bit", format="tag", delim=","))
print(data.convert(1, fromUnit="gbyte", toUnit="bit", prec=1, format="tag", delim="default", mode="engineering"))
print(data.convert(80, fromUnit="MBps", toUnit="Mbps", format="verbose"))
print(data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw"))
gb1 = data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw")
print(data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw"))
gb2 = data.convert(150, fromUnit="mbps", toUnit="gbps", format="raw")
print(gb1 + gb2)
print(data.convert(1, "gbps", "mbps", prec=2, format="tag", delim=","))

print("\n------ Volume\n")
# Volune Test
print(vol.convert(1_000_000, fromUnit="ml", toUnit="m3", prec=2, format="tag"))
print(vol.convert(1_000_000, fromUnit="milliliter", toUnit="cubic meter", prec=2, format="tag", delim=","))
print(vol.convert(2.5, fromUnit="l", toUnit="gal", prec=4, format="verbose"))
print(vol.convert(5, fromUnit="gallon", toUnit="liter", prec=4, format="verbose"))
print(vol.convert(10, fromUnit="tbsp", toUnit="ml", prec=2, format="raw"))
raw1 = vol.convert(1, "pt", "ml", prec=10, format="raw", mode="engineering")
raw2 = vol.convert(2, "qt", "ml", prec=10, format="raw", mode="engineering")
print(raw1 + raw2)
print(vol.convert(999999, fromUnit="ml", toUnit="l", prec=0, format="tag", delim="_"))
print(vol.convert(750, "ml", "cup", prec=10, format="verbose", mode="engineering"))
print(vol.convert(10, "cup", "tsp", prec=0, format="tag"))
print(vol.convert(3.78541, "l", "gal", prec=5, format="verbose"))
print(vol.convert(2, "in3", "cl", prec=2))
print(vol.convert(2, "in3", "cl", prec=2, delim="dot"))

print("\n------ Pressure\n")

# Pressure Test
print(press.convert(1_000_000, fromUnit="pa", toUnit="mpa", prec=2, format="tag"))
print(press.convert(1_000_000, fromUnit="pascal", toUnit="megapascal", prec=2, format="tag", delim=","))
print(press.convert(2.5, fromUnit="bar", toUnit="psi", prec=4, format="verbose"))
print(press.convert(14.7, fromUnit="psi", toUnit="bar", prec=4, format="verbose"))
print(press.convert(10, fromUnit="atm", toUnit="pa", prec=2, format="raw"))
raw1 = press.convert(1, "torr", "pa", prec=4, format="raw")
raw2 = press.convert(2, "inHg", "pa", prec=4, format="raw")
print(raw1 + raw2)
print(press.convert(101325, fromUnit="pa", toUnit="atm", prec=0, format="tag", delim=True))
print(press.convert(750, "mmHg", "psi", prec=4, format="verbose"))
print(press.convert(10, "psi", "torr", prec=0, format="tag"))
print(press.convert(29.92, "inHg", "hpa", prec=5, format="verbose"))
print(press.convert(1013.25, "mbar", "bar", prec=2))

print("\n------ Speed\n")

# Speed Test
print(speed.convert(120, fromUnit="km/h", toUnit="m/s", prec=2, format="tag"))
print(speed.convert(100, fromUnit="km per hour", toUnit="meter per second", prec=4, format="verbose", delim=","))
print(speed.convert(60, fromUnit="mph", toUnit="fps", prec=3, format="verbose"))
print(speed.convert(30, fromUnit="kt", toUnit="km/h", prec=2, format="verbose"))
print(speed.convert(20, fromUnit="knot", toUnit="m/s", prec=4, format="tag"))
print(speed.convert(1, "mach", "km/h", prec=2, format="verbose"))
print(speed.convert(343, "m/s", "mach", prec=4, format="verbose"))
print(speed.convert(10, "km/h", "mph", prec=4, format="raw")) 
print(speed.convert(10000, "cm/s", "km/h", prec=5, format="raw", delim=","))
print(speed.convert(999_999, "mm/s", "m/s", prec=1, format="tag"))
raw_speed = speed.convert(100, "km/h", "m/s", prec=10, format="raw", delim="default", mode="engineering")
raw_speed2 = speed.convert(36, "km/h", "m/s", prec=10, format="raw", delim="default", mode="engineering")
print(f"{raw_speed} m/s + {raw_speed2} m/s = {raw_speed + raw_speed2} m/s")
print(speed.convert(100, "mph", "km/h", prec=2, format="verbose", delim=True))
print(speed.convert(88, "ft/s", "km/h", prec=4, format="tag"))
print(speed.convert(5, "m/s", "cm/s", prec=0, format="tag"))
print(speed.convert(60, "km/h", "ft/s", prec=2, format="verbose"))
print(speed.convert(1, "c", "mach", prec=6, format="verbose", delim=","))
print(speed.convert(1, "speed of light", "km/h", prec=1, format="verbose", delim=","))

print("\n------ Time")

# Time Test
print(time.convert(3600, "s", "h", prec=2, format="tag"))
print(time.convert(50, "day", "h", prec=2, format="raw", delim=".")) # if format="raw" delimiter will not be used
print(time.convert(1, "year", "mo", prec=4, format="verbose"))
print(time.convert(90, "minute", "hr", prec=2, format="verbose"))
print(time.convert(5, "week", "d", prec=0, format="raw"))
r1 = time.convert(2, "hr", "sec", prec=0, format="raw")
r2 = time.convert(30, "min", "sec", prec=0, format="raw")
print(r1 + r2)
print(time.convert(1_000_000, "ms", "s", prec=1, format="verbose", delim=True))
print(time.convert(2_500_000_000, "ns", "ms", prec=1, format="verbose"))
print(time.convert(2, "triwulan", "mo", prec=2))
print(time.convert(1, "semester", "days", prec=2))
print(time.convert(3, "week", "year", prec=12, format="tag", mode="engineering"))
print(time.convert(1, "decade", "yr", prec=0))
print(time.convert(2, "century", "windu", prec=2))
print(time.convert(1, "millennium", "year", prec=0))