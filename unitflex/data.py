from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
from unitflex.utils import debugLog
import warnings
class dataConverter:
    conversionRates  = {
        # Bit
        "bit": "1.25e-7", "Bit": "1.25e-7", "bits": "1.25e-7", "Bits": "1.25e-7",
        "b": "1.25e-7", "Bps": "1.25e-7", "bps": "1.25e-7",

        # Byte
        "byte": "1e-6", "Byte": "1e-6", "bytes": "1e-6", "Bytes": "1e-6",

        # Nibble
        "nibble": "5e-7", "nibbles": "5e-7", "Nibble": "5e-7", "Nibbles": "5e-7",

        # Kilobit
        "kilobit": "1.25e-4", "Kilobit": "1.25e-4", "kilobits": "1.25e-4", "Kilobits": "1.25e-4",
        "kbit": "1.25e-4", "Kbit": "1.25e-4", "Kb": "1.25e-4", "kbps": "1.25e-4", "Kbps": "1.25e-4",

        # Kibibyte (Binary)
        "kibibyte": "9.765625e-4", "kibibytes": "9.765625e-4", "Kibibytes": "9.765625e-4",
        "kib": "9.765625e-4", "KiB": "9.765625e-4",

        # Kilobyte
        "kilobyte": "0.001", "Kilobyte": "0.001", "kilobytes": "0.001", "Kilobytes": "0.001",
        "kbyte": "0.001", "Kbyte": "0.001", "KB": "0.001", "KBps": "0.001",

        # Megabit
        "megabit": "0.125", "Megabit": "0.125", "megabits": "0.125", "Megabits": "0.125",
        "mbit": "0.125", "Mbit": "0.125", "mbps": "0.125", "Mbps": "0.125", "Mb": "0.125",

        # Megabyte (Base Unit)
        "megabyte": "1", "Megabyte": "1", "megabytes": "1", "Megabytes": "1",
        "mbyte": "1", "Mbyte": "1", "MB": "1", "MBps": "1",

        # Mebibyte (Binary)
        "mebibyte": "1.048576", "mebibytes": "1.048576", "Mebibyte": "1.048576", "Mebibytes": "1.048576",
        "mib": "1.048576", "MiB": "1.048576",

        # Gigabit
        "gigabit": "125", "Gigabit": "125", "gigabits": "125", "Gigabits": "125",
        "gbit": "125", "Gbit": "125", "gbps": "125", "Gbps": "125", "Gb": "125",

        # Gigabyte
        "gigabyte": "1000", "Gigabyte": "1000", "gigabytes": "1000", "Gigabytes": "1000",
        "gbyte": "1000", "Gbyte": "1000", "GB": "1000", "GBps": "1000",

        # Gibibyte (Binary)
        "gibibyte": "1024", "gibibytes": "1024", "Gibibyte": "1024", "Gibibytes": "1024",
        "gib": "1024", "GiB": "1024",

        # Terabit
        "terabit": "125000", "Terabit": "125000", "terabits": "125000", "Terabits": "125000",
        "tbit": "125000", "Tbit": "125000", "tbps": "125000", "Tbps": "125000", "Tb": "125000",

        # Terabyte
        "terabyte": "1e6", "Terabyte": "1e6", "terabytes": "1e6", "Terabytes": "1e6",
        "tbyte": "1e6", "Tbyte": "1e6", "TB": "1e6", "TBps": "1e6",

        # Tebibyte (Binary)
        "tebibyte": "1.048576e6", "tebibytes": "1.048576e6", "Tebibyte": "1.048576e6", "Tebibytes": "1.048576e6",
        "tib": "1.048576e6", "TiB": "1.048576e6",

        # Petabit
        "petabit": "1.25e8", "Petabit": "1.25e8", "petabits": "1.25e8", "Petabits": "1.25e8",
        "pbit": "1.25e8", "Pbit": "1.25e8", "pbps": "1.25e8", "Pbps": "1.25e8", "Pb": "1.25e8",

        # Petabyte
        "petabyte": "1e9", "Petabyte": "1e9", "petabytes": "1e9", "Petabytes": "1e9",
        "pbyte": "1e9", "Pbyte": "1e9", "PB": "1e9", "PBps": "1e9",

        # Pebibyte (Binary)
        "pebibyte": "1.073741824e9", "pebibytes": "1.073741824e9", "Pebibyte": "1.073741824e9", "Pebibytes": "1.073741824e9",
        "pib": "1.073741824e9", "PiB": "1.073741824e9",

        # Exabit
        "exabit": "1.25e11", "exabits": "1.25e11", "Exabit": "1.25e11", "Exabits": "1.25e11", 
        "ebit": "1.25e11", "ebps": "1.25e11", "Ebit": "1.25e11", "Ebps": "1.25e11", "Eb": "1.25e11",

        # Exbibyte (Binary)
        "exbibyte": "1.099511627776e12", "exbibytes": "1.099511627776e12", "eib": "1.099511627776e12", "EiB": "1.099511627776e12",

        # Exabyte
        "exabyte": "1e12", "exabytes": "1e12", "Exabyte": "1e12", "Exabytes": "1e12",
        "ebyte": "1e12", "Ebyte": "1e12", "EB": "1e12",

        # Zettabit
        "zettabit": "1.25e14", "zettabits": "1.25e14", "Zettabit": "1.25e14", "Zettabits": "1.25e14",
        "zbit": "1.25e14", "Zbit": "1.25e14", "zbps": "1.25e14", "Zbps": "1.25e14", "Zb": "1.25e14",

        # Zettabyte
        "zettabyte": "1e15", "zettabytes": "1e15", "Zettabyte": "1e15", "Zettabytes": "1e15",
        "zbyte": "1e15", "Zbyte": "1e15", "ZB": "1e15", "ZBps": "1e15",

        # Zebibyte (Binary)
        "zebibyte": "1.1805916207174113e15", "zebibytes": "1.1805916207174113e15", 
        "Zebibyte": "1.1805916207174113e15", "Zebibytes": "1.1805916207174113e15",
        "zib": "1.1805916207174113e15", "ZiB": "1.1805916207174113e15",

        # Yottabit
        "yottabit": "1.25e17", "yottabits": "1.25e17", "Yottabit": "1.25e17", "Yottabits": "1.25e17",
        "ybit": "1.25e17", "Ybit": "1.25e17", "ybps": "1.25e17", "Ybps": "1.25e17", "Yb": "1.25e17",

        # Yottabyte
        "yottabyte": "1e18", "yottabytes": "1e18", "Yottabyte": "1e18", "Yottabytes": "1e18",
        "ybyte": "1e18", "Ybyte": "1e18", "YB": "1e18", "YBps": "1e18",

        # Yobibyte (Binary)
        "yobibyte": "1.2089258196146292e18", "yobibytes": "1.2089258196146292e18", 
        "Yobibyte": "1.2089258196146292e18", "Yobibytes": "1.2089258196146292e18",
        "yib": "1.2089258196146292e18", "YiB": "1.2089258196146292e18"
    }

    @classmethod
    def convert(cls, value, fromUnit, toUnit, *, precision=None, format="raw", delimiter=False, mode="standard", **kwargs):
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

        format = format.lower().strip() if isinstance(format, str) else format
        mode = mode.lower().strip() if isinstance(mode, str) else mode

        debugLog(f"[convert] Started 'Data' conversion: {value} {fromUnit} to {toUnit}")

        if value < 0:
            debugLog(f"[convert] Error: value is negative! '{value}'")
            raise ValueError("'Data' value cant't be negative!")
        elif value == 0:
            debugLog(f"[convert] Error: value is zero! '{value}'")
            raise ValueError("'Data' value can't be zero!")

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
            result = f"{value} {fromUnit} = {formattedValue} {toUnit}"
        else:
            raise ValueError("Unexpected format parameter!")
        debugLog(f"[convert] Final output: {result}")
        return result