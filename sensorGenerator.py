import json
import jinja2
import os
import sys


def getSensorFromOption():
    i = 1
    sensors = []

    for sensor in os.listdir("./Examples"):
        for file in os.listdir("./Examples/" + sensor):
            if file.endswith(".ino"):
                fileName = file[9:-4].lower()
                print(str(i) + ") " + file + " - " + json_c['sensor_description'][fileName])
                sensors.insert(i-1, fileName)
        i += 1

    return sensors


with open('questions.json') as json_file:
    json_q = json.load(json_file)

with open('code.json') as json_file:
    json_c = json.load(json_file)


libraries = []
constants = []
codeVars = []
settings = []
code = []
remoteStore = False
period = False
captivePortal = False
sensorType = 0

for lib in json_c['general_lib']:
    libraries.append(json_c['general_lib'][lib])

correct = False
print(json_q['introduction']['welcome'])
print(json_q['sensors_list']['list_init'])

while not correct:

    sensors = getSensorFromOption()
    print(json_q['sensors_list']['i0'])
    option = input(json_q['sensors_list']['i1'])

    if 0 <= int(option) <= len(sensors):
        correct = True
        sensorType = sensors[int(option) - 1]
        libraries.append(json_c['sensor_lib'][sensorType])
        for a in json_c['sensors_vars'][sensorType]:
            codeVars.append(json_c['sensor_vars'][sensorType][a])
    else:
        print(json_q["error"])

correct = False
while not correct:
    option = input(json_q['code_questions']['wifi']['q0'])
    if 0 <= int(option) <= 1:
        correct = True
        if int(option) == 0:
            remoteStore = True
            for lib in json_c['storing_lib']:
                libraries.append(json_c['storing_lib'][lib])
    else:
        print(json_q["error"])

correct = False
while not correct:
    option = input(json_q['code_questions']['measures']['q0'])
    if 0 <= int(option) <= 1:
        correct = True
        if int(option) == 1:
            period = True
            option = input(json_q['code_questions']['measures']['q1'])
            correct = True
            constants.append(json_c['constants']['c0'])
            constants.append(json_c['constants']['c1'] + option)
    else:
        print(json_q["error"])

correct = False
if remoteStore:
    print(json_q['code_questions']['captive_portal']['q0'])
    while not correct:
        option = input(json_q['code_questions']['captive_portal']['q1'])
        if 0 <= int(option) <= 1:
            correct = True
            if int(option) == 0:
                captivePortal = True
                for a in json_c['settings']['captive_portal']:
                    settings.append(json_c['settings']['captive_portal'][a])
                if remoteStore:
                    for a in json_c['settings']['remote_server']:
                        settings.append(json_c['settings']['remote_server'][a])
                    for a in json_c['settings']['wifi']:
                        settings.append(json_c['settings']['wifi'][a])
                    for a in json_c['code_blocks']['wifi']:
                        code.append(json_c['code_blocks']['wifi'][a])
                    for a in json_c['code_blocks']['ip']:
                        code.append(json_c['code_blocks']['ip'][a])
                for a in json_c['code_blocks']['captive_portal']:
                    code.append(json_c['code_blocks']['captive_portal'][a])
                for a in json_c['code_blocks']['credentials']:
                    code.append(json_c['code_blocks']['credentials'][a])
        else:
            print(json_q["error"])

    code.append(json_c['code_blocks']['remote_server']['f0'])
    code.append(json_c['code_blocks']['remote_server']['sensors']['titles'][sensorType])
    code.append(json_c['code_blocks']['remote_server']['common']['c0'])
    code.append(json_c['code_blocks']['remote_server']['common']['c1'])
    if sensorType == "max30100":
        code.append(json_c['code_blocks']['remote_server']['sensors']['jsons']['max30100a'])
        code.append(json_c['code_blocks']['remote_server']['common']['c2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c1'])
        code.append(json_c['code_blocks']['remote_server']['sensors']['jsons']['max30100b'])
        code.append(json_c['code_blocks']['remote_server']['common']['c4'])
        code.append(json_c['code_blocks']['remote_server']['sensors']['s2'])
    else:
        code.append(json_c['code_blocks']['remote_server']['sensors']['jsons'][sensorType])
        code.append(json_c['code_blocks']['remote_server']['common']['c2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c3'])

code.append(json_c['code_blocks']['start_sensor']['common']['f0'])
if remoteStore:
    code.append(json_c['code_blocks']['start_sensor']['common']['f3'])

code.append(json_c['code_blocks']['start_sensor']['initialize'][sensorType])
if remoteStore:
    code.append(json_c['code_blocks']['start_sensor']['webserver'][sensorType])
if period > 0:
    if sensorType != "gsr":
        code.append(json_c['code_blocks']['start_sensor']['common']['f1'])
    else:
        code.append(json_c['code_blocks']['start_sensor']['body']['b2'])
if sensorType == "tmp117":
    code.append(json_c['code_blocks']['start_sensor']['body']['b0'])

code.append(json_c['code_blocks']['start_sensor']['common']['f2'])

code.append(json_c['code_blocks']['setup']['init'])
if captivePortal:
    code.append(json_c['code_blocks']['setup']['portal'])
code.append(json_c['code_blocks']['setup']['end'])

code.append(json_c['code_blocks']['loop']['init'])
if captivePortal:
    code.append(json_c['code_blocks']['loop']['portal'])
else:
    code.append(json_c['code_blocks']['loop']['noPortal'])
code.append(json_c['code_blocks']['loop']['end'])

print("Answers colected!")

all = {"libraries":libraries, "constants":constants, "codeVars":codeVars, "settings":settings, "code":code}
y = json.dumps(all)
y = json.loads(y)
#print(y)

outputFileName = "M5StickC_" + sensorType + ".ino"
result = jinja2.Environment(loader=jinja2.FileSystemLoader('./')).get_template('sensor-template.ino')
result = result.render(templ=y)
#print(result)

outFile = open(outputFileName, "w")
outFile.write(result)
outFile.close()

correct = False
while not correct:
    print(json_q["complete_process"]["q0"])
    option = input(json_q["complete_process"]["q1"])
    if int(option)==0:
        correct = True
        command = "python uploadGeneration.py " + outputFileName
        if sys.platform.startswith("win"):
            os.system('cmd /c "' + command + '"')
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            os.system("python ./uploadGeneration.py " + outputFileName)
        else:
            raise EnvironmentError("Unsupported platform")
    elif int(option) > 1:
        print(json_q["error"])