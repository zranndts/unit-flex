class temperatureConverter:
    conversionToCelsius = {
        "c": lambda x: x,
        "f": lambda x: (x - 32) * 5 / 9,
        "k": lambda x: x - 273.15
    }

    conversionFromCelsius = {
        "c": lambda x: x,
        "f": lambda x: (x * 9 / 5) + 32,
        "k": lambda x: x + 273.15
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=1, format="compact"):
        fromUnit = fromUnit.lower()
        toUnit = toUnit.lower()

        if fromUnit not in cls.conversionToCelsius:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionFromCelsius:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        celsiusValue = cls.conversionToCelsius[fromUnit](value)
        convertedValue = cls.conversionFromCelsius[toUnit](celsiusValue)

        if int(precision) < 0:
            raise ValueError("precision can't be negative!")

        validationFormatting = {"raw", "compact", "verbose"}
        if format not in validationFormatting:
            raise ValueError(f"Output format '{format}' not recognized! Choose from: {', '.join(validationFormatting)}")
        
        if format == "raw":
            result = f"{round(convertedValue, int(precision))}"
        elif format == "compact":
            result = f"{round(convertedValue, int(precision))} {toUnit}"
        elif format == "verbose":
            result = f"{value} {fromUnit} = {round(convertedValue, int(precision))} {toUnit}"
        else:
            raise ValueError("Unexpected format parameters!")
        
        return result
