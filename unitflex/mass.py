class massConverter:
    conversionRates = {
        "kg": 1,
        "g": 0.001,
        "mg": 0.000001,
        "ton": 1000,
        "lb": 0.453592,
        "oz": 0.0283495,
        "st": 6.35029
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