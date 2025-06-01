from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN, InvalidOperation
from math import log10, floor
from unitflex.utils import debug_log
import warnings
class VolumeConverter:
    conversion_rates = {
    # Metric Units (SI)
    "nl": "1e-9", "nanoliter": "1e-9", "nanoliters": "1e-9",
    "µl": "1e-6", "μl": "1e-6", "microliter": "1e-6", "microliters": "1e-6",
    "ml": "1e-6", "milliliter": "1e-6", "milliliters": "1e-6",
    "cl": "1e-5", "centiliter": "1e-5", "centiliters": "1e-5",
    "dl": "1e-4", "deciliter": "1e-4", "deciliters": "1e-4",
    "dal": "1e-2", "dekaliter": "1e-2", "dekaliters": "1e-2",
    "l": "1e-3", "liter": "1e-3", "liters": "1e-3",
    "hl": "0.1", "hectoliter": "0.1", "hectoliters": "0.1",
    "m3": "1", "m³": "1", "cubicmeter": "1", "cubic meters": "1", "cubic meter": "1", "cubicmeters": "1",
    "cm3": "1e-6", "cm³": "1e-6", "cubic centimeter": "1e-6", "cubic centimeters": "1e-6", "cubic centimetre": "1e-6",
    "dm3": "1e-3", "dm³": "1e-3", "cubic decimeter": "1e-3", "cubic decimeters": "1e-3",
    "mm3": "1e-9", "mm³": "1e-9", "cubic millimeter": "1e-9", "cubic millimeters": "1e-9",
    "km3": "1e9", "km³": "1e9", "cubic kilometer": "1e9", "cubic kilometers": "1e9",

    # US Customary Units (based on NIST definitions)
    "tsp": "4.92892159375e-6", "teaspoon": "4.92892159375e-6", "teaspoons": "4.92892159375e-6",
    "tbsp": "1.478676478125e-5", "tablespoon": "1.478676478125e-5", "tablespoons": "1.478676478125e-5",
    "floz": "2.95735295625e-5", "fl oz": "2.95735295625e-5", "fluid ounce": "2.95735295625e-5", "fluid ounces": "2.95735295625e-5",
    "cup": "2.365882375e-4", "cups": "2.365882375e-4",
    "pt": "4.73176475e-4", "pint": "4.73176475e-4", "pints": "4.73176475e-4",
    "qt": "9.4635295e-4", "quart": "9.4635295e-4", "quarts": "9.4635295e-4",
    "gal": "3.785411784e-3", "us sgal": "3.785411784e-3", "gallon": "3.785411784e-3", "gallons": "3.785411784e-3",
    "in3": "1.6387064e-5", "in³": "1.6387064e-5", "cubic inch": "1.6387064e-5", "cubic inches": "1.6387064e-5",
    "ft3": "0.028316846592", "ft³": "0.028316846592", "cubic foot": "0.028316846592", "cubic feet": "0.028316846592",
    "yd3": "0.764554857984", "yd³": "0.764554857984", "cubic yard": "0.764554857984", "cubic yards": "0.764554857984",

    # UK Imperial Units
    "uk gal": "4.54609e-3", "uk-gal": "4.54609e-3", "gal-uk": "4.54609e-3", "imperial gallon": "4.54609e-3", "imperial gallons": "4.54609e-3",

    # Oil Barrel
    "bbl": "0.158987294928", "barrel": "0.158987294928", "barrels": "0.158987294928",
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

        to_unit = to_unit.lower().strip() if isinstance(to_unit, str) else to_unit
        from_unit = from_unit.lower().strip() if isinstance(from_unit, str) else from_unit
        roundin = roundin.lower().strip() if isinstance(roundin, str) else roundin
        output = output.lower().strip() if isinstance(output, str) else output
        mode = mode.lower().strip() if isinstance(mode, str) else mode

        debug_log(f"[convert] Started 'Volume' conversion: {value} {from_unit} to {to_unit}")

        if not isinstance(value,(int, float)):
            raise ValueError("Invalid input: value must be an integer or float!.")
        if value <= 0:
            debug_log(f"[convert] Error: value is invalid! '{value}'")
            raise ValueError("'Volume` value must be a postive integer or float!")

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