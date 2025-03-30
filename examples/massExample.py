from unitflex.mass import MassConverter

# Convert 2.5 kilograms to grams with raw number output
print(MassConverter.convert(2.5, "kg", "g", precission=0, formatStyle="raw"))
