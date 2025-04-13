from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
import warnings
class lengthConverter:
    conversionRates = {
        # Metric Units (SI)
        "pm": "1e-12", "picometer": "1e-12", "picometers": "1e-12",
        "nm": "1e-9", "nanometer": "1e-9", "nanometers": "1e-9",
        "µm": "1e-6", "um": "1e-6", "micrometer": "1e-6", "micrometers": "1e-6",
        "mm": "1e-3", "millimeter": "1e-3", "millimeters": "1e-3",
        "cm": "1e-2", "centimeter": "1e-2", "centimeters": "1e-2",
        "dm": "1e-1", "decimeter": "1e-1", "decimeters": "1e-1",
        "m": "1", "meter": "1", "meters": "1",
        "km": "1000", "kilometer": "1000", "kilometers": "1000",
        "angstrom": "1e-10", "Å": "1e-10",

        # Astronomical
        "ly": "9460730472580800", "lightyear": "9460730472580800", "lightyears": "9460730472580800",
        "au": "149597870700", "astronomicalunit":"149597870700", "astronomicalunits":"149597870700",
        "pc": "3.085677581491367e16", "parsec": "3.085677581491367e16", "parsecs": "3.085677581491367e16", 

        # Engineering
        "chain": "20.1168", "chains": "20.1168",
        "link": "0.201168", "links": "0.201168",
        "rod": "5.0292", "rods": "5.0292", "pole": "5.0292", "poles": "5.0292", "perch": "5.0292", "perches": "5.0292",
        "furlong": "201.168", "furlongs": "201.168",

        # Imperial / US Units
        "in": "0.0254", "inch": "0.0254", "inches": "0.0254",
        "ft": "0.3048", "foot": "0.3048", "feet": "0.3048",
        "yd": "0.9144", "yard": "0.9144", "yards": "0.9144",
        "mi": "1609.344", "mile": "1609.344", "miles": "1609.344",
        "nmi": "1852", "nauticalmile": "1852", "nauticalmiles": "1852",
        "mil": "0.0000254", "thou": "0.0000254",
        "league": "4_828.032", "leagues": "4_828.032",
        "hand": "0.1016", "hands": "0.1016",
        "barleycorn": "0.00847", "barleycorns": "0.00847",

        # Typographic
        "point": "0.000352778", "pt": "0.000352778","points": "0.000352778",
        "pica": "0.004233333", "picas": "0.004233333",

        # Microscopic
        "femtometer": "1e-15", "fermi": "1e-15"
    }

    sensitiveUnits = {"pc", "parsec", "femtometer", "fm", "fermi", "ly", "lightyear"}

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, prec=None, format="tag", delim=False, mode="standard"):
        toUnit = toUnit.lower().strip()
        fromUnit = fromUnit.lower().strip()
        format = format.lower().strip()
        mode = mode.lower().strip()

        if value < 0:raise ValueError("'Length` value cant't be negative!")
        elif value == 0:raise ValueError("'Length` value can't be zero!")

        if mode == "standard" and (fromUnit in cls.sensitiveUnits or toUnit in cls.sensitiveUnits):
            warnings.warn(f"Unit '{fromUnit}' or '{toUnit}' is highly sensitive! Consider using engineering mode for better accuracy.")

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
