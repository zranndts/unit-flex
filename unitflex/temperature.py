from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
from unitflex.utils import debugLog
import warnings
class temperatureConverter:
    conversionToCelsius = {
        # Celcius (Base Unit)
        "c": lambda x: x, 
        "celsius": lambda x: x, 
        "celcius": lambda x: x, 
        "°c": lambda x: x,

        # Fahrenheit
        "f": lambda x: (x - Decimal('32')) * Decimal('5') / Decimal('9'),
        "fahrenheit": lambda x: (x - Decimal('32')) * Decimal('5') / Decimal('9'),
        "°f": lambda x: (x - Decimal('32')) * Decimal('5') / Decimal('9'),

        # Kelvin
        "k": lambda x: x - Decimal('273.15'),
        "kelvin": lambda x: x - Decimal('273.15'),
        "°k": lambda x: x - Decimal('273.15'),

        # Rankine
        "r": lambda x: (x - Decimal('491.67')) * Decimal('5') / Decimal('9'),
        "rankine": lambda x: (x - Decimal('491.67')) * Decimal('5') / Decimal('9'),
        "°r": lambda x: (x - Decimal('491.67')) * Decimal('5') / Decimal('9'),

        # Reaumur
        "re": lambda x: x * Decimal('5') / Decimal('4'),
        "reaumur": lambda x: x * Decimal('5') / Decimal('4'),
        "réaumur": lambda x: x * Decimal('5') / Decimal('4'),
        "°re": lambda x: x * Decimal('5') / Decimal('4'),
        "°ré": lambda x: x * Decimal('5') / Decimal('4')
    }

    conversionFromCelsius = {
        # Celcius (Base Unit)
        "c": lambda x: x, 
        "celsius": lambda x: x, 
        "celcius": lambda x: x, 
        "°c": lambda x: x,

        # Fahrenheit
        "f": lambda x: (x * Decimal('9') / Decimal('5')) + Decimal('32'),
        "fahrenheit": lambda x: (x * Decimal('9') / Decimal('5')) + Decimal('32'),
        "°f": lambda x: (x * Decimal('9') / Decimal('5')) + Decimal('32'),

        # Kelvin
        "k": lambda x: x + Decimal('273.15'),
        "kelvin": lambda x: x + Decimal('273.15'),
        "°k": lambda x: x + Decimal('273.15'),

        # Rankine
        "r": lambda x: (x + Decimal('273.15')) * Decimal('9') / Decimal('5'),
        "rankine": lambda x: (x + Decimal('273.15')) * Decimal('9') / Decimal('5'),
        "°r": lambda x: (x + Decimal('273.15')) * Decimal('9') / Decimal('5'),

        # Reaumur
        "re": lambda x: x * Decimal('4') / Decimal('5'),
        "reaumur": lambda x: x * Decimal('4') / Decimal('5'),
        "réaumur": lambda x: x * Decimal('4') / Decimal('5'),
        "°re": lambda x: x * Decimal('4') / Decimal('5'),
        "°ré": lambda x: x * Decimal('4') / Decimal('5')
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
        debugLog(f"[convert] Started 'Temperature' conversion: {value} {fromUnit} to {toUnit}")

        if fromUnit not in cls.conversionToCelsius:
            debugLog(f"[convert] Error: From unit '{fromUnit}' not recognized!")
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionFromCelsius:
            debugLog(f"[convert] Error: From unit '{fromUnit}' not recognized!")
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

        if mode == "standard" and precision > 6: warnings.warn("High precision requested in standard mode. Consider using engineering mode for better accuracy.")

        if mode in {"engineering", "eng", "e"}:
            debugLog(f"[convert] Engineering mode activated")
            getcontext().prec = precision + 5
            getcontext().rounding = ROUND_HALF_UP

            try:
                value = Decimal(str(value))
                celsiusValue = Decimal(str(cls.conversionToCelsius[fromUnit](value)))
                convertedValue = Decimal(str(cls.conversionFromCelsius[toUnit](celsiusValue)))

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
            celsiusValue = cls.conversionToCelsius[fromUnit](value)
            convertedValue = cls.conversionFromCelsius[toUnit](celsiusValue)
            finalValue = round(convertedValue, precision)

        if isinstance(finalValue, (float, Decimal)) and finalValue == int(finalValue):
            finalValue = int(finalValue)

        if format == "raw":
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
            return f"{formattedValue} °{toUnit}" if toUnit in {"c", "f", "k", "r", "re"} else f"{formattedValue} {toUnit}"
        elif format == "verbose":
            return f"{value} °{fromUnit} = {formattedValue} °{toUnit}" if toUnit in {"c", "f", "k", "r", "re"} else f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
