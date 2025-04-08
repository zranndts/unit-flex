from decimal import Decimal, getcontext, ROUND_HALF_UP
import warnings
class massConverter:
    conversionRates = {
        # Metric Units
        "mg": 1e-6, "milligram": 1e-6, "milligrams": 1e-6,
        "g": 1e-3, "gram": 1e-3, "grams": 1e-3,
        "kg": 1, "kilogram": 1, "kilograms": 1,
        "t": 1_000, "ton": 1_000, "tons": 1_000, "metricton": 1_000,
        "quintal": 100,
        "ons": 0.1, "ons-nl": 0.1,

        # Imperial/US Units
        "oz": 0.028_349_5, "ounce": 0.028_349_5, "ounces": 0.028_349_5,
        "lb": 0.453_592, "pound": 0.453_592, "pounds": 0.453_592,
        "st": 6.350_29, "stone": 6.350_29, "stones": 6.350_29,
        "slug": 14.593_9,
        "dram": 0.001_771_845_195_312_5, "dr": 0.001_771_845_195_312_5,

        # Smaller/Scientific Units
        "carat": 0.000_2,
        "grain": 0.000_064_798_91,

        # Ton variations
        "shortton": 907.184_74,
        "longton": 1_016.046_908_8,
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