from unitflex import config
def debugLog(message):
    if config.DEBUG == True:
        print(f"[DEBUG] {message}")