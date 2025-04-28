from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
from unitflex.utils import debugLog
import warnings
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
    def convert(cls, value, fromUnit, toUnit, *, prec=None, format="tag", delim=False, mode="standard"):
        toUnit = toUnit.lower().strip()
        fromUnit = fromUnit.lower().strip()
        fromUnit = fromUnit.lower()
        toUnit = toUnit.lower()
        mode = mode.lower()
        debugLog(f"[convert] Started 'Temperature' conversion: {value} {fromUnit} to {toUnit}")

        if fromUnit not in cls.conversionToCelsius:
            debugLog(f"[convert] Error: From unit '{fromUnit}' not recognized!")
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionFromCelsius:
            debugLog(f"[convert] Error: From unit '{fromUnit}' not recognized!")
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
            debugLog(f"[convert] Error: mode='{mode}' is not recognized!")
            raise ValueError("Mode must be either 'standard' or 'engineering'.")
        debugLog(f"[convert] Parsed prec={prec}, mode={mode}")

        if mode == "standard" and prec > 6:
            warnings.warn("High precision requested in standard mode. Consider using engineering mode for better accuracy.")

        if mode == "engineering":
            debugLog(f"[convert] Engineering mode activated")
            getcontext().prec = prec + 5
            getcontext().rounding = ROUND_HALF_UP

            try:
                value = Decimal(str(value))
                celsiusValue = Decimal(str(cls.conversionToCelsius[fromUnit](value)))
                convertedValue = Decimal(str(cls.conversionFromCelsius[toUnit](celsiusValue)))

                digits = convertedValue.adjusted() + 1
                decimalPlaces = prec - digits

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
            return f"{formattedValue} °{toUnit}" if toUnit in {"c", "f", "k", "r", "re"} else f"{formattedValue} {toUnit}"
        elif format == "verbose":
            return f"{value} °{fromUnit} = {formattedValue} °{toUnit}" if toUnit in {"c", "f", "k", "r", "re"} else f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
