import os
import sys
import serial
import glob

if len(sys.argv) == 1:
    print("uploadGeneration.py <file path>")
    print("\t<file>: .ino file you want to upload to your board")
    sys.exit(2)
else:
    platform = 0
    if sys.platform.startswith("win"):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        ports = glob.glob('/dev/tty[A-Za-z]*')
        platform = 1
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    if len(ports) == 0:
        print("No available COM ports!")
        sys.exit(2)
    else:
        arduinoFile = str(sys.argv[1])
        if platform == 0:
            for port in result:
                print("\t- Port " + port + " available")
            command = "arduino-cli compile --fqbn esp32:esp32:m5stick-c " + arduinoFile + " && arduino-cli upload -p " + str(result[0]) + " --fqbn esp32:esp32:m5stick-c " + arduinoFile
            os.system('cmd /c "' + command + '"')
        else:
            commands = ["arduino-cli compile --fqbn esp32:esp32:m5stick-c "+arduinoFile, "arduino-cli upload -p "+ str(result[0]) + " --fqbn esp32:esp32:m5stick-c " + arduinoFile]
            for command in commands:
                os.system(command)
