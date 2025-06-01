from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN, InvalidOperation
from math import log10, floor
from unitflex.utils import debug_log

class PressureConverter:
    conversion_rates = {
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
        "kgf/cm2": "98066.5", "kilogram-force per square centimeter": "98066.5","kilogram-force/square centimeter": "98066.5",

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
    def convert(
        cls, value, from_unit, to_unit, *, mode="decimal", environment=None,
        precision=None, output="raw", roundin=None, significant_figures=None,
        scientific_notation=False, tolerance=None, delimiter=False, **kwargs
    ):
        aliases_map = {
            'precision': ['precision', 'prec'],
            'delimiter': ['delimiter', 'delim'],
            'scientific_notation': ['scientific_notation', 'scinote'],
            'significant_figures': ['significant_figures', 'sigfigs'],
            'environment': ['env']
        }

        def get_parameter(default, parameter_name):
            aliases = aliases_map.get(parameter_name, [])
            for alias in aliases:
                if alias in kwargs:
                    return kwargs[alias]
            return default

        precision = get_parameter(precision, 'precision')
        output = get_parameter(output, 'output')
        delimiter = get_parameter(delimiter, 'delimiter')
        mode = get_parameter(mode, 'mode')
        environment = get_parameter(environment, 'environment')
        significant_figures = get_parameter(significant_figures, 'significant_figures')
        scientific_notation = get_parameter(scientific_notation, 'scientific_notation')

        from_unit = from_unit.lower().strip() if isinstance(from_unit, str) else from_unit
        to_unit = to_unit.lower().strip() if isinstance(to_unit, str) else to_unit
        roundin = roundin.lower().strip() if isinstance(roundin, str) else roundin
        output = output.lower().strip() if isinstance(output, str) else output
        mode = mode.lower().strip() if isinstance(mode, str) else mode
        
        debug_log(f"[convert] Started 'Pressure' conversion: {value} {from_unit} to {to_unit}")
        
        if environment is None:
            environment = {}
        else:
            debug_log(f"[convert] Environment use: {environment}")

        atm_pressure = None
        gravity = None 
        temperature = None 

        for key, (value, unit) in environment.items():
            key = key.lower()
            unit = unit.lower()

            if key == "atm_pressure":
                atm_pressure = value
                if unit == "psi":
                    atm_pressure = atm_pressure * 6894.76  # psi ➔ Pa
            elif key == "gravity":
                gravity = value
                if unit in {"ft/s²", "ft/s2"}:
                    gravity = gravity * 0.3048  # ft/s² ➔ m/s²
                elif unit in {"gal", "galileo"}:
                    gravity = gravity * 0.01  # Gal ➔ m/s²
                elif unit in {"g", "g-force", "gf"}:
                    gravity = gravity * 9.80665  # g ➔ m/s²
            elif key == "temperature":
                temperature = value
                if unit in {"°f", "f", "fahrenheit"}:
                    temperature = (temperature - 32) * 5/9  # ➔ °C
            else:
                pass

        if atm_pressure is None:
            if ("psia" in from_unit or "psig" in from_unit or
                "psia" in to_unit or "psig" in to_unit):
                atm_pressure = 14.696 * 6894.76  # psi ➔ Pa
            else:
                atm_pressure = 101325  # Pa (SI)
        if gravity is None:
            gravity = 9.80665
        if temperature is None:
            temperature = 20

        raw_value = value
        if from_unit == "psia" and to_unit == "psig":
            value -= atm_pressure
        elif from_unit == "psig" and to_unit == "psia":
            value += atm_pressure
            
        if not isinstance(value,(int, float)):
            raise ValueError("Invalid input: value must be an integer or float!.")
        if value <= 0 and (from_unit and to_unit not in {"psia", "psig"}):
            debug_log(f"[convert] Error: value is invalid! '{value}'")
            raise ValueError("'Pressure` value must be a postive integer or float!")

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

                gravity = Decimal(str(gravity))
                # Kgf/cm2 conversion
                if from_unit in {"kgf/cm2", "kgf/cm²", "kilogram-force per square centimeter" } and to_unit in {"pa", "pascal"}:
                    kgfcm2_pa_factor = gravity * Decimal('10000') 
                    value *= kgfcm2_pa_factor
                    converted_value = value
                elif from_unit in {"pa", "pascal"} and to_unit == "kgf/cm2":
                    kgfcm2_pa_factor = gravity * Decimal('10000') 
                    value /= kgfcm2_pa_factor
                    converted_value = value
                #Kgf/m2 conversion
                elif from_unit in {"kgf/m2", "kgf/m²", "kilogram-force per square meter"} and to_unit in {"pa", "pascal"}:
                    value *= gravity
                    converted_value = value
                elif from_unit in {"pa", "pascal"} and to_unit in {"kgf/m2"}: 
                    value /= gravity
                    converted_value = value
                else:
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
            raise ValueError("Unexpected output parameter!")

        debug_log(f"[convert] Final output: {result}")
        return result