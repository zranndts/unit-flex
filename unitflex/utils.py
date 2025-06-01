from unitflex import config
def debug_log(message):
    if config.DEBUG == True:
        print(f"[DEBUG] {message}")