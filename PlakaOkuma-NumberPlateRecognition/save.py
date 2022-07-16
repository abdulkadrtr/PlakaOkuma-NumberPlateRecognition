import datetime
from time import time

def write(message):
    f = open("data.txt", "r")
    result = f.read().find(message)
    f.close()
    if result ==-1:
        time = datetime.datetime.now()
        f = open("data.txt","a")    
        f.write(message +" ")
        f.write(str(time)+"\n")
        f.close