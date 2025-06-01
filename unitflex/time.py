from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN, InvalidOperation
from unitflex.utils import debug_log
from math import log10, floor
import warnings
class TimeConverter:
    conversion_rates = {
        # Base unit: second (s)
        "s": "1", "sec": "1", "second": "1", "seconds": "1",

        # Millisecond and smaller
        "ms": "0.001", "millisecond": "0.001", "milliseconds": "0.001",
        "μs": "0.000001", "us": "0.000001", "microsecond": "0.000001", "microseconds": "0.000001",
        "ns": "0.000000001", "nanosecond": "0.000000001", "nanoseconds": "0.000000001",

        # Minute and larger
        "min": "60", "minute": "60", "minutes": "60",
        "h": "3600", "hr": "3600", "hour": "3600", "hours": "3600",
        "d": "86400", "day": "86400", "days": "86400",
        "w": "604800", "wk": "604800", "week": "604800", "weeks": "604800",
        "m": "2629800", "mo": "2629800", "month": "2629800", "months": "2629800",
        "y": "31557600", "yr": "31557600", "year": "31557600", "years": "31557600",

        # Additional variants
        "millis": "0.001", "micros": "0.000001", "nanos": "0.000000001",

        # Custom calendar-based terms
        "quarter": "7889400", "quarters": "7889400", "triwulan": "7889400",
        "semester": "15778800", "semesters": "15778800",
        "bimonth": "5259600", "bimonthly": "5259600",
        "trimester": "7889400", "trimesters": "7889400",
        "quadmester": "10505700", "quadmesters": "10505700",

        # Longer periods
        "decade": "315576000", "decades": "315576000", "dasawarsa": "315576000",
        "score": "631152000", "scores": "631152000",
        "generation": "946728000", "generations": "946728000",
        "century": "3155760000", "centuries": "3155760000",
        "millennium": "31557600000", "millennia": "31557600000", "milenium": "31557600000", "millenium": "31557600000",
        "windu": "252460800", "windus": "252460800",
        "lustrum": "157788000", "lustra": "157788000",
    }

    @classmethod
    def convert(
        cls, value, from_unit, to_unit, *, mode='decimal', 
        precision=None, output='raw', roundin=None, significant_figures=None,
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

        to_unit = to_unit.lower().strip() if isinstance(to_unit, str) else to_unit
        from_unit = from_unit.lower().strip() if isinstance(from_unit, str) else from_unit
        roundin = roundin.lower().strip() if isinstance(roundin, str) else roundin
        output = output.lower().strip() if isinstance(output, str) else output
        mode = mode.lower().strip() if isinstance(mode, str) else mode

        debug_log(f"[convert] Started 'Length' conversion: {value} {from_unit} to {to_unit}")

        if not isinstance(value,(int, float)):
            raise ValueError("Invalid input: value must be an integer or float!.")
        if value <= 0:
            debug_log(f"[convert] Error: value is invalid! '{value}'")
            raise ValueError("'Length` value must be a postive integer or float!")

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
                        final_value = converted_value.quantize(quant, rounding=getcontext().rounding)
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

    @classmethod
    def flex(cls, value, from_unit, *, flex_range=(None, None), delim=True):
        getcontext().prec = 10

        if value < 0:
            raise ValueError("'Time` value can't be negative!")
        elif value == 0:
            raise ValueError("'Time` value can't be zero!")
        
        valid_units_ordered = [
            "millennium", "century", "decade", "year", "month", "week",
            "day", "hour", "minute", "second"
        ]

        lower_bound, upper_bound = flex_range

        try:
            start_index = valid_units_ordered.index(lower_bound) if lower_bound else 0
            end_index = valid_units_ordered.index(upper_bound) if upper_bound else len(valid_units_ordered) - 1
        except ValueError:
            raise ValueError(f"Invalid unit in flex_range: {flex_range}")

        if start_index > end_index:
            raise ValueError("Invalid flex_range: lower bound must be larger unit than upper bound")

        allowed_units = valid_units_ordered[start_index:end_index + 1]

        try:
            value = str(value)
            base_seconds = Decimal(value) * Decimal(cls.conversion_rates[from_unit])
        except KeyError:
            raise ValueError(f"Unit '{from_unit}' not recognized for flex conversion.")
        except Exception as e:
            debug_log(f"[flex] Error: {e}")
            raise ValueError(f"Invalid input value for conversion: {value!r}") from e

        ordered_units = []
        for unit in valid_units_ordered:
            if unit in allowed_units:
                for key, rate in cls.conversion_rates.items():
                    if key.lower() == unit:
                        ordered_units.append((unit, Decimal(rate)))
                        break

        result = []
        remaining = base_seconds

        for unit_name, unit_seconds in ordered_units:
            count = remaining // unit_seconds
            if count > 0:
                count_str = f"{int(count):,}" if delim else str(int(count))
                result.append(f"{count_str} {unit_name}{'s' if int(count) != 1 else ''}")
                remaining -= count * unit_seconds

            if remaining < Decimal("0.0001"):
                break

        if not result:
            result.append("0 second")

        final = " ".join(result)
        debug_log(f"[flex] Output: {final}")
        return final
