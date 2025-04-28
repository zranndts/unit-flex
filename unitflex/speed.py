from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
from unitflex.utils import debugLog
import warnings
class speedConverter:
    conversionRates = {
        # Milimeter per second
        "mm/s": "0.001", "millimeter per second": "0.001", "millimeters per second": "0.001", "mm per second": "0.001",
        "mm/min": "0.000016666666666666666", "millimeter per minute": "0.000016666666666666666", "millimeters per minute": "0.000016666666666666666", "mm per minute": "0.000016666666666666666",

        # Centimeters per second
        "cm/s": "0.01", "centimeter per second": "0.01", "centimeters per second": "0.01", "cm per second": "0.01",

        # Centimeter per minute
        "cm/min": "0.00016666666666666666", "centimeter per minute": "0.00016666666666666666", "centimeters per minute": "0.00016666666666666666", "cm": "0.00016666666666666666",

        # Meters per second (base unit)
        "m/s": "1", "meter per second": "1", "meters per second": "1",

        # Meters per minute
        "m/min": "0.016666666666666666", "meter per minute": "0.016666666666666666", "meters per minute": "0.016666666666666666",

        # Kilometers per hour
        "km/h": "0.277778", "kph": "0.277778", "kilometer per hour": "0.277778", "kilometers per hour": "0.277778", "km per hour": "0.277778",
 
        # Miles per hour
        "mi/h": "0.44704", "mph": "0.44704", "mile per hour": "0.44704", "miles per hour": "0.44704",

        # Feet per second
        "ft/s": "0.3048", "fps": "0.3048", "foot per second": "0.3048", "feet per second": "0.3048",

        # Knots
        "kt": "0.514444", "knot": "0.514444", "knots": "0.514444", "kn": "0.514444",

        # Mach (at sea level)
        "mach": "340.29", "ma": "340.29",

        # Speed of light
        "c": "299792458", "speed of light": "299792458",

        # Inches per second
        "in/s": "0.0254", "inch per second": "0.0254", "inches per second": "0.0254",

        # Inches per minute
        "in/min": "0.0004233333333333333", "inch per minute": "0.0004233333333333333", "inches per minute": "0.0004233333333333333",
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, prec=None, format="tag", delim=False, mode="standard"):
        fromUnit = fromUnit.lower().strip()
        toUnit = toUnit.lower().strip()
        format = format.lower().strip()
        mode = mode.lower().strip()
        debugLog(f"[convert] Started 'Speed' conversion: {value} {fromUnit} to {toUnit}")

        if value < 0:
            debugLog(f"[convert] Error: value is negative! '{value}'")
            raise ValueError("'Speed` value cant't be negative!")
        elif value == 0:
            debugLog(f"[convert] Error: value is zero! '{value}'")
            raise ValueError("'Speed` value can't be zero!")

        if fromUnit not in cls.conversionRates:
            debugLog(f"[convert] Error: From unit '{fromUnit}' not recognized!")
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            debugLog(f"[convert] Error: From unit '{toUnit}' not recognized!")
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        if prec is None: prec = 9 if mode == "engineering" else 2
        elif int(prec) < 0: raise ValueError("Precision can't be negative!")
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
                fromFactor = Decimal(str(cls.conversionRates[fromUnit]))
                toFactor = Decimal(str(cls.conversionRates[toUnit]))

                defaultValue = value * fromFactor
                convertedValue = defaultValue / toFactor

                debugLog(f"[convert] Engineering mode: raw result={convertedValue}")

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
            defaultValue = float(value) * float(cls.conversionRates[fromUnit])
            convertedValue = defaultValue / float(cls.conversionRates[toUnit])
            finalValue = round(convertedValue, prec)
            debugLog(f"[convert] Standard mode: result={finalValue}")

        if isinstance(finalValue, (float, Decimal)) and finalValue == int(finalValue):
            finalValue = int(finalValue)

        if format == "raw":
            debugLog(f"[convert] Final output: {finalValue}")
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
            result = f"{formattedValue} {toUnit}"
        elif format == "verbose":
            result = f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
        debugLog(f"[convert] Final output: {result}")
        return result