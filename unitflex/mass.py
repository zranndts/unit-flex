class massConverter:
    conversionRates = {
        "kg": 1,
        "g": 0.001,
        "mg": 0.000001,
        "ton": 1000,
        "lb": 0.453592,
        "oz": 0.0283495,
        "st": 6.35029
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, precision=2):
        fromUnit = fromUnit.lower()
        toUnit = toUnit.lower()

        if fromUnit not in cls.conversionRates:
            raise ValueError(f"Satuan asal '{fromUnit}' tidak dikenali.")
        if toUnit not in cls.conversionRates:
            raise ValueError(f"Satuan tujuan '{toUnit}' tidak dikenali.")

        defaultValue = value * cls.conversionRates[fromUnit]
        convertedValue = defaultValue / cls.conversionRates[toUnit]

        if int(precision) < 0:
            raise ValueError("Precision tidak boleh negatif.")

        return round(convertedValue, precision)