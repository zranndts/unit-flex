class volumeConverter:
    conversionRates = {
        # Metric Units (SI)
        "ml": 1e-6, "milliliter": 1e-6, "milliliters": 1e-6,
        "cl": 1e-5, "centiliter": 1e-5, "centiliters": 1e-5,
        "dl": 1e-4, "deciliter": 1e-4, "deciliters": 1e-4,
        "l": 1e-3, "liter": 1e-3, "liters": 1e-3,
        "hl": 0.1, "hectoliter": 0.1, "hectoliters": 0.1,
        "m3": 1, "cubic meter": 1, "cubic meters": 1,
        
        # Imperial / US Units
        "tsp": 4.92892e-6, "teaspoon": 4.92892e-6, "teaspoons": 4.92892e-6,
        "tbsp": 1.47868e-5, "tablespoon": 1.47868e-5, "tablespoons": 1.47868e-5,
        "floz": 2.95735e-5, "fl oz": 2.95735e-5, "fluid ounce": 2.95735e-5, "fluid ounces": 2.95735e-5,
        "cup": 2.36588e-4, "cups": 2.36588e-4,
        "pt": 4.73176e-4, "pint": 4.73176e-4, "pints": 4.73176e-4,
        "qt": 9.46353e-4, "quart": 9.46353e-4, "quarts": 9.46353e-4,
        "gal": 3.78541e-3, "gallon": 3.78541e-3, "gallons": 3.78541e-3,
        "in3": 1.63871e-5, "cubic inch": 1.63871e-5, "cubic inches": 1.63871e-5,
        "ft3": 0.0283168, "cubic foot": 0.0283168, "cubic feet": 0.0283168,
        "yd3": 0.764555, "cubic yard": 0.764555, "cubic yards": 0.764555,
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=2, format="tag", delim=False):
        fromUnit = fromUnit.lower()
        toUnit = toUnit.lower()

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        defaultValue = value * cls.conversionRates[fromUnit]
        convertedValue = defaultValue / cls.conversionRates[toUnit]

        if int(precision) < 0:
            raise ValueError("Precision can't be negative!")

        roundedValue = round(convertedValue, int(precision))
        if roundedValue == int(roundedValue):
            roundedValue = int(roundedValue) 

        if format == "raw":
            return roundedValue

        if roundedValue == int(roundedValue):
            if delim:
                separator = "_" if delim is True or str(delim).lower().strip() == "default" else str(delim)
                formattedValue = f"{int(roundedValue):,}".replace(",", separator)
            else:
                formattedValue = str(int(roundedValue))
        else:
            if delim:
                separator = "_" if delim is True or str(delim).lower().strip() == "default" else str(delim)
                formattedValue = f"{roundedValue:,.{precision}f}".replace(",", separator)
            else:
                formattedValue = f"{roundedValue:.{precision}f}"

        if format == "tag":
            return f"{formattedValue} {toUnit}"
        elif format == "verbose":
            return f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
