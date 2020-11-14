import os
import sys

if len(sys.argv) == 1:
    print("You must indicate the path of your 'arduino-cli' executable file!")
    print("If you didn't download it yet, go to: https://arduino.github.io/arduino-cli/latest/installation/#download")
    print("\tSchema: tools.py <file path>")
    sys.exit(2)
else:
    platform = 0
    if sys.platform.startswith("win"):
        os.system('cmd /c "setx path \"%PATH%;"' + str(sys.argv[0]) + '"\""')
        os.system('cmd /c "arduino-cli core install arduino:avr"')
        os.system('cmd /c "arduino-cli config init && arduino-cli core update-index --additional-urls https://dl.espressif.com/dl/package_esp32_index.json"')
        os.system('cmd /c "arduino-cli core install esp32:esp32"')
        os.system('cmd /c "arduino-cli board listall esp32"')
        # adding necessary libraries
        os.system('cmd /c "arduino-cli lib install \"M5StickC\" && arduino-cli lib install \"SparkFun High Precision Temperature Sensor TMP117 Qwiic\" && arduino-cli lib install \"MAX30100lib\""')
        os.system('cmd /c "pip install Jinja2 && pip install pyserial"')
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        os.system('export PATH=$PATH:' + str(sys.argv[0]))
        commands = ["arduino-cli core install arduino:avr", "arduino-cli config init",
                    "arduino-cli core update-index --additional-urls https://dl.espressif.com/dl/package_esp32_index.json",
                    "arduino-cli core install esp32:esp32", "arduino-cli board listall esp32",
                    "arduino-cli lib install \"M5StickC\"",
                    "arduino-cli lib install \"SparkFun High Precision Temperature Sensor TMP117 Qwiic\"",
                    "arduino-cli lib install \"MAX30100lib\"", "pip install Jinja2", "pip install pyserial"]
        for command in commands:
            os.system(command)
    else:
        raise EnvironmentError("Unsupported platform")
