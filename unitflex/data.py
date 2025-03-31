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
        "kilobit": 1 / 8_000,
        "kbps": 1 / 8_000,

        # Kilobyte
        "kbyte": 0.001,
        "kilobyte": 0.001,
        "kb": 0.001,

        # Megabit
        "mbit": 0.125,
        "megabit": 0.125,
        "mbps": 0.125,

        # Megabyte (base unit)
        "mb": 1,
        "megabyte": 1,
        "mbyte": 1,

        # Gigabit
        "gbit": 125,
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
