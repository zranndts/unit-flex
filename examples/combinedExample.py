from unitflex.length import LengthConverter
from unitflex.mass import MassConverter

print("Mass conversion:")
print(MassConverter.convert(1, "lb", "kg", 2, "simple"))

print("Length conversion:")
print(LengthConverter.convert(10, "mi", "km", 3, "full"))
