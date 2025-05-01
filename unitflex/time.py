from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
from unitflex.utils import debugLog
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
        "millennium": "31557600000", "millennia": "31557600000", "milenium": "31557600000", "millenium": "31557600000",
        "windu": "252460800", "windus": "252460800",
        "lustrum": "157788000", "lustra": "157788000",
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, precision=None, format="raw", delimiter=False, mode="standard", **kwargs):
        aliasesMap = {
        'precision': ['precision', 'prec', 'p'],
        'format': ['format', 'fmt', 'f'],
        'delimiter': ['delimiter', 'delim', 'de'],
        'mode': ['mode', 'm']
        }

        def getParameter(default, parameterName):
            aliases = aliasesMap.get(parameterName, [])
            for alias in aliases:
                if alias in kwargs:
                    return kwargs[alias]
            return default
            
        precision = getParameter(precision, 'precision')
        format = getParameter(format, 'format')
        delimiter = getParameter(delimiter, 'delimiter')
        mode = getParameter(mode, 'mode')

        toUnit = toUnit.lower().strip()
        fromUnit = fromUnit.lower().strip()
        format = format.lower().strip() if isinstance(format, str) else format
        mode = mode.lower().strip() if isinstance(mode, str) else mode
        debugLog(f"[convert] Started 'Time' conversion: {value} {fromUnit} to {toUnit}")

        if value < 0:
            debugLog(f"[convert] Error: value is negative! '{value}")
            raise ValueError("'Time` value cant't be negative!") 
        elif value == 0:
            debugLog(f"[convert] Error: value is zero '{value}'")
            raise ValueError("'Time` value can't be zero!")

        if fromUnit not in cls.conversionRates:
            debugLog(f"[convert] Error: From unit '{fromUnit}' not recognized!")
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            debugLog(f"[convert] Error: To unit '{toUnit}' not recognized!")
            raise ValueError(f"To unit '{toUnit}' not recognized!")
        
        precision = 9 if precision is None and mode in {"engineering", "eng", "e"} else 2 if precision is None else precision
        if int(precision) < 0: raise ValueError("Precision can't be negative!")
        else:
            try:
                precision = int(precision)
            except (ValueError, TypeError):
                raise ValueError("Precision must be a Number!")

        if mode not in {"standard", "engineering", "eng", "e"}:
            debugLog(f"[convert] Error: mode='{mode}' is not recognized!")
            raise ValueError("Mode must be either 'standard' or 'engineering'.")
        
        debugLog(f"[convert] Parsed prec={precision}, mode={mode}")
          
        if mode == "standard" and precision > 6:
            warnings.warn("High precision requested in standard mode. Consider using engineering mode for better accuracy.")

        if mode in {"engineering", "eng", "e"}:
            debugLog(f"[convert] Engineering mode activated")
            getcontext().prec = precision + 5
            getcontext().rounding = ROUND_HALF_UP

            try:
                value = Decimal(str(value))
                fromFactor = Decimal(str(cls.conversionRates[fromUnit]))
                toFactor = Decimal(str(cls.conversionRates[toUnit]))

                defaultValue = value * fromFactor
                convertedValue = defaultValue / toFactor

                debugLog(f"[convert] Engineering mode: raw result={convertedValue}")

                digits = convertedValue.adjusted() + 1
                decimalPlaces = precision - digits

                if decimalPlaces >= 0 and decimalPlaces <= 50:
                    try:
                        quant = Decimal(f"1e-{decimalPlaces}")
                        finalValue = convertedValue.quantize(quant, rounding=ROUND_HALF_UP)
                    except (InvalidOperation, ValueError) as e:
                        debugLog(f"[convert] Quantize fallback triggered: {e}")
                        finalValue = convertedValue.normalize()
                else:
                    debugLog(f"[convert] Skipping quantize due to extreme decimalPlaces={decimalPlaces}")
                    finalValue = convertedValue.normalize()

                debugLog(f"[convert] Final output: {finalValue}")
            except (InvalidOperation, ValueError) as e:
                debugLog(f"[convert] Decimal error: {e}")
                raise ValueError("Conversion failed due to invalid decimal operation.")
        else:
            defaultValue = float(value) * float(cls.conversionRates[fromUnit])
            convertedValue = defaultValue / float(cls.conversionRates[toUnit])
            finalValue = round(convertedValue, precision)
            debugLog(f"[convert] Standard mode: result={finalValue}")

        if isinstance(finalValue, (float, Decimal)) and finalValue == int(finalValue):
            finalValue = int(finalValue)
            
        if format == "raw":
            debugLog(f"[convert] Final output: {finalValue}")
            return finalValue

        separator = None
        if delimiter:
            if delimiter is True or str(delimiter).lower().strip() == "default":
                separator = ","
            else:
                separator = str(delimiter)

        if isinstance(finalValue, int):
            formattedValue = f"{finalValue:,}" if separator else str(finalValue)
        else:
            formattedValue = f"{finalValue:,.{precision}f}" if separator else f"{finalValue:.{precision}f}"

        if separator:
            formattedValue = formattedValue.replace(",", separator)

        if format == "tag":
            result = f"{formattedValue} {toUnit}"
        elif format == "verbose":
            result = f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
        debugLog(f"[convert] Final output: {result}")
        return result
    
    @classmethod
    def flex(cls, value, fromUnit, *, flexRange=(None, None), delim=True):
        getcontext().prec = 10

        if value < 0:raise ValueError("'Time` value can't be negative!")
        elif value == 0:raise ValueError("'Time` value can't be zero!")
        
        validUnitsOrdered = [
            "millennium", "century", "decade", "year", "month", "week",
            "day", "hour", "minute", "second"
        ]

        lowerBound, upperBound = flexRange

        try:
            startIndex = validUnitsOrdered.index(lowerBound) if lowerBound else 0
            endIndex = validUnitsOrdered.index(upperBound) if upperBound else len(validUnitsOrdered) - 1
        except ValueError:
            raise ValueError(f"Invalid unit in flexRange: {flexRange}")

        if startIndex > endIndex:
            raise ValueError("Invalid flexRange: lower bound must be larger unit than upper bound")

        allowedUnits = validUnitsOrdered[startIndex:endIndex + 1]

        try:
            value = str(value)
            baseSeconds = Decimal(value) * Decimal(cls.conversionRates[fromUnit])
        except KeyError:
            raise ValueError(f"Unit '{fromUnit}' not recognized for flex conversion.")
        except Exception as e:
            debugLog(f"[flex] Error: {e}")
            raise ValueError(f"Invalid input value for conversion: {value!r}") from e

        orderedUnits = []
        for u in validUnitsOrdered:
            if u in allowedUnits:
                for key, rate in cls.conversionRates.items():
                    if key.lower() == u:
                        orderedUnits.append((u, Decimal(rate)))
                        break

        result = []
        remaining = baseSeconds

        for unitName, unitSeconds in orderedUnits:
            count = remaining // unitSeconds
            if count > 0:
                countStr = f"{int(count):,}" if delim else str(int(count))
                result.append(f"{countStr} {unitName}{'s' if int(count) != 1 else ''}")
                remaining -= count * unitSeconds

            if remaining < Decimal("0.0001"):
                break

        if not result:
            result.append("0 second")

        final = " ".join(result)
        debugLog(f"[flex] Output: {final}")
        return final