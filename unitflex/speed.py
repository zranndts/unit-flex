class speedConverter:
    conversionRates = {
        # Milimeter per second
        "mm/s": 0.001, "millimeter per second": 0.001, "millimeters per second": 0.001, "mm per second": 0.001,
        "Mm/s": 0.001, "MM/s": 0.001, "Millimeter per second": 0.001, "Millimeters per second": 0.001, "Mm per second": 0.001, "MM per second": 0.001,

        "mm/min": 0.001 / 60, "millimeter per minute": 0.001 / 60, "millimeters per minute": 0.001 / 60, "mm per minute": 0.001 / 60,
        "Mm/min": 0.001 / 60, "MM/min": 0.001 / 60, "millimeter per minute": 0.001 / 60, "millimeters per minute": 0.001 / 60, "MM per minute": 0.001 / 60,

        # Centimeters per second
        "cm/s": 0.01, "centimeter per second": 0.01, "centimeters per second": 0.01, "cm per second": 0.01,
        "Cm/s": 0.01, "CM/s": 0.01, "Centimeter per second": 0.01, "Centimeters per second": 0.01, "Cm per second": 0.01, "CM per second": 0.01,

        # Centimeter per minute
        "cm/min": 0.01 / 60, "centimeter per minute": 0.01 / 60, "centimeters per minute": 0.01 / 60, "cm": 0.01 / 60,
        "Cm/min": 0.01 / 60, "CM/min": 0.01 / 60, "Centimeter per minute": 0.01 / 60, "Centimeters per minute": 0.01 / 60, "CM per minute": 0.01 / 60,

        # Meters per second (base unit)
        "m/s": 1, "meter per second": 1, "meters per second": 1,
        "M/S": 1, "Meter per Second": 1, "Meters per Second": 1,

        # Meters per minute
        "m/min": 1 / 60, "meter per minute": 1 / 60, "meters per minute": 1 / 60,
        "M/min": 1 / 60, "Meter per minute": 1 / 60, "Meters per minute": 1 / 60,

        # Kilometers per hour
        "km/h": 0.277778, "kph": 0.277778, "kilometer per hour": 0.277778, "kilometers per hour": 0.277778, "km per hour": 0.277778,
        "KM/H": 0.277778, "KPH": 0.277778, "Kilometer per Hour": 0.277778, "Kilometers per Hour": 0.277778, "Km per hour": 0.277778,

        # Miles per hour
        "mi/h": 0.44704, "mph": 0.44704, "mile per hour": 0.44704, "miles per hour": 0.44704,
        "MI/H": 0.44704, "MPH": 0.44704, "Mile per Hour": 0.44704, "Miles per Hour": 0.44704,

        # Feet per second
        "ft/s": 0.3048, "fps": 0.3048, "foot per second": 0.3048, "feet per second": 0.3048,
        "FT/S": 0.3048, "FPS": 0.3048, "Foot per Second": 0.3048, "Feet per Second": 0.3048,

        # Knots
        "kt": 0.514444, "knot": 0.514444, "knots": 0.514444, "kn": 0.514444,
        "KT": 0.514444, "Knot": 0.514444, "Knots": 0.514444, "KN": 0.514444,

        # Mach (at sea level, ~340.29 m/s)
        "mach": 340.29, "Mach": 340.29, "Ma": 340.29, "ma": 340.29,

        # Speed of light
        "c": 299_792_458, "C": 299_792_458, "speed of light": 299_792_458, "Speed of Light": 299_792_458,

        # Inches per second
        "in/s": 0.0254, "inch per second": 0.0254, "inches per second": 0.0254,
        "IN/S": 0.0254, "Inch per Second": 0.0254, "Inches per Second": 0.0254,

        # Inches per minute
        "in/min": 0.0254 / 60, "inch per minute": 0.0254 / 60, "inches per minute": 0.0254 / 60,
        "In/min": 0.0254 / 60, "Inch per minute": 0.0254 / 60, "Inches per minute": 0.0254 / 60,
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=2, format="tag", delim=False):

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        defaultValue = value * cls.conversionRates[fromUnit]
        convertedValue = defaultValue / cls.conversionRates[toUnit]

        if int(precision) < 0:
            raise ValueError("Precision can't be negative!")

        roundedValue = round(convertedValue, int(precision))
        if roundedValue == int(roundedValue):
            roundedValue = int(roundedValue)

        if format == "raw":
            return roundedValue

        if roundedValue == int(roundedValue):
            if delim:
                separator = "_" if delim is True or str(delim).lower().strip() == "default" else str(delim)
                formattedValue = f"{int(roundedValue):,}".replace(",", separator)
            else:
                formattedValue = str(int(roundedValue))
        else:
            if delim:
                separator = "_" if delim is True or str(delim).lower().strip() == "default" else str(delim)
                formattedValue = f"{roundedValue:,.{precision}f}".replace(",", separator)
            else:
                formattedValue = f"{roundedValue:.{precision}f}"

        if format == "tag":
            return f"{formattedValue} {toUnit}"
        elif format == "verbose":
            return f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
