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
uf.time.convert(1, "millennium", "day", delim="default")







