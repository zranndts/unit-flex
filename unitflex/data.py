class dataConverter:
    conversionRates = {
        "mb": 1,
        "bit": 0.000000125,
        "byte": 0.000001,
        "kb": 0.001,
        "gb": 1000,
        "tb": 1000000,
        "pb": 1000000000,
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=1, format="compact"):
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
        
        validationFormatting = {"raw", "compact", "verbose"}
        if format not in validationFormatting:
            raise (f"Output format '{format}' not recognized! Choose from: {', '.join(validationFormatting)}")
    
        if format == "raw":
            result = f"{round(convertedValue, int(precision))}"
            return result
        elif format == "compact":
            result = f"{round(convertedValue, int(precision))} {toUnit}"
            return result
        elif format == "verbose":
            result = f"{value} {fromUnit} = {round(convertedValue, int(precision))} {toUnit}"
            return result
        else:
            raise ValueError("Unexpected format parameters!")
