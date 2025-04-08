from decimal import Decimal, getcontext, ROUND_HALF_UP
import warnings
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
    def convert(cls, value, fromUnit, toUnit, *, prec=2, format="tag", delim=False, mode="standard"):
        toUnit = toUnit.lower().strip()
        fromUnit = fromUnit.lower().strip()
        format = format.lower().strip()
        mode = mode.lower().strip()

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        try:
            prec = int(prec)
        except (ValueError, TypeError):
            raise ValueError("Precision must be an integer!")

        if prec < 0:
            raise ValueError("Precision can't be negative!")

        if mode not in ("standard", "engineering"):
            raise ValueError("Mode must be either 'standard' or 'engineering'.")

        if mode == "standard" and prec > 6:
            warnings.warn("High precision requested in standard mode. Consider using engineering mode for better accuracy.")

        if mode == "engineering":
            getcontext().prec = prec + 5
            getcontext().rounding = ROUND_HALF_UP

            try:
                value = Decimal(str(value))
                fromFactor = Decimal(str(cls.conversionRates[fromUnit]))
                toFactor = Decimal(str(cls.conversionRates[toUnit]))

                defaultValue = value * fromFactor
                convertedValue = defaultValue / toFactor

                if convertedValue == convertedValue.to_integral():
                    finalValue = convertedValue
                else:
                    quant = Decimal(f"1e-{prec}")
                    finalValue = convertedValue.quantize(quant)
            except (InvalidOperation, ValueError):
                finalValue = convertedValue
        else:
            defaultValue = value * cls.conversionRates[fromUnit]
            convertedValue = defaultValue / cls.conversionRates[toUnit]
            finalValue = round(convertedValue, prec)

        if isinstance(finalValue, (float, Decimal)) and finalValue == int(finalValue):
            finalValue = int(finalValue)

        if format == "raw":
            return finalValue

        separator = None
        if delim:
            if delim is True or str(delim).lower() == "default":
                separator = ","
            else:
                separator = str(delim)

        if isinstance(finalValue, int):
            formattedValue = f"{finalValue:,}" if separator else str(finalValue)
        else:
            formattedValue = f"{finalValue:,.{prec}f}" if separator else f"{finalValue:.{prec}f}"

        if separator:
            formattedValue = formattedValue.replace(",", separator)

        if format == "tag":
            return f"{formattedValue} {toUnit}"
        elif format == "verbose":
            return f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")