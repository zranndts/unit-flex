from decimal import Decimal, getcontext, ROUND_HALF_EVEN, ROUND_HALF_UP, InvalidOperation
from math import log10, floor
from unitflex.utils import debug_log
class MassConverter:
    conversion_rates = {
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

        debug_log(f"[convert] Started 'Mass' conversion: {value} {from_unit} to {to_unit}")

        if not isinstance(value,(int, float)):
            raise ValueError("Invalid input: value must be an integer or float!.")
        if value <= 0:
            debug_log(f"[convert] Error: value is invalid! '{value}'")
            raise ValueError("'Mass` value must be a postive integer or float!")

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