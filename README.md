# What is Unitflex? 📦
Unitflex is a Python library for converting values between various measurement units such as length, mass, temperature, and data. It provides a clean and extensible interface to convert units with ease and even lets you customize the formatting of the result.

# Supported Converters 🧪 
1. Length (unitflex.length)<br>Supports: `mm`, `cm`, `m`, `km`, `in`, `ft`, `yard`, `mil` or `thou`, `mile`, `nm`, `um`, `pm`, `dm`, `angstrom` and `nmi`

2. Mass (unitflex.mass)<br>Supports: `mg`, `g`, `kg`, `lb`, `ton`, `quintal`, `ons`, `oz`, `st`, `slug`, `dram`, `carat`, `grain`, `shortton` and `longton`.

3. Temperature (unitflex.temper)<br>Supports: `celsius`, `fahrenheit`, `kelvin`, `rankine` and `reaumur`. Short names: `c`, `f`, `k`, `r`, `re`. Symbols supported: `°c`, `°f`, `k`, `°r` and `°re`.

4. Data (unitflex.data)<br>Supports: `bit`, `byte`, `kilobit`, `kilobyte`, `megabit`, `megabyte`, `gigabit`, `gigabyte`, `terabyte`, `petabyte`.<br>When converting data units, this library differentiates between bits `b` and bytes `B`. Since 1 byte = 8 bits, incorrect capitalization can lead to incorrect conversions.<br>Bit-based units: `b`, `Kbps`, `Mbps`, `Gbps`, etc. (lowercase `b` represents bits)<br>Byte-based units: `B`, `KB`, `MBps`, `GBps`, etc. (uppercase `B` represents bytes)

5. Volume (unitflex.vol)<br>Supports: `ml`, `cl`, `dl`, `l`, `hl`, `m3`, `tsp`, `tbsp`, `fl oz`, `cup`, `pt`, `qt`, `gal`, `in3`, `ft3`, `yd3` and their full forms like `milliliter`, `cubic meter`, `fluid ounce`, etc. Both metric and imperial units are supported.

6. Pressure (unitflex.press)<br>Supports: `pa`, `kpa`, `mpa`, `bar`, `mbar`, `psi`, `atm`, `mmhg`, `torr`, `inhg`, `hpa`, and `dyne/cm²`. Full names and alternate spellings are recognized, such as `millibar`, `hectopascal`, `millimeter of mercury`, and more.

7. Speed (unitflex.speed)<br>Supports: `m/s`, `km/h`, `km/s`, `mph`, `knot`, `ft/s`, `ft/min`, `in/s`, `in/min`, `cm/s`, `mm/s`, `and mach (assumed at sea level)`. Accepts multiple variants in casing and formatting.

8. Time (unitflex.time)<br>Supports: `ns`, `μs`, `us`, `ms`, `s`, `min`, `h`, `d`, `wk`, `mo`, `yr`, `decade`, `century`, `millennium`, as well as localized time terms like `triwulan`, `semester`, `millennium"`, `generation`, , and more. All units are based on precise average durations (e.g., month = 30.44 days, year1 = 365.25 days).

You can specify units using either their abbreviations or full names. The system will automatically recognize and adjust accordingly.

<-- There will be many useful converters to come, stay tuned! -->
<!-- There will be many useful converters to come, stay tuned! -->

# Parameters Explained 🔧
Each convert() function accepts up to six parameters. The first three are required, the rest are optional for customizing the output.

1. value (required)<br>The numeric value to convert. Can be an int or float.<br>Example: `100, 3.14`

2. fromUnit (required)<br>A string representing the source unit, case-insensitive, supports short and long forms. Exception for data units as it must differentiate `b` bits and `B` bytes.<br>Example: `cm`, `meter`, `Kb`, `KB`, `°f`

3. toUnit (required)<br>A string representing the target unit. Same rules as fromUnit.<br>Example: `km`, `yard`, `megabit`, `reamur`.

4. precision (optional, `default = 2`)<br>Number of decimal places to round the result.<br>Must be a non-negative integer.<br>Use 0 for whole number output.<br>Example: `precision=3 → 12.345`

5. format (optional, default = `tag`)<br>Controls how the result is formatted:<br>`"raw"` → returns only the number as an int/float: `123.45`. <br>Raw format is used if the conversion result will be subjected to math operations.<br>`"tag"` → returns number with unit: "123.45 cm".<br>`"verbose"` → full expression: "5 meter = 500 cm"

6. delim (optional)<br>Adds a thousands separator to large numbers for readability:<br>`True` or `"default"` → underscore separator: 1_000_000 (default separator). Default separator is good to use with raw format, because it is intended to produce int/float conversion results that can be used for further calculations.<br>Or you can use a custom separator by replacing the delimiter parameter value with whatever string you want to be the separator, for example:<br>`","` → comma separator: 1,000,000<br>`"."` → dot separator: 1.000.000<br>`False` → no separator.

# Notes 📌
- Units are case-insensitive. (exception for data and speed unit)
- Flexible naming (e.g., "kg", "kilogram", "Kilograms" all work).
- Safe rounding with fallback if result is an integer.
- Delimiters help with large numbers.

# Another Information 🔍
This module is now available on PyPI. You can install it directly using `pip install unitflex`. Once installed, you can import and use the length, mass, temper, and data classes from the unitflex package. Each class provides a convert() method that accepts the value to be converted, the source unit, the target unit, the number of decimal digits, and the preferred output style.

The folder structure of this project is organized for clarity and scalability. The main package, `unitflex`, contains individual modules for each category of conversion (such as `length.py`, `mass.py`, `data.py` and `temperature.py`). In addition, there are directories for usage examples and test scripts, which help demonstrate the library's capabilities and ensure consistent performance through future updates.

Upcoming features planned for unitflex include conversion of area, volume, time or even conversion with scientific units such as electric current, thermodynamic, amount of substance, luminous intensity, frequency, and more. While external contributions are currently limited as the library is in its early development stage, feedback and suggestions are more than welcome and encouraged.

Unitflex is released under the MIT License, which allows you to freely use, modify, and distribute the library as long as the original license is included. For more information about usage, structure, and licensing, please refer to the LICENSE file included in this repository.
