class temperatureConverter:
    conversionToCelsius = {
        "c": lambda x: x, "celsius": lambda x: x, "celcius": lambda x: x, "°c": lambda x: x,
        "f": lambda x: (x - 32) * 5 / 9, "fahrenheit": lambda x: (x - 32) * 5 / 9, "°f": lambda x: (x - 32) * 5 / 9,
        "k": lambda x: x - 273.15, "kelvin": lambda x: x - 273.15, "°k": lambda x: x - 273.15,
        "r": lambda x: (x - 491.67) * 5 / 9, "rankine": lambda x: (x - 491.67) * 5 / 9, "°r": lambda x: (x - 491.67) * 5 / 9,
        "re": lambda x: x * 5 / 4, "reaumur": lambda x: x * 5 / 4, "réaumur": lambda x: x * 5 / 4, "°re": lambda x: x * 5 / 4, "°ré": lambda x: x * 5 / 4

    }

    conversionFromCelsius = {
        "c": lambda x: x, "celsius": lambda x: x, "celcius": lambda x: x, "°c": lambda x: x,
        "f": lambda x: (x * 9 / 5) + 32, "fahrenheit": lambda x: (x * 9 / 5) + 32, "°f": lambda x: (x * 9 / 5) + 32,
        "k": lambda x: x + 273.15, "kelvin": lambda x: x + 273.15, "°k": lambda x: x + 273.15,
        "r": lambda x: (x + 273.15) * 9 / 5, "rankine": lambda x: (x + 273.15) * 9 / 5, "°r": lambda x: (x + 273.15) * 9 / 5,
        "re": lambda x: x * 4 / 5, "reaumur": lambda x: x * 4 / 5, "réaumur": lambda x: x * 4 / 5, "°re": lambda x: x * 4 / 5, "°ré": lambda x: x * 4 / 5 
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
            raise ValueError("Precision can't be negative!")

        formats = {"raw", "compact", "verbose"}
        if format not in formats:
            raise ValueError(f"Output format '{format}' not recognized! Choose from: {', '.join(formats)}")

        if format == "raw":
                return f"{round(convertedValue, int(precision))}"
        elif format == "compact":
            if toUnit in ["c", "f", "k", "r", "re"]:
                return f"{round(convertedValue, int(precision))} °{toUnit}"
            else:
                return f"{round(convertedValue, int(precision))} {toUnit}"
        elif format == "verbose":
            if toUnit in ["c", "f", "k", "r", "re"]:
                return f"{value} °{fromUnit} = {round(convertedValue, int(precision))} °{toUnit}"
            else:
                return f"{value} {fromUnit} = {round(convertedValue, int(precision))} {toUnit}"

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
