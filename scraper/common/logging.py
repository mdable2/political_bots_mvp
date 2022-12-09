import traceback
import datetime

def log(message):
    print(f"{datetime.datetime.now()} LOG: {message}")

def error(message):
    print(f"{datetime.datetime.now()} ERROR: {message}")
    traceback.print_exc()
