import serial, time

port = "COM1"
baud = 1200

ser = serial.Serial(port, baud, timeout = 1)

command = "V"

output_file = "AccuBalance_test.txt"

def blank_remove(data):
    temp = []
    for element in data:
        if len(element) > 0:
            temp.append(element)
    return temp

date = time.localtime()
date = str(date[2]) + "." + str(date[1]) + "." + str(date[0])
file = open(output_file, "a")
header = "\n" + "* * * *\n\n" + "AccuBalance Plus\n" + "Data pomiaru: " + date + "\n\n" + "* * * *\n\n"
print(header)
file.write(header)
file.close()

while True:
    ser.flush()
    ser.write(command.encode())
    resp = ser.readline()
    if len(resp) > 0:
        resp = str(resp).split("\\")[0]
        #print("Raw response: " + resp)
        resp = resp.split(" ")
        resp = blank_remove(resp)
        #print("Data: " + str(resp))
        accu_time = resp[0].split("'")[1]
        if str(resp[1]).isdigit():
            accu_flow = str(resp[1])
        else:
            accu_flow = "0"
        accu_temp = resp[-1]
        date = time.localtime()
        date = str(date[2]) + "." + str(date[1]) + "." + str(date[0])

        file = open(output_file, "a")
        output_data = date + ", " + accu_time + ", " + accu_flow + ", m3/h, " + accu_temp + ", deg.C"
        print(output_data)
        file.write(output_data + "\n")
        file.close()
