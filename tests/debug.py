import unitflex as uf
from unitflex import config
config.DEBUG = False
from unitflex import(
    temperature as temp,
    pressure as press,
    volume as vol
)

print(f"Author: {uf.__author__}, Version: {uf.__version__}")
uf.length.convert(1, "lightyear", "femtometer", mode="engineering", delim="default")
uf.mass.convert(1, "earthmass", "dalton", mode="engineering", delim="default")
uf.time.flex(1.292321, "year")
uf.time.flex(1.5328, "century", flexRange=("hour", "second"), delim=False)
uf.time.convert(1, "millennium", "day", delim="default")
uf.data.convert(1.231, "GiB", "TiB", mode="engineering")
uf.speed.convert(1, "c", "mach", mode="eng", de=True, prec=12, fmt = "tag",)
press.convert(1.213, "psia", "psig", prec=3, de=True, fmt="tag", m="eng")
press.convert(12923.008783, "psia", "pascal", de=True, m="e", p=10, f="tag")
uf.length.convert(58923.7285, "km", "miles",prec=12, fmt="tag", de=True, m="eng")
uf.length.convert(59800.6850, "km", "miles", prec=6, fmt="verbose", delim=True)
uf.length.convert(1, "lightyear", "km", mode="eng", prec=10, fmt="verbose", delim=True)
uf.data.convert(11211.472388, "MiB", "Gb", m="eng", prec=12, fmt="verbose", delim=True)
uf.mass.convert(3219.2193, "gram", "quintal", m="eng", fmt="tag")
uf.mass.convert(3219.2193, "quintal", "gram", m="eng", fmt="tag", de=True)
uf.speed.convert(20, "mach", "km/h", m="eng", f="verbose", delim=True, p=9)
temp.convert(129.912, "celcius", "kelvin", de=True, m="eng", fmt="tag", prec=8)
uf.time.convert(12.123132, "year", "minute", de=True, fmt="verbose", m="eng", p=7)
vol.convert(1921.00321, "m3", "gallons", m="e", p=15, f="tag", de=True)








