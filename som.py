import os

path = "C:\\Users\\inesb\\AAIB\\ficheiros"
dir_list = os.listdir(path)
os.chdir(path)
x_array = []
sr_array = []
for i in range(len(dir_list)):
    x, sr = lib.load(dir_list[i])
    x_array.append(x)
    sr_array.append(sr)