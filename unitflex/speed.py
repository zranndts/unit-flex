from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
import warnings
class speedConverter:
    conversionRates = {
        # Milimeter per second
        "mm/s": "0.001", "millimeter per second": "0.001", "millimeters per second": "0.001", "mm per second": "0.001",
        "Mm/s": "0.001", "MM/s": "0.001", "Millimeter per second": "0.001", "Millimeters per second": "0.001", "Mm per second": "0.001", "MM per second": "0.001",

        "mm/min": "0.000016666666666666666", "millimeter per minute": "0.000016666666666666666", "millimeters per minute": "0.000016666666666666666", "mm per minute": "0.000016666666666666666",
        "Mm/min": "0.000016666666666666666", "MM/min": "0.000016666666666666666", "MM per minute": "0.000016666666666666666", "Millimeter per minute": "0.000016666666666666666", "Millimeters per minute": "0.000016666666666666666",

        # Centimeters per second
        "cm/s": "0.01", "centimeter per second": "0.01", "centimeters per second": "0.01", "cm per second": "0.01",
        "Cm/s": "0.01", "CM/s": "0.01", "Centimeter per second": "0.01", "Centimeters per second": "0.01", "Cm per second": "0.01", "CM per second": "0.01",

        # Centimeter per minute
        "cm/min": "0.00016666666666666666", "centimeter per minute": "0.00016666666666666666", "centimeters per minute": "0.00016666666666666666", "cm": "0.00016666666666666666",
        "Cm/min": "0.00016666666666666666", "CM/min": "0.00016666666666666666", "Centimeter per minute": "0.00016666666666666666", "Centimeters per minute": "0.00016666666666666666", "CM per minute": "0.00016666666666666666",

        # Meters per second (base unit)
        "m/s": "1", "meter per second": "1", "meters per second": "1",
        "M/S": "1", "Meter per Second": "1", "Meters per Second": "1",

        # Meters per minute
        "m/min": "0.016666666666666666", "meter per minute": "0.016666666666666666", "meters per minute": "0.016666666666666666",
        "M/min": "0.016666666666666666", "Meter per minute": "0.016666666666666666", "Meters per minute": "0.016666666666666666",

        # Kilometers per hour
        "km/h": "0.277778", "kph": "0.277778", "kilometer per hour": "0.277778", "kilometers per hour": "0.277778", "km per hour": "0.277778",
        "KM/H": "0.277778", "KPH": "0.277778", "Kilometer per Hour": "0.277778", "Kilometers per Hour": "0.277778", "Km per hour": "0.277778",

        # Miles per hour
        "mi/h": "0.44704", "mph": "0.44704", "mile per hour": "0.44704", "miles per hour": "0.44704",
        "MI/H": "0.44704", "MPH": "0.44704", "Mile per Hour": "0.44704", "Miles per Hour": "0.44704",

        # Feet per second
        "ft/s": "0.3048", "fps": "0.3048", "foot per second": "0.3048", "feet per second": "0.3048",
        "FT/S": "0.3048", "FPS": "0.3048", "Foot per Second": "0.3048", "Feet per Second": "0.3048",

        # Knots
        "kt": "0.514444", "knot": "0.514444", "knots": "0.514444", "kn": "0.514444",
        "KT": "0.514444", "Knot": "0.514444", "Knots": "0.514444", "KN": "0.514444",

        # Mach (at sea level)
        "mach": "340.29", "Mach": "340.29", "Ma": "340.29", "ma": "340.29",

        # Speed of light
        "c": "299792458", "C": "299792458", "speed of light": "299792458", "Speed of Light": "299792458",

        # Inches per second
        "in/s": "0.0254", "inch per second": "0.0254", "inches per second": "0.0254",
        "IN/S": "0.0254", "Inch per Second": "0.0254", "Inches per Second": "0.0254",

        # Inches per minute
        "in/min": "0.0004233333333333333", "inch per minute": "0.0004233333333333333", "inches per minute": "0.0004233333333333333",
        "In/min": "0.0004233333333333333", "Inch per minute": "0.0004233333333333333", "Inches per minute": "0.0004233333333333333",
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, prec=None, format="tag", delim=False, mode="standard"):
        format = format.lower().strip()
        mode = mode.lower().strip()

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