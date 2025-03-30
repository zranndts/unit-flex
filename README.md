# Unitflex

Unitflex is a lightweight Python library designed to make unit conversion simple, fast, and flexible. Whether you're working with length or mass units, Unitflex allows you to convert values easily with minimal syntax. It’s built with readability and developer convenience in mind, making it a helpful tool for both beginners and experienced Python users.

The core functionality of Unitflex includes support for converting common units of length such as meters, kilometers, centimeters, inches, feet, and miles, as well as mass units like grams, kilograms, pounds, and ounces. Each conversion method accepts customizable options including precision (to round the result to a specified number of decimal places) and output format, giving users full control over the result’s appearance. You can choose between a simple numeric output, a formatted string with the target unit, or a full descriptive sentence like "5 kg = 5000 g".

Although not yet available on PyPI, Unitflex can be cloned directly from this repository for immediate use. Once installed, users can import and use the `LengthConverter` and `MassConverter` classes from the `unitflex` package. Each class provides a `convert()` method that accepts the value to be converted, the source unit, the target unit, the number of decimal digits, and the preferred output style.

The folder structure of this project is organized for clarity and scalability. The main package, `unitflex`, contains individual modules for each category of conversion (such as `length.py` and `mass.py`). In addition, there are directories for usage examples and test scripts, which help demonstrate the library's capabilities and ensure consistent performance through future updates.

Upcoming features planned for Unitflex include support for temperature conversion (Celsius, Fahrenheit, Kelvin), speed and time conversions, and even a simple command-line interface (CLI) for quick access from the terminal. While external contributions are currently limited as the library is in its early development stage, feedback and suggestions are more than welcome and encouraged.

Unitflex is released under the MIT License, which allows you to freely use, modify, and distribute the library as long as the original license is included. For more information about usage, structure, and licensing, please refer to the LICENSE file included in this repository.
