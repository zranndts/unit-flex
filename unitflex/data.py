class dataConverter:
    conversionRates = {
        # Bit
        "bit": 1 / 8_000_000,
        "b": 1 / 8_000_000,
        
        # Byte
        "byte": 1 / 1_000_000,
        "bps": 1 / 1_000_000,

        # Kilobit
        "kbit": 1 / 8_000,
        "kbps": 1 / 8_000,

        # Kilobyte
        "kbyte": 0.001,
        "kb": 0.001,

        # Megabit
        "mbit": 0.125,
        "mbps": 0.125,

        # Megabyte (base unit)
        "mb": 1,
        "megabyte": 1,
        "mbyte": 1,

        # Gigabit
        "gbit": 125,
        "gbps": 125,

        # Gigabyte
        "gb": 1_000,
        "gigabyte": 1_000,
        "gbyte": 1_000,

        # Terabyte
        "tb": 1_000_000,
        "terabyte": 1_000_000,
        "tbyte": 1_000_000,

        # Petabyte
        "pb": 1_000_000_000,
        "petabyte": 1_000_000_000,
        "pbyte": 1_000_000_000,
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=8, format="compact"):
        fromUnit = fromUnit.lower()
        toUnit = toUnit.lower()

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        defaultValue = value * cls.conversionRates[fromUnit]
        convertedValue = defaultValue / cls.conversionRates[toUnit]

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
