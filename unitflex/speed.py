from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN, InvalidOperation
from math import log10, floor
from unitflex.utils import debug_log
class SpeedConverter:
    conversion_rates = {
        # Milimeter per second
        "mm/s": "0.001", "millimeter per second": "0.001", 
        "millimeters per second": "0.001","mm per second": "0.001",
        "mm/min": "0.000016666666666666666", "millimeter per minute": "0.000016666666666666666", 
        "millimeters per minute": "0.000016666666666666666", "mm per minute": "0.000016666666666666666",

        # Centimeters per second
        "cm/s": "0.01", "centimeter per second": "0.01", 
        "centimeters per second": "0.01", "cm per second": "0.01",

        # Centimeter per minute
        "cm/min": "0.00016666666666666666", "centimeter per minute": "0.00016666666666666666", 
        "centimeters per minute": "0.00016666666666666666", "cm": "0.00016666666666666666",

        # Meters per second (base unit)
        "m/s": "1", "meter per second": "1", "meters per second": "1",

        # Meters per minute
        "m/min": "0.016666666666666666", "meter per minute": "0.016666666666666666", 
        "meters per minute": "0.016666666666666666",

        # Kilometers per hour
        "km/h": "0.27777777777777778", "kph": "0.277778", "kilometer per hour": "0.277778", 
        "kilometers per hour": "0.277778", "km per hour": "0.277778",
 
        # Miles per hour
        "mi/h": "0.44704", "mph": "0.44704", "mile per hour": "0.44704", "miles per hour": "0.44704",

        # Feet per second
        "ft/s": "0.3048", "fps": "0.3048", "foot per second": "0.3048", "feet per second": "0.3048",

        # Knots
        "kt": "0.514444", "knot": "0.514444", "knots": "0.514444", "kn": "0.514444",

        # Mach (at sea level)
        "mach": "340.29", "ma": "340.29",

        # Speed of light
        "c": "299792458", "speed of light": "299792458",

        # Inches per second
        "in/s": "0.0254", "inch per second": "0.0254", "inches per second": "0.0254",

        # Inches per minute
        "in/min": "0.0004233333333333333", "inch per minute": "0.0004233333333333333", 
        "inches per minute": "0.0004233333333333333",
    }

    @classmethod
    def convert(
        cls, value, from_unit, to_unit, *, mode="decimal", environment=None,
        precision=None, output="raw", roundin=None, significant_figures=None,
        scientific_notation=False, tolerance=None, delimiter=False, **kwargs
    ):
        aliases_map = {
            'precision': ['precision', 'prec'],
            'delimiter': ['delimiter', 'delim'],
            'roundin': ['roundin', 'rounding', 'round'],
            'environment':['environment', 'env'],
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

        debug_log(f"[convert] Started 'Speed' conversion: {value} {from_unit} to {to_unit}")

        if not isinstance(value,(int, float)):
            raise ValueError("Invalid input: value must be an integer or float!.")
        if value <= 0:
            debug_log(f"[convert] Error: value is invalid! '{value}'")
            raise ValueError("'Speed` value must be a postive integer or float!")

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

            getcontext().prec = max(getcontext().prec, sigfigs * 2)
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