class dataConverter:
    conversionRates = {
        # Bit
        "bit": 1 / 8_000_000, "Bit": 1 / 8_000_000, "bits": 1 / 8_000_000, "Bits": 1 / 8_000_000,
        "b": 1 / 8_000_000, "Bps": 1 / 8_000_000, "bps": 1 / 8_000_000,

        # Byte
        "byte": 1 / 1_000_000, "Byte": 1 / 1_000_000, "bytes": 1 / 1_000_000, "Bytes": 1 / 1_000_000,

        # Kilobit
        "kilobit": 1 / 8_000, "Kilobit": 1 / 8_000, "kilobits": 1 / 8_000, "Kilobits": 1 / 8_000,
        "kbit": 1 / 8_000, "Kbit": 1 / 8_000, "kbps": 1 / 8_000, "Kbps": 1 / 8_000,

        # Kilobyte
        "kilobyte": 0.001, "Kilobyte": 0.001, "kilobytes": 0.001, "Kilobytes": 0.001,
        "kbyte": 0.001, "Kbyte": 0.001, "kb": 0.001, "KB": 0.001, "KBps": 0.001,

        # Megabit
        "megabit": 0.125, "Megabit": 0.125, "megabits": 0.125, "Megabits": 0.125,
        "mbit": 0.125, "Mbit": 0.125, "mbps": 0.125, "Mbps": 0.125,

        # Megabyte (Base Unit)
        "megabyte": 1, "Megabyte": 1, "megabytes": 1, "Megabytes": 1,
        "mbyte": 1, "Mbyte": 1, "mb": 1, "MB": 1, "MBps": 1,

        # Gigabit
        "gigabit": 125, "Gigabit": 125, "gigabits": 125, "Gigabits": 125,
        "gbit": 125, "Gbit": 125, "gbps": 125, "Gbps": 125,

        # Gigabyte
        "gigabyte": 1_000, "Gigabyte": 1_000, "gigabytes": 1_000, "Gigabytes": 1_000,
        "gbyte": 1_000, "Gbyte": 1_000, "gb": 1_000, "GB": 1_000, "GBps": 1_000,

        # Terabit
        "terabit": 125_000, "Terabit": 125_000, "terabits": 125_000, "Terabits": 125_000,
        "tbit": 125_000, "Tbit": 125_000, "tbps": 125_000, "Tbps": 125_000,

        # Terabyte
        "terabyte": 1_000_000, "Terabyte": 1_000_000, "terabytes": 1_000_000, "Terabytes": 1_000_000,
        "tbyte": 1_000_000, "Tbyte": 1_000_000, "tb": 1_000_000, "TB": 1_000_000, "TBps": 1_000_000,

        # Petabit
        "petabit": 125_000_000, "Petabit": 125_000_000, "petabits": 125_000_000, "Petabits": 125_000_000,
        "pbit": 125_000_000, "Pbit": 125_000_000, "pbps": 125_000_000, "Pbps": 125_000_000,

        # Petabyte
        "petabyte": 1_000_000_000, "Petabyte": 1_000_000_000, "petabytes": 1_000_000_000, "Petabytes": 1_000_000_000,
        "pbyte": 1_000_000_000, "Pbyte": 1_000_000_000, "pb": 1_000_000_000, "PB": 1_000_000_000, "PBps": 1_000_000_000,
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=2, format="tag", delim=False):

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