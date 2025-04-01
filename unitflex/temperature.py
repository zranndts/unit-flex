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
    def convert(cls, value, fromUnit, toUnit, precision=1, format="tag", delim=False):
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
        
        roundedValue = round(convertedValue, int(precision))
        if roundedValue == int(roundedValue):
            roundedValue = int(roundedValue) 

        if format == "raw":
            return roundedValue

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
    
        if format == "tag":
            if toUnit in ["c", "f", "k", "r", "re"]:
                return f"{formattedValue} °{toUnit}"
            else:
                return f"{formattedValue} {toUnit}"
        elif format == "verbose":
            if toUnit in ["c", "f", "k", "r", "re"]:
                return f"{value} °{fromUnit} = {formattedValue} °{toUnit}"
            else:
                return f"{value} {fromUnit} = {formattedValue} {toUnit}"