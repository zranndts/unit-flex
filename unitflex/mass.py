from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
from unitflex.utils import debugLog
import warnings
class massConverter:
    conversionRates = {
        # Metric Units
        "mg": "1e-6", "milligram": "1e-6", "milligrams": "1e-6",
        "g": "1e-3", "gram": "1e-3", "grams": "1e-3",
        "kg": "1", "kilogram": "1", "kilograms": "1",
        "t": "1000", "ton": "1000", "tons": "1000", "metricton": "1000",
        "quintal": "100",
        "ons": "0.1", "ons-nl": "0.1",

        # Imperial/US Units
        "oz": "0.028349523125", "ounce": "0.028349523125", "ounces": "0.028349523125",
        "lb": "0.45359237", "pound": "0.45359237", "pounds": "0.45359237",
        "st": "6.35029318", "stone": "6.35029318", "stones": "6.35029318",
        "slug": "14.593903",
        "dram": "0.0017718451953125", "dr": "0.0017718451953125", "drams": "0.0017718451953125",

        # Smaller/Scientific Units
        "carat": "0.0002", "carats": "0.0002",
        "grain": "0.00006479891", "grains": "0.00006479891",

        # Ton variations
        "shortton": "907.18474",
        "longton": "1016.0469088",

        # Astronomical Units
        "solarmass": "1.988409870698051e30", "solar-mass": "1.988409870698051e30", "M☉": "1.988409870698051e30",
        "earthmass": "5.972168e24", "earth-mass": "5.972168e24", "M⊕": "5.972168e24",
        "lunarmass": "7.342e22", "lunar-mass": "7.342e22", "M☾": "7.342e22",
        "jupitermass": "1.89813e27", "jupiter-mass": "1.89813e27", "Mj": "1.89813e27", "M♃": "1.89813e27",
        "saturnmass": "5.6834e26", "saturn-mass": "5.6834e26", "Msat": "5.6834e26", "M♄": "5.6834e26",
        "uranusmass": "8.6810e25", "uranus-mass": "8.6810e25", "Mura": "8.6810e25",
        "neptunemass": "1.02413e26", "neptune-mass": "1.02413e26", "Mnep": "1.02413e26",
        "venusmass": "4.8675e24", "venus-mass": "4.8675e24", "Mven": "4.8675e24",
        "marsmass": "6.4171e23", "mars-mass": "6.4171e23", "Mmars": "6.4171e23",
        "mercurymass": "3.3011e23", "mercury-mass": "3.3011e23", "Mmer": "3.3011e23",
        "plutomass": "1.303e22", "pluto-mass": "1.303e22", "Mplu": "1.303e22",
        "ceresmass": "9.393e20", "ceres-mass": "9.393e20", "Mcer": "9.393e20",

        # Atomic / Microscopic Units
        "amu": "1.66053906660e-27", "atomicmassunit": "1.66053906660e-27",
        "atomic-mass-unit": "1.66053906660e-27", "atomic mass unit": "1.66053906660e-27",
        "dalton": "1.66053906660e-27", "Da": "1.66053906660e-27", "u": "1.66053906660e-27",
        "planckmass": "2.176434e-8", "planck-mass": "2.176434e-8",
        "planck mass": "2.176434e-8", "m_p": "2.176434e-8",

        # Quantum Physics Units
        "ev/c^2": "1.78266192e-36", "ev/c2": "1.78266192e-36", "ev/c²": "1.78266192e-36",
        "electronvoltpercsquared": "1.78266192e-36", "electron-volt-per-c-squared": "1.78266192e-36",
        "electron volt per c squared": "1.78266192e-36", "electron volt/c^2": "1.78266192e-36",
        "electron volt/c2": "1.78266192e-36", "eV/c^2": "1.78266192e-36", "eV/c2": "1.78266192e-36",

        # Obsolete / Regional Units
        "bale": "217.72", "bale-cotton": "217.72", "bale_cotton": "217.72",
        "bale-wool": "204", "bale_wool": "204",
        "bale-uk": "226.8", "bale_uk": "226.8", "bale-aus": "204", "bale_aus": "204",
        "mark": "0.25", "mark-de": "0.25", "mark_de": "0.25",
        "mark-no": "0.213", "mark_no": "0.213",
        "arroba": "11.5", "arroba-es": "11.5", "arroba_es": "11.5",
        "arrobas": "15", "arroba-pt": "15", "arroba_pt": "15"
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, prec=None, format="tag", delim=False, mode="standard"):
        toUnit = toUnit.lower().strip()
        fromUnit = fromUnit.lower().strip()
        format = format.lower().strip()
        debugLog(f"[convert] Started 'Mass' conversion: {value} {fromUnit} to {toUnit}")

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