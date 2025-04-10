from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
import warnings
class timeConverter:
    conversionRates = {
        # Base unit: second (s)
        "s": "1", "sec": "1", "second": "1", "seconds": "1",

        # Millisecond and smaller
        "ms": "0.001", "millisecond": "0.001", "milliseconds": "0.001",
        "μs": "0.000001", "us": "0.000001", "microsecond": "0.000001", "microseconds": "0.000001",
        "ns": "0.000000001", "nanosecond": "0.000000001", "nanoseconds": "0.000000001",

        # Minute and larger
        "min": "60", "minute": "60", "minutes": "60",
        "h": "3600", "hr": "3600", "hour": "3600", "hours": "3600",
        "d": "86400", "day": "86400", "days": "86400",
        "w": "604800", "wk": "604800", "week": "604800", "weeks": "604800",
        "m": "2629800", "mo": "2629800", "month": "2629800", "months": "2629800",
        "y": "31557600", "yr": "31557600", "year": "31557600", "years": "31557600",

        # Additional variants
        "millis": "0.001", "micros": "0.000001", "nanos": "0.000000001",

        # Custom calendar-based terms
        "quarter": "7889400", "quarters": "7889400", "triwulan": "7889400",
        "semester": "15778800", "semesters": "15778800",
        "bimonth": "5259600", "bimonthly": "5259600",
        "trimester": "7889400", "trimesters": "7889400",
        "quadmester": "10505700", "quadmesters": "10505700",

        # Longer periods
        "decade": "315576000", "decades": "315576000", "dasawarsa": "315576000",
        "score": "631152000", "scores": "631152000",
        "generation": "946728000", "generations": "946728000",
        "century": "3155760000", "centuries": "3155760000",
        "millennium": "31557600000", "millennia": "31557600000",
        "windu": "252460800", "windus": "252460800",
        "lustrum": "157788000", "lustra": "157788000",
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, prec=None, format="tag", delim=False, mode="standard"):
        toUnit = toUnit.lower().strip()
        fromUnit = fromUnit.lower().strip()
        format = format.lower().strip()
        mode = mode.lower().strip()

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        if prec is None:
            prec = 9 if mode == "engineering" else 2
        elif int(prec) < 0:
            raise ValueError("Precision can't be negative!")
        else:
            try:
                prec = int(prec)
            except (ValueError, TypeError):
                raise ValueError("Precision must be a Number!")

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

                digits = convertedValue.adjusted() + 1 
                decimalPlaces = max(prec - digits, 0)

                if decimalPlaces > 0:
                    try:
                        quant = Decimal(f"1e-{decimalPlaces}")
                        finalValue = convertedValue.quantize(quant)
                    except InvalidOperation:
                        finalValue = convertedValue.normalize()
                else:
                    finalValue = convertedValue.to_integral_value(rounding=ROUND_HALF_UP)
            except (InvalidOperation, ValueError):
                raise ValueError("Conversion failed due to invalid decimal operation.")
        else:
            defaultValue = float(value) * float(cls.conversionRates[fromUnit])
            convertedValue = defaultValue / float(cls.conversionRates[toUnit])
            finalValue = round(convertedValue, prec)

        if isinstance(finalValue, (float, Decimal)) and finalValue == int(finalValue):
            finalValue = int(finalValue)

        if format == "raw":
            return finalValue

        separator = None
        if delim:
            if delim is True or str(delim).lower().strip() == "default":
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