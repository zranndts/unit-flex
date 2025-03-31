# What is unitflex? 📦

unitflex is a Python library for converting values between various measurement units such as length, mass, temperature, and data. It provides a clean and extensible interface to convert units with ease and even lets you customize the formatting of the result.

# Supported Converters 🧪 

- Length (unitflex.length)
Supports: mm, cm, m, km, in, ft, yard, mile, nm, um, etc.

- Mass (unitflex.mass)
Supports: mg, g, kg, lb, ton, carat, etc.

- Temperature (unitflex.temper)
Supports: celsius, fahrenheit, kelvin, rankine, reaumur
Short names: c, f, k, r, re
Symbols supported: "°c", "°f", "°r", "°re", etc.

- Data (unitflex.data)
Supports: bit, byte, kb, mb, gb, tb, pb, mbps, gbps, etc.

<!-- There will be many useful converters to come, stay tuned! -->

#  Parameters Explained 🔧

Each convert() function accepts up to six parameters. The first three are required, the rest are optional for customizing the output.

1. value (required)

The numeric value to convert. Can be an int or float.
Example: 100, 3.14

2. fromUnit (required)

A string representing the source unit. Case-insensitive. Supports short and long forms.
Example: "cm", "meter", "kilobyte", "°f"

3. toUnit (required)

A string representing the target unit. Same rules as fromUnit.
Example: "km", "yard", "megabit"

4. precision (optional, default = 2)

Number of decimal places to round the result.
Must be a non-negative integer.
Use 0 for whole number output.
Example: precision=3 → 12.345

5. format (optional, default = "tag")

Controls how the result is formatted:
"raw" → returns only the number as a int/float: "123.45"
raw format is used if the conversion result will be subjected to math operations.

"tag" → returns number with unit: "123.45 cm"

"verbose" → full expression: "5 meter = 500 cm"

6. delim (optional)

Adds a thousands separator to large numbers for readability:

True → underscore separator: 1_000_000 (default separator)
default separator is good to use with raw format, because it is intended to produce int/float conversion results that can be used for further calculations.

"," → comma separator: 1,000,000

"." → dot separator: 1.000.000

False → no separator

# Notes 📌

- Units are case-insensitive.
- Flexible naming (e.g., "kg", "kilogram", "Kilograms" all work).
- Safe rounding with fallback if result is an integer.
- Delimiters help with large numbers.

# Another Information 🔍

This module is not yet available on PyPI, Unitflex can be cloned directly from this repository for immediate use. Once installed, users can import and use the `length`, `mass`, `temper` and `data` classes from the `unitflex` package. Each class provides a `convert()` method that accepts the value to be converted, the source unit, the target unit, the number of decimal digits, and the preferred output style.

The folder structure of this project is organized for clarity and scalability. The main package, `unitflex`, contains individual modules for each category of conversion (such as `length.py`, `mass.py`, `data.py` and `temperature.py`). In addition, there are directories for usage examples and test scripts, which help demonstrate the library's capabilities and ensure consistent performance through future updates.

upcoming features planned for unitflex include conversion of area, volume, time or even conversion with scientific units such as electric current, thermodynamic, amont of substance, luminous intensity, hz etc. While external contributions are currently limited as the library is in its early development stage, feedback and suggestions are more than welcome and encouraged.

Unitflex is released under the MIT License, which allows you to freely use, modify, and distribute the library as long as the original license is included. For more information about usage, structure, and licensing, please refer to the LICENSE file included in this repository.