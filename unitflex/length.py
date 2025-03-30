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
    def convert(cls, value, fromUnit, toUnit, precision=2, format="compact"):
        fromUnit = fromUnit.lower()
        toUnit = toUnit.lower()

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        defaultValue = value * cls.conversionRates[fromUnit]
        convertedValue = defaultValue / cls.conversionRates[toUnit]

        if int(precision) < 0:
            raise ValueError("Precision can't be negative!")

        validationFormatting = {"raw", "compact", "verbose"}
        if format not in validationFormatting:
            raise ValueError(f"Output format '{format}' not recognized! Choose from: {', '.join(validationFormatting)}")

        if format == "raw":
            return f"{round(convertedValue, int(precision))}"
        elif format == "compact":
            return f"{round(convertedValue, int(precision))} {toUnit}"
        elif format == "verbose":
            return f"{value} {fromUnit} = {round(convertedValue, int(precision))} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
