from decimal import Decimal, getcontext, ROUND_HALF_UP
import warnings
class volumeConverter:

    conversionRates = {
        # Metric Units (SI)0
        "nl": 1e-9, "nanoliter": 1e-9, "nanoliters": 1e-9,
        "µl": 1e-6, "μl": 1e-6, "microliter": 1e-6, "microliters": 1e-6,
        "ml": 1e-6, "milliliter": 1e-6, "milliliters": 1e-6,
        "cl": 1e-5, "centiliter": 1e-5, "centiliters": 1e-5,
        "dl": 1e-4, "deciliter": 1e-4, "deciliters": 1e-4,
        "dal": 1e-2, "dekaliter": 1e-2, "dekaliters": 1e-2,
        "l": 1e-3, "liter": 1e-3, "liters": 1e-3,
        "hl": 0.1, "hectoliter": 0.1, "hectoliters": 0.1,
        "m3": 1, "m³": 1, "cubic meter": 1, "cubic meters": 1,
        "cm3": 1e-6, "cm³": 1e-6, "cubic centimeter": 1e-6, "cubic centimeters": 1e-6,"cubic centimetre": 1e-6,
        "dm3": 1e-3, "dm³": 1e-3, "cubic decimeter": 1e-3, "cubic decimeters": 1e-3,
        "mm3": 1e-9, "mm³": 1e-9, "cubic millimeter": 1e-9, "cubic millimeters": 1e-9,
        "km3": 1e9,  "km³": 1e9,  "cubic kilometer": 1e9, "cubic kilometer": 1e9,
        
        # Imperial / US Units
        "tsp": 4.92892e-6, "teaspoon": 4.92892e-6, "teaspoons": 4.92892e-6,
        "tbsp": 1.47868e-5, "tablespoon": 1.47868e-5, "tablespoons": 1.47868e-5,
        "floz": 2.95735e-5, "fl oz": 2.95735e-5, "fluid ounce": 2.95735e-5, "fluid ounces": 2.95735e-5,
        "cup": 2.36588e-4, "cups": 2.36588e-4,
        "pt": 4.73176e-4, "pint": 4.73176e-4, "pints": 4.73176e-4,
        "qt": 9.46353e-4, "quart": 9.46353e-4, "quarts": 9.46353e-4,
        "gal": 3.78541e-3, "gallon": 3.78541e-3, "gallons": 3.78541e-3,
        "in3": 1.63871e-5, "cubic inch": 1.63871e-5, "cubic inches": 1.63871e-5,
        "ft3": 0.0283168, "cubic foot": 0.0283168, "cubic feet": 0.0283168,
        "yd3": 0.764555, "cubic yard": 0.764555, "cubic yards": 0.764555,

        # UK-specific gallon
        "uk gal": 4.54609e-3, "imperial gallon": 4.54609e-3, "imperial gallons": 4.54609e-3,
        
        # Barrel (oil barrel, common in industry)
        "bbl": 0.158987, "barrel": 0.158987, "barrels": 0.158987,
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
                finalValue = convertedValue  #
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

