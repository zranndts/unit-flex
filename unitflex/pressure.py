from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
from unitflex.utils import debugLog
import warnings
import re

def normalizePressureUnit(unit: str) -> str:
    unit = unit.strip().lower()
    unit = re.sub(r'[^a-z0-9]+', '/', unit)          
    unit = re.sub(r'/+', '/', unit)                  
    unit = unit.replace("per", "/").replace("square", "")
    unit = unit.replace(" ", "")

    return unit

class pressureConverter:
    conversionRates = {
        # SI Units
        "pa": "1", "pascal": "1", "pascals": "1",

        # Metric multiples
        "kpa": "1e3", "kilopascal": "1e3", "kilopascals": "1e3",
        "mpa": "1e6", "megapascal": "1e6", "megapascals": "1e6",
        "gpa": "1e9", "gigapascal": "1e9", "gigapascals": "1e9",
        "hpa": "100", "hectopascal": "100", "hectopascals": "100",

        # Bar units
        "bar": "1e5", "bars": "1e5",
        "mbar": "1e2", "millibar": "1e2", "millibars": "1e2",

        # Atmosphere
        "atm": "101325", "atmosphere": "101325", "atmospheres": "101325",

        # Torr / mmHg
        "torr": "133.322", "mmhg": "133.322", "mmHg": "133.322",
        "millimeter of mercury": "133.322", "millimeters of mercury": "133.322",

        # Inches of Mercury
        "inhg": "3386.39", "inch of mercury": "3386.39", "Inch of mercury": "3386.39",
        "inHg": "3386.39", "inches of mercury": "3386.39", "Inches of mercury": "3386.39",

        # Per Square Inch
        "psi": "6894.76", "pound per square inch": "6894.76", "pounds per square inch": "6894.76",
        "psia": "6894.76", "psig": "6894.76",
        "ksi": "6894760", "kip per square inch": "6894760", "kips per square inch": "6894760",

        # CGS System
        "barye": "0.1", "ba": "0.1",
        "dyne/cm²": "0.1", "dyne per square centimeter": "0.1", "dyne/cm2": "0.1", "dyne per cm 2": "0.1",

        # Technical atmosphere (kgf/cm²)
        "at": "98066.5", "technical atmosphere": "98066.5", "technical atmospheres": "98066.5",

        # Kilogram-force per square meter
        "kgf/m²": "9.80665", "kilogram-force per square meter": "9.80665", "kgf/m2": "9.80665", "kgf per m2": "9.80665",

        # Kilogram-force per square centimeter (alias technical atm)
        "kgf/cm²": "98066.5", "kilogram-force per square centimeter": "98066.5", "kgf/cm3": "98066.5", "kgf per cm3": "98066.5",

        # Ton-force per square inch
        "tsi": "1.379e7", "ton per square inch": "1.379e7", "tons per square inch": "1.379e7",

        # Ton-force per square foot
        "tsf": "9.578e4", "ton per square foot": "9.578e4", "tons per square foot": "9.578e4",

        # Ton-force per square meter
        "tf/m²": "9806650", "ton-force per square meter": "9806650", "tf/m2": "9806650", "tf per m²": "9806650",

        # Pascal fractions
        "millipa": "1e-3", "millipascal": "1e-3", "millipascals": "1e-3",
        "μpa": "1e-6", "micropascal": "1e-6", "micropascals": "1e-6", "micro pascal": "1e-6",
        "npa": "1e-9", "nanopascal": "1e-9", "nanopascals": "1e-9",
        "ppa": "1e-12", "picopascal": "1e-12", "picopascals": "1e-12",

        # Pascal multiples
        "tpa": "1e12", "terapascal": "1e12", "terapascals": "1e12",
        "epa": "1e18", "exapascal": "1e18", "exapascals": "1e18",
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, precision=None, format="raw", delimiter=False, mode="standard", atmPressure=14.696, **kwargs):
        aliasesMap = {
        'precision': ['precision', 'prec', 'p'],
        'format': ['format', 'fmt', 'f'],
        'delimiter': ['delimiter', 'delim', 'de'],
        'mode': ['mode', 'm']
        }

        def getParameter(default, parameterName):
            aliases = aliasesMap.get(parameterName, [])
            for alias in aliases:
                if alias in kwargs:
                    return kwargs[alias]
            return default
            
        precision = getParameter(precision, 'precision')
        format = getParameter(format, 'format')
        delimiter = getParameter(delimiter, 'delimiter')
        mode = getParameter(mode, 'mode')

        fromUnit = normalizePressureUnit(fromUnit)
        toUnit = normalizePressureUnit(toUnit)
        format = format.lower().strip() if isinstance(format, str) else format
        mode = mode.lower().strip() if isinstance(mode, str) else mode
        debugLog(f"[convert] Started 'Pressure' conversion: {value} {fromUnit} to {toUnit}")
        
        rawValue = value
        if fromUnit == "psia" and toUnit == "psig":
            value -= atmPressure
        elif fromUnit == "psig" and toUnit == "psia":
            value += atmPressure

        if fromUnit not in cls.conversionRates:
            debugLog(f"[convert] Error: From unit '{fromUnit}' not recognized!")
            raise ValueError(f"From unit '{fromUnit}' not recognized!")
        if toUnit not in cls.conversionRates:
            debugLog(f"[convert] Error: From unit '{toUnit}' not recognized!")
            raise ValueError(f"To unit '{toUnit}' not recognized!")

        precision = 9 if precision is None and mode in {"engineering", "eng", "e"} else 2 if precision is None else precision
        if int(precision) < 0: raise ValueError("Precision can't be negative!")
        else:
            try:
                precision = int(precision)
            except (ValueError, TypeError):
                raise ValueError("Precision must be a Number!")

        if mode not in {"standard", "engineering", "eng", "e"}:
            debugLog(f"[convert] Error: mode='{mode}' is not recognized!")
            raise ValueError("Mode must be either 'standard' or 'engineering'.")

        debugLog(f"[convert] Parsed prec={precision}, mode={mode}")

        if mode == "standard" and precision > 6:
            warnings.warn("High precision requested in standard mode. Consider using engineering mode for better accuracy.")

        if mode in {"engineering", "eng", "e"}:
            debugLog(f"[convert] Engineering mode activated")
            getcontext().prec = precision + 5
            getcontext().rounding = ROUND_HALF_UP

            try:
                value = Decimal(str(value))
                fromFactor = Decimal(str(cls.conversionRates[fromUnit]))
                toFactor = Decimal(str(cls.conversionRates[toUnit]))

                defaultValue = value * fromFactor
                convertedValue = defaultValue / toFactor

                debugLog(f"[convert] Engineering mode: raw result={convertedValue}")

                digits = convertedValue.adjusted() + 1
                decimalPlaces = precision - digits

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
            finalValue = round(convertedValue, precision)
            debugLog(f"[convert] Standard mode: result={finalValue}")

        if isinstance(finalValue, (float, Decimal)) and finalValue == int(finalValue):
            finalValue = int(finalValue)

        if format == "raw":
            debugLog(f"[convert] Final output: {finalValue}")
            return finalValue

        separator = None
        if delimiter:
            if delimiter is True or str(delimiter).lower().strip() == "default":
                separator = ","
            else:
                separator = str(delimiter)

        if isinstance(finalValue, int):
            formattedValue = f"{finalValue:,}" if separator else str(finalValue)
        else:
            formattedValue = f"{finalValue:,.{precision}f}" if separator else f"{finalValue:.{precision}f}"

        if separator:
            formattedValue = formattedValue.replace(",", separator)

        if format == "tag":
            result = f"{formattedValue} {toUnit}"
        elif format == "verbose":
            result = f"{rawValue} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
        debugLog(f"[convert] Final output: {result}")
        return result