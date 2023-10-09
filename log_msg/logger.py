import datetime
import sys


def info(msg):
    print(datetime.datetime.now(), "[INFO]", msg, sep=", ", file=sys.stdout)


def err(msg, err = None):
    if err == None:
        print(datetime.datetime.now(), "[ERROR]", msg, sep=", ", file=sys.stderr)
    else:
        print(datetime.datetime.now(), "[ERROR]", msg, err, sep=", ", file=sys.stderr)