import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unitflex import length
from unitflex import mass

# Debugging buat length
print(length.convert(12, fromUnit="km", toUnit="m", output="verbose"))
print(length.convert(5, fromUnit="mi", toUnit="km", precision="1", output="compact"))   
print(length.convert(160, fromUnit="cm", toUnit="ft", precision="4", output="compact"))
print(length.convert(160, fromUnit="cm", toUnit="ft", precision="1"))
print(length.convert(150, fromUnit="ft", toUnit="cm", precision="2", output="raw"))

# Debugging buat mass
result = (mass.convert(120, fromUnit="kg", toUnit="lb"))
print(f"Jadi 120 kg itu sama dengan {result} lb")
