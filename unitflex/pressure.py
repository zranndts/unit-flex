from decimal import Decimal, getcontext, ROUND_HALF_UP
import warnings
class pressureConverter:
    conversionRates = {
        # SI Units
        "pa": 1, "pascal": 1, "pascals": 1,

        # Metric multiples
        "kpa": 1e3, "kilopascal": 1e3, "kilopascals": 1e3,
        "kpa": 1e3, "kilopascal": 1e3, "kilopascals": 1e3,
        "mpa": 1e6, "megapascal": 1e6, "megapascals": 1e6,
        "gpa": 1e9, "gigapascal": 1e9, "gigapascals": 1e9,
        "hpa": 100, "hectopascal": 100, "hectopascals": 100,

        # Bar units
        "bar": 1e5, "bars": 1e5,
        "mbar": 1e2, "millibar": 1e2, "millibars": 1e2,

        # Atmosphere
        "atm": 101325, "atmosphere": 101325, "atmospheres": 101325,

        # Torr / mmHg
        "torr": 133.322, "mmhg": 133.322, "mmHg": 133.322, "millimeter of mercury": 133.322, "millimeters of mercury": 133.322,

        # Inches of Mercury
        "inhg": 3386.39, "inch of mercury": 3386.39, "Inch of mercury": 3386.39,
        "inHg": 3386.39, "inches of mercury": 3386.39, "Inches of mercury": 3386.39,

        # Per Square Inch
        "psi": 6894.76, "pound per square inch": 6894.76, "pounds per square inch": 6894.76,
        "ksi": 6_894_760, "kip per square inch": 6_894_760, "kips per square inch": 6_894_760,
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