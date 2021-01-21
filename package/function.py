from datetime import datetime
def current_time():
    return datetime.now().strftime("%d-%m-%y %H:%M:%S")