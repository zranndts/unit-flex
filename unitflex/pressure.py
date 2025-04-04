class pressureConverter:
    conversionRates = {
        # SI Units
        "pa": 1, "pascal": 1, "pascals": 1,

        # Metric multiples
        "kpa": 1e3, "kilopascal": 1e3, "kilopascals": 1e3,
        "kpa": 1e3, "kilopascal": 1e3, "kilopascals": 1e3,
        "mpa": 1e6, "megapascal": 1e6, "megapascals": 1e6,
        "gpa": 1e9, "gigapascal": 1e9, "gigapascals": 1e9,
        "hpa": 100, "hectopascal": 100, "hectopascals": 100,

        # Bar units
        "bar": 1e5, "bars": 1e5,
        "mbar": 1e2, "millibar": 1e2, "millibars": 1e2,

        # Atmosphere
        "atm": 101325, "atmosphere": 101325, "atmospheres": 101325,

        # Torr / mmHg
        "torr": 133.322, "mmhg": 133.322, "mmHg": 133.322, "millimeter of mercury": 133.322, "millimeters of mercury": 133.322,

        # Inches of Mercury
        "inhg": 3386.39, "inch of mercury": 3386.39, "Inch of mercury": 3386.39,
        "inHg": 3386.39, "inches of mercury": 3386.39, "Inches of mercury": 3386.39,

        # Per Square Inch
        "psi": 6894.76, "pound per square inch": 6894.76, "pounds per square inch": 6894.76,
        "ksi": 6_894_760, "kip per square inch": 6_894_760, "kips per square inch": 6_894_760,
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
