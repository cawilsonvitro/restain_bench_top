import os
from datetime import datetime as dt

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


date = dt.now().strftime("%m-%d-%Y, Hour %H Min %M Sec %S")

day = date[:date.find(",")]

print(date)

path = r"data"


last_file = newest(path)

exst = ".csv"

last_file = last_file[:last_file.find(exst)]

print(last_file)
sample_num = 1

if last_file.find(day) == -1:
    sample_num = 1

else:
    sample_num = int(last_file[-1]) + 1


print(sample_num)
