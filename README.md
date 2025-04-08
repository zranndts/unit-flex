# What is Unitflex? 📦

**Unitflex** is a Python library for converting values between various measurement units such as **length**, **mass**, **temperature**, **data**, and more.  
It provides a **clean, extensible**, and **user-friendly** interface to perform conversions easily — with customizable output formatting and **high precision modes** for professional use.

Designed to be both **beginner-friendly** and **robust enough for engineers**, Unitflex is suitable for daily tasks, education, and advanced scientific projects.  
It even supports a special `"engineering"` mode for precise calculations using `decimal.Decimal`.

---

# Supported Converters 🧪 
**1. Length (unitflex.length)**<br>
Units: mm, cm, m, km, in, ft, yard, mil, mile, nm, um, pm, dm, angstrom, nmi

**2. Mass (unitflex.mass)**<br>
Units: mg, g, kg, lb, ton, quintal, ounce, oz, st, slug, dram, carat, grain, shortton, longton

**3. Temperature (unitflex.temper)**<br>
Units: celsius, fahrenheit, kelvin, rankine, reaumur<br>
Short names: c, f, k, r, re<br>
Symbols: °c, °f, k, °r, °re

**4. Data (unitflex.data)**<br>
Units: bit, byte, kilobit, kilobyte, megabit, megabyte, gigabit, gigabyte, terabyte, petabyte<br>
Bit: b, Kbps, Mbps (lowercase = bits)<br>
Byte: B, KB, MBps (uppercase = bytes)

**5. Volume (unitflex.vol)**<br>
Units: ml, cl, dl, l, hl, m3, tsp, tbsp, fl oz, cup, pt, qt, gal, in3, ft3, yd3<br>
Supports both metric and imperial units (short and full names)

**6. Pressure (unitflex.press)**<br>
Units: pa, kpa, mpa, bar, mbar, psi, atm, mmhg, torr, inhg, hpa, dyne/cm²<br>
Handles variations like “millibar”, “hectopascal”, etc.

**7. Speed (unitflex.speed)**<br>
Units: m/s, km/h, km/s, mph, knot, ft/s, ft/min, in/s, in/min, cm/s, mm/s, mach<br>
Flexible recognition of various spellings and capitalizations

**8. Time (unitflex.time)**<br>
Units: ns, μs, us, ms, s, min, h, d, wk, mo, yr, decade, century, millennium<br>
Includes local terms like “quarter”, “semester”, “generation” and more<br>
Based on accurate average durations (e.g., 1 month = 30.44 days)

> All units support both short and long forms.  
> The system automatically recognizes and converts them.

<-- There will be many useful converters to come, stay tuned! -->
---

# Parameters Explained 🔧
Each convert() function accepts up to six parameters. The first three are required, the rest are optional for customizing the output.

- value (required)<br> The numeric value to convert (int or float)<br> Example: 100, 3.14

- fromUnit (required)<br> The original unit (short, long name, or symbol)<br> Example: cm, meter, °f

- toUnit (required)<br> The target unit (same format options as fromUnit)<br> Example: km, yard, kelvin

- precision (optional, default = 2)<br> Number of decimal digits in the result<br> Example: precision=3 → 12.345

- format (optional, default = "tag")<br> Output style:<br> • "raw" → numeric only (ideal for calculations)<br> • "tag" → number + unit<br> • "verbose" → detailed explanation (e.g. "1 meter = 100 cm")

- delim (optional)<br> Adds a separator:<br> • True or "default" → comma: 1,000,000<br> • "." → dot: 1.000.000<br> • False → no separator<br>⚠️ **Note on delim and format="raw**<br>
When using format="raw", the output is intended for further calculations. Therefore, even if delim is set to "default" or any custom separator, no separators will be applied — the result will be returned as a clean float, int, or Decimal without formatting.

- mode (optional, default = "standard")<br> • "standard" → default mode<br> • "engineering" → high-precision mode using decimal.Decimal

---

# Notes 📌
- Units are case-insensitive. (Exception: data and speed units where b ≠ B, and formatting like m/s matters.)
- Flexible unit names. For example: "kg", "kilogram", "Kilograms" are all valid and automatically recognized.
- Smart rounding system ensures accurate output and avoids losing significance. Whole number results are automatically simplified.
- Delimiters improve large number readability (e.g., 1_000_000 or 1,000,000).
- Supports multiple output formats: raw number, tagged result (value + unit), or full verbose expression.
- Highly precise with engineering mode — ideal for technical/scientific usage.
- Clear error messages for invalid inputs or unsupported units.
- Easily extendable for custom units in future versions.

⚠️ **Note on Engineering Mode Output:**
When using `mode="engineering"`, the result is returned as a high-precision `Decimal` object to ensure maximum accuracy.<br>Please note that `Decimal` values cannot be directly operated with `float` or `int` types in Python.

If you need to perform mathematical operations with the result, consider casting it manually:
```python
float_result = float(result)
```
---

# Another Information 🔍
This library is now available on PyPI. You can install it directly using `pip install unitflex`. Once installed, you can import and use the unit classes from the unitflex package. Each class provides a convert() method that accepts the value to be converted, the source unit, the target unit, the number of decimal digits, and the preferred output style.

After the installation with `pip install unitflex`, you can import and use this library by:<br>
```python
from unitflex import length, speed, time
 # Convert 12 mach to km/h
a = speed.convert(12, "mach", "km/h")
# Convert 18 years to seconds using delim, prec and format paramaters
b = time.convert(18, "year", "second", delim="default", prec=2, format="tag")
 # Converting 12.0504 nanometers to centimeters using `engineering mode` to obtain a highly accurate result — ideal for outputs with many decimal places. 
c = length.convert(12.0504, "nm", "cm", format="raw", prec=12, mode="engineering")
```

The folder structure of this project is organized for clarity and scalability. The main package, `unitflex`, contains individual modules for each category of conversion (such as `length.py`, `mass.py`, `data.py` and `temperature.py`). In addition, there are directories for usage examples and test scripts, which help demonstrate the library's capabilities and ensure consistent performance through future updates.

Upcoming features planned for unitflex include conversion of area, volume, time or even conversion with scientific units such as electric current, thermodynamic, amount of substance, luminous intensity, frequency, and more. While external contributions are currently limited as the library is in its early development stage, feedback and suggestions are more than welcome and encouraged.

Unitflex is released under the MIT License, which allows you to freely use, modify, and distribute the library as long as the original license is included. For more information about usage, structure, and licensing, please refer to the LICENSE file included in this repository. 
