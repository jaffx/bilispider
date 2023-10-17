import time, datetime

getDefault = lambda d, k, v: d[k] if isinstance(d, dict) and k in d else v


def timeStamp2Str(t):
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
