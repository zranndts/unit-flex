from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
from unitflex.utils import debugLog
import warnings
class volumeConverter:
    conversionRates = {
    # Metric Units (SI)
    "nl": "1e-9", "nanoliter": "1e-9", "nanoliters": "1e-9",
    "µl": "1e-6", "μl": "1e-6", "microliter": "1e-6", "microliters": "1e-6",
    "ml": "1e-6", "milliliter": "1e-6", "milliliters": "1e-6",
    "cl": "1e-5", "centiliter": "1e-5", "centiliters": "1e-5",
    "dl": "1e-4", "deciliter": "1e-4", "deciliters": "1e-4",
    "dal": "1e-2", "dekaliter": "1e-2", "dekaliters": "1e-2",
    "l": "1e-3", "liter": "1e-3", "liters": "1e-3",
    "hl": "0.1", "hectoliter": "0.1", "hectoliters": "0.1",
    "m3": "1", "m³": "1", "cubic meter": "1", "cubic meters": "1",
    "cm3": "1e-6", "cm³": "1e-6", "cubic centimeter": "1e-6", "cubic centimeters": "1e-6", "cubic centimetre": "1e-6",
    "dm3": "1e-3", "dm³": "1e-3", "cubic decimeter": "1e-3", "cubic decimeters": "1e-3",
    "mm3": "1e-9", "mm³": "1e-9", "cubic millimeter": "1e-9", "cubic millimeters": "1e-9",
    "km3": "1e9", "km³": "1e9", "cubic kilometer": "1e9", "cubic kilometers": "1e9",

    # US Customary Units (based on NIST definitions)
    "tsp": "4.92892159375e-6", "teaspoon": "4.92892159375e-6", "teaspoons": "4.92892159375e-6",
    "tbsp": "1.478676478125e-5", "tablespoon": "1.478676478125e-5", "tablespoons": "1.478676478125e-5",
    "floz": "2.95735295625e-5", "fl oz": "2.95735295625e-5", "fluid ounce": "2.95735295625e-5", "fluid ounces": "2.95735295625e-5",
    "cup": "2.365882375e-4", "cups": "2.365882375e-4",
    "pt": "4.73176475e-4", "pint": "4.73176475e-4", "pints": "4.73176475e-4",
    "qt": "9.4635295e-4", "quart": "9.4635295e-4", "quarts": "9.4635295e-4",
    "gal": "3.785411784e-3", "us sgal": "3.785411784e-3", "gallon": "3.785411784e-3", "gallons": "3.785411784e-3",
    "in3": "1.6387064e-5", "in³": "1.6387064e-5", "cubic inch": "1.6387064e-5", "cubic inches": "1.6387064e-5",
    "ft3": "0.028316846592", "ft³": "0.028316846592", "cubic foot": "0.028316846592", "cubic feet": "0.028316846592",
    "yd3": "0.764554857984", "yd³": "0.764554857984", "cubic yard": "0.764554857984", "cubic yards": "0.764554857984",

    # UK Imperial Units
    "uk gal": "4.54609e-3", "uk-gal": "4.54609e-3", "gal-uk": "4.54609e-3", "imperial gallon": "4.54609e-3", "imperial gallons": "4.54609e-3",

    # Oil Barrel
    "bbl": "0.158987294928", "barrel": "0.158987294928", "barrels": "0.158987294928",
}

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, prec=None, format="tag", delim=False, mode="standard"):
        toUnit = toUnit.lower().strip()
        fromUnit = fromUnit.lower().strip()
        format = format.lower().strip()
        debugLog(f"[convert] Started 'Volume' conversion: {value} {fromUnit} to {toUnit}")

        if value < 0:
            debugLog(f"[convert] Error: value is negative! '{value}'")
            raise ValueError("'Mass' value cant't be negative!")
        elif value == 0:
            debugLog(f"[convert] Error: value is zero! '{value}'")
            raise ValueError("'Mass' value can't be zero!")

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