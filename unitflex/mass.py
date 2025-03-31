class massConverter:
    conversionRates = {
        # Metric Units
        "mg": 1e-6, "milligram": 1e-6, "milligrams": 1e-6,
        "g": 1e-3, "gram": 1e-3, "grams": 1e-3,
        "kg": 1, "kilogram": 1, "kilograms": 1,
        "t": 1_000, "ton": 1_000, "tons": 1_000, "metricton": 1_000,
        "quintal": 100,
        "ons": 0.1, "ons-nl": 0.1,

        # Imperial/US Units
        "oz": 0.028_349_5, "ounce": 0.028_349_5, "ounces": 0.028_349_5,
        "lb": 0.453_592, "pound": 0.453_592, "pounds": 0.453_592,
        "st": 6.350_29, "stone": 6.350_29, "stones": 6.350_29,
        "slug": 14.593_9,
        "dram": 0.001_771_845_195_312_5, "dr": 0.001_771_845_195_312_5,

        # Smaller/Scientific Units
        "carat": 0.000_2,
        "grain": 0.000_064_798_91,

        # Ton variations
        "shortton": 907.184_74,
        "longton": 1_016.046_908_8,
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
            if delim:
                separator = "_" if delim is True else str(delim)
                formattedValue = f"{int(roundedValue):,}".replace(",", separator)
            else:
                formattedValue = str(int(roundedValue))
        else:
            if delim:
                separator = "_" if delim is True else str(delim)
                formattedValue = f"{roundedValue:,.{precision}f}".replace(",", separator)
            else:
                formattedValue = f"{roundedValue:.{precision}f}"

        if format == "raw":
            return formattedValue
        elif format == "tag":
            return f"{formattedValue} {toUnit}"
        elif format == "verbose":
            return f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")