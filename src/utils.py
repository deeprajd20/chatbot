from datetime import datetime

def get_time(date=False, time=False):
    now = datetime.now()

    if date and time:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    elif date:
        return now.strftime("%Y-%m-%d")
    elif time:
        return now.strftime("%H:%M:%S")
    else:
        return "Please specify either date or time"