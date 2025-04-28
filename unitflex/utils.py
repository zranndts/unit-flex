from unitflex import config
def debugLog(message):
    if config.DEBUG:
        print(f"[DEBUG] {message}")