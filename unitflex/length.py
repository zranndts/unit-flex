from decimal import Decimal, getcontext, ROUND_HALF_UP
import warnings
class lengthConverter:
    conversionRates = {
        # Metric Units (SI)
        "pm": 1e-12, "picometer": 1e-12, "picometers": 1e-12,
        "nm": 1e-9, "nanometer": 1e-9, "nanometers": 1e-9,
        "µm": 1e-6, "um": 1e-6, "micrometer": 1e-6, "micrometers": 1e-6,
        "mm": 1e-3, "millimeter": 1e-3, "millimeters": 1e-3,
        "cm": 1e-2, "centimeter": 1e-2, "centimeters": 1e-2,
        "dm": 1e-1, "decimeter": 1e-1, "decimeters": 1e-1,
        "m": 1, "meter": 1, "meters": 1,
        "km": 1_000, "kilometer": 1_000, "kilometers": 1_000,
        "angstrom": 1e-10, "Å": 1e-10,

        # Imperial / US Units
        "in": 0.0254, "inch": 0.0254, "inches": 0.0254,
        "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
        "yd": 0.9144, "yard": 0.9144, "yards": 0.9144,
        "mi": 1_609.344, "mile": 1_609.344, "miles": 1_609.344,
        "nmi": 1_852, "nauticalmile": 1_852, "nauticalmiles": 1_852,
        "mil": 0.0000254, "thou": 0.0000254,
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
