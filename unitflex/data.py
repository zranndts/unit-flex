from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN, InvalidOperation
from unitflex.utils import debug_log
from math import log10, floor
class DataConverter:
    conversion_rates  = {
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
    def convert(
        cls, value, from_unit, to_unit, *, mode="decimal", 
        precision=None, output="raw", roundin=None, significant_figures=None,
        scientific_notation=False, tolerance=None, delimiter=False, **kwargs
    ):
        aliases_map = {
            'precision': ['precision', 'prec'],
            'delimiter': ['delimiter', 'delim'],
            'roundin': ['roundin', 'rounding', 'round'],
            'significant_figures': ['significant_figures', 'sigfigs'],
            'scientific_notation': ['scientific_notation', 'sci_note', 'scinote']
        }

        def get_parameter(default, parameter_name):
            aliases = aliases_map.get(parameter_name, [])
            for alias in aliases:
                if alias in kwargs:
                    return kwargs[alias]
            return default

        precision = get_parameter(precision, 'precision')
        delimiter = get_parameter(delimiter, 'delimiter')
        roundin = get_parameter(roundin, 'roundin')
        significant_figures = get_parameter(significant_figures, 'significant_figures')
        scientific_notation = get_parameter(scientific_notation, 'scientific_notation')

        to_unit = to_unit if isinstance(to_unit, str) else to_unit
        from_unit = from_unit if isinstance(from_unit, str) else from_unit
        roundin = roundin.lower().strip() if isinstance(roundin, str) else roundin
        output = output.lower().strip() if isinstance(output, str) else output
        mode = mode.lower().strip() if isinstance(mode, str) else mode

        debug_log(f"[convert] Started 'Data' conversion: {value} {from_unit} to {to_unit}")

        if not isinstance(value,(int, float)):
            raise ValueError("Invalid input: value must be an integer or float!.")
        if value <= 0:
            debug_log(f"[convert] Error: value is invalid! '{value}'")
            raise ValueError("'Data` value must be a postive integer or float!")

        if from_unit not in cls.conversion_rates:
            debug_log(f"[convert] Error: From unit '{from_unit}' not recognized!")
            raise ValueError(f"From unit '{from_unit}' not recognized!")
        if to_unit not in cls.conversion_rates:
            debug_log(f"[convert] Error: To unit '{to_unit}' not recognized!")
            raise ValueError(f"To unit '{to_unit}' not recognized!")

        precision = 9 if precision is None and mode in {"decimal", "dec"} else 2 if precision is None else precision
        if int(precision) <= 0:
            debug_log(f"[convert] Error: precision is invalid! '{precision}'")
            raise ValueError("Precision must be a postive integer!")
        try:
            precision = int(precision)
        except (ValueError, TypeError):
            debug_log(f"[convert] Error: precision is not an Integer! '{precision}'")
            raise ValueError("Precision must be an Integer!")

        if mode not in {"decimal", "dec", "float", "float64"}:
            debug_log(f"[convert] Error: mode='{mode}' is not recognized!")
            raise ValueError(f"Mode '{mode}' is not recognized.")
        debug_log(f"[convert] Parsed prec={precision}, mode={mode}")

        if mode in {"decimal", "dec"}:
            debug_log(f"[convert] Decimal mode activated")
            getcontext().prec = precision * 2
            if roundin is None:
                getcontext().rounding = ROUND_HALF_UP
                debug_log(f"[convert] Rounding is None, set default rounding: 'Round Half Up'.")
            elif roundin == "half_even":
                getcontext().rounding = ROUND_HALF_EVEN
                debug_log(f"[convert] Use Round Half Even rounding.")
            elif roundin == "half_up":
                debug_log(f"[convert] Use Round Half Up rounding.")
                getcontext().rounding = ROUND_HALF_UP
            else:
                raise ValueError(f"Rounding '{roundin}' is not recognized!")

            try:
                value = Decimal(str(value))
                from_factor = Decimal(str(cls.conversion_rates[from_unit]))
                to_factor = Decimal(str(cls.conversion_rates[to_unit]))
                default_value = value * from_factor
                converted_value = default_value / to_factor

                debug_log(f"[convert] Decimal mode: raw result={converted_value}")

                digits = converted_value.adjusted() + 1
                decimal_places = precision - digits

                if 0 <= decimal_places <= 50:
                    try:
                        quant = Decimal(f"1e-{decimal_places}")
                        final_value = converted_value.quantize(quant, rounding=ROUND_HALF_EVEN)
                    except (InvalidOperation, ValueError) as e:
                        debug_log(f"[convert] Quantize fallback triggered: {e}")
                        final_value = converted_value.normalize()
                else:
                    debug_log(f"[convert] Skipping quantize due to extreme decimal_places={decimal_places}")
                    final_value = converted_value.normalize()
            except (InvalidOperation, ValueError) as e:
                debug_log(f"[convert] Decimal error: {e}")
                raise ValueError("Conversion failed due to invalid decimal operation.")
            debug_log(f"[convert] Decimal mode: adjusted result={final_value}")
        elif mode in {"float", "float64"}:
            debug_log(f"[convert] Float mode activated")
            default_value = float(value) * float(cls.conversion_rates[from_unit])
            converted_value = default_value / float(cls.conversion_rates[to_unit])
            final_value = round(converted_value, precision)
            debug_log(f"[convert] Float mode: result={final_value}")
        else:
            raise ValueError(f"Mode '{mode}' is not recognized!")

        if isinstance(final_value, (float, Decimal)) and final_value == int(final_value):
            final_value = int(final_value)

        if output == "raw" and scientific_notation is False and significant_figures is None:
            return final_value
        
        def round_sigfigs(num, sigfigs):
            if num == 0:
                return Decimal(0)
            elif isinstance(num, Decimal):
                shift = sigfigs - num.adjusted() - 1
                quantizer = Decimal('1e{}'.format(-shift))
                return num.quantize(quantizer, rounding=getcontext().rounding)
            else:
                return round(num, -int(floor(log10(abs(num)))) + (sigfigs - 1))

        if significant_figures:
            try:
                sigfigs = int(significant_figures)
                if sigfigs <= 0:
                    raise ValueError("Significant figures must be a positive integer!")
            except (ValueError, TypeError):
                raise ValueError("Invalid significant_figures parameter!")

            final_value = round_sigfigs(final_value, sigfigs)
            debug_log(f"[convert] Applying Significant Figures={sigfigs}")
        else:
            sigfigs = None

        if scientific_notation:
            debug_log(f"[convert] Applying Scientific Notation")
            digits = sigfigs - 1 if sigfigs is not None else precision
            formatted_value = f"{final_value:.{digits}E}"
        else:
            if sigfigs:
                decimal_places = sigfigs - (final_value.adjusted() + 1)
                decimal_places = max(decimal_places, 0)
                formatted_value = f"{final_value:.{decimal_places}f}"
            else:
                formatted_value = f"{final_value:.{precision}f}"

        if output == "raw":
            if scientific_notation:
                debug_log(f"[convert] Final output: {formatted_value}")
                return formatted_value
            elif sigfigs:
                debug_log(f"[convert] Final output: {formatted_value}")
                return float(formatted_value)

        separator = None
        if delimiter:
            if delimiter is True or str(delimiter).lower().strip() == "default":
                separator = ","
            else:
                separator = str(delimiter)

        if scientific_notation is False:
            final_value_str = format(final_value, 'f') 
        else:
            final_value_str = format(final_value, 'e')

        if significant_figures is not None and scientific_notation is False:
            final_value_str = final_value_str.rstrip('0').rstrip('.') if '.' in final_value_str else final_value_str

        if separator:
            formatted_value = formatted_value.replace(",", separator)

        if output == "tag":
            result = f"{formatted_value} {to_unit}"
        elif output == "verbose":
            result = f"{value} {from_unit} = {formatted_value} {to_unit}"
        else:
            raise ValueError("Unexpected format parameter!")

        debug_log(f"[convert] Final output: {result}")
        return result