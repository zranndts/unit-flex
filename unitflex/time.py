class timeConverter:
    conversionRates = {
        # Base unit: second (s)
        "s": 1, "sec": 1, "second": 1, "seconds": 1,

        # Millisecond and smaller
        "ms": 1e-3, "millisecond": 1e-3, "milliseconds": 1e-3,
        "μs": 1e-6, "us": 1e-6, "microsecond": 1e-6, "microseconds": 1e-6,
        "ns": 1e-9, "nanosecond": 1e-9, "nanoseconds": 1e-9,

        # Minute and larger
        "min": 60, "minute": 60, "minutes": 60,
        "h": 3600, "hr": 3600, "hour": 3600, "hours": 3600,
        "d": 86400, "day": 86400, "days": 86400,
        "w": 604800, "wk": 604800, "week": 604800, "weeks": 604800,
        "m": 2629800, "mo": 2629800, "month": 2629800, "months": 2629800,
        "y": 31557600, "yr": 31557600, "year": 31557600, "years": 31557600,

        # Additional variants
        "millis": 1e-3, "micros": 1e-6, "nanos": 1e-9,

        # Custom calendar-based terms
        "quarter": 7889400, "quarters": 7889400, "triwulan": 7889400,
        "semester": 15778800, "semesters": 15778800,
        "bimonth": 5259600, "bimonthly": 5259600,
        "trimester": 7889400, "trimesters": 7889400,
        "quadmester": 10505700, "quadmesters": 10505700,

        # Longer periods
        "decade": 315576000, "decades": 315576000, "dasawarsa": 315576000,
        "score": 631152000, "scores": 631152000,
        "generation": 946728000, "generations": 946728000,
        "century": 3155760000, "centuries": 3155760000,
        "millennium": 31557600000, "millennia": 31557600000,
        "windu": 252460800, "windus": 252460800,
        "score": 631152000, "scores": 631152000,
        "lustrum": 157788000, "lustra": 157788000,
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=2, format="tag", delim=False):
        fromUnit = fromUnit.lower()
        toUnit = toUnit.lower()

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        baseValue = value * cls.conversionRates[fromUnit]
        convertedValue = baseValue / cls.conversionRates[toUnit]

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