class lengthConverter:
    conversionRates = {
        "m": 1,
        "km": 1000,
        "cm": 0.01,
        "mm": 0.001,
        "mi": 1609.34,
        "yd": 0.9144,
        "ft": 0.3048,
        "in": 0.0254
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=2, output="compact"):
        fromUnit = fromUnit.lower()
        toUnit = toUnit.lower()

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        defaultValue = value * cls.conversionRates[fromUnit]
        convertedValue = defaultValue / cls.conversionRates[toUnit]

        if int(precision) < 0:
            raise ValueError("precisson can't be negative!")
        
        if output == "raw":
            result = f"{round(convertedValue, int(precision))}"
            return result
        elif output == "compact":
            result = f"{round(convertedValue, int(precision))} {toUnit}"
            return result
        elif output == "verbose":
            result = f"{value} {fromUnit} = {round(convertedValue, int(precision))} {toUnit}"
            return result
        else:
            raise ValueError("Unexpected output parameters!")
