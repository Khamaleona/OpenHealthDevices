import json
import jinja2
import os
import sys

libraries = []
codeVars = []
settings = []
code = []

correct = False
lang = ""
main = False
period = 0
flags = {}

if len(sys.argv) == 2: # and len(json_gq['language']) > 1:
    lang = str(sys.argv[1]) #storing language
    generalQ = "./questions.json"
    sensorQ = "./Devices/Galvanic/questions_sensor.json"
    sensorCode = "./Devices/Galvanic/code_sensor.json"
    template = "sensor-template.ino"
    uploadPy = "./uploadGeneration.py"
    main = True

else:
    generalQ = "../../questions.json"
    sensorQ = "./questions_sensor.json"
    sensorCode = "./code_sensor.json"
    template = "sensor-template.ino"
    uploadPy = "../../uploadGeneration.py"

with open(generalQ) as json_file:
    json_gq = json.load(json_file)

with open(sensorQ) as json_file:
    json_q = json.load(json_file)

with open(sensorCode) as json_file:
    json_c = json.load(json_file)

if len(json_q['language']) == 1 or lang == "" or lang not in json_q['language']:
    lang = "en"

for a in json_c['extra']:
    flags[a] = False
flags["period"]=0

json_q = json_q['language'][lang]
print("Sensor selected: " + json_q['info']['name'])

json_gq = json_gq['language'][lang]
print(json_gq['introduction']['welcome'])

# Libraries and vars
for lib in json_c['base']['libs']['general_lib']:
    libraries.append(json_c['base']['libs']['general_lib'][lib])
for lib in json_c['base']['libs']['sensor_lib']:
    libraries.append(json_c['base']['libs']['sensor_lib'][lib])
for var in json_c['base']['sensor_vars']:
    codeVars.append(json_c['base']['sensor_vars'][var])

option = input(json_q['code_questions']['period']['q0'])
correct = False
while not correct:
    if option == "1":
        option = input(json_q['code_questions']['period']['q1'])
        while not correct:
            if option.isnumeric():
                period = int(option)
                flags['period'] = period
                correct = True
                codeVars.append(json_c['base']['period']['c0'])
                codeVars.append(json_c['base']['period']['c1'] + str(period))
            else:
                option = input(json_q['error'])
    elif option == "0":
        correct = True
        period = 0
    else:
        option = input(json_q['error'])

correct = False
option = input(json_q['code_questions']['wifi']['q0'])
while not correct:
    if option == "0":
        flags['wifi'] = True
        correct = True
        for w in json_c['extra']['wifi']:
            for x in json_c['extra']['wifi'][w]:
                if w == "libs":
                    libraries.append(json_c['extra']['wifi'][w][x])
                if w == "vars":
                    codeVars.append(json_c['extra']['wifi'][w][x])
                if w == "functions":
                    code.append(json_c['extra']['wifi'][w][x])
    elif option == "1":
        correct = True
    else:
        option = input(json_q['error'])

if flags['wifi']:
    correct = False
    option = input(json_q['code_questions']['remote_store']['q0'])
    while not correct:
        if option == "0":
            flags['remote_store'] = True
            correct = True
            for w in json_c['extra']['remote_store']:
                for x in json_c['extra']['remote_store'][w]:
                    if w == "libs":
                        libraries.append(json_c['extra']['remote_store'][w][x])
                    if w == "vars":
                        codeVars.append(json_c['extra']['remote_store'][w][x])
                    if w == "functions":
                        code.append(json_c['extra']['remote_store'][w][x])
        elif option == "1":
            correct = True
        else:
            option = input(json_q['error'])

    if flags["remote_store"]:
        correct = False
        print(json_q['code_questions']['captive_portal']['q0'])
        option = input(json_q['code_questions']['captive_portal']['q1'])
        while not correct:
            if option == "0":
                correct = True;
                flags['captive_portal'] = True;
                for w in json_c['extra']['captive_portal']:
                    for x in json_c['extra']['captive_portal'][w]:
                        if w == "libs":
                            libraries.append(json_c['extra']['captive_portal'][w][x])
                        if w == "vars":
                            codeVars.append(json_c['extra']['captive_portal'][w][x])
                        if w == "functions":
                            code.append(json_c['extra']['captive_portal'][w][x])
            elif option == "1":
                correct = True;
                captivePortal = False;
            else:
                option = input(json_q['error'])

# Base Functions
code.append(json_c['base']['functions']['start_sensor']["f0"])
if flags["remote_store"]:
    code.append(json_c['extra']['remote_store']['start_sensor']['f0'])
code.append(json_c['base']['functions']['start_sensor']["f1"])
if flags["remote_store"]:
    code.append(json_c['extra']['remote_store']['start_sensor']['f1'])
if flags["period"] > 0:
    code.append(json_c['base']['functions']['start_sensor']["f2"])
code.append(json_c['base']['functions']['start_sensor']["f3"])

code.append(json_c['base']['functions']['setup']["init"])
if flags["remote_store"]:
    code.append(json_c['extra']['remote_store']['setup']['s0'])
code.append(json_c['base']['functions']['setup']["end"])

code.append(json_c['base']['functions']['loop']["init"])
if flags["remote_store"]:
    code.append(json_c['extra']['remote_store']['loop']['l0'])
else:
    code.append(json_c['base']['functions']['loop']["body"])
code.append(json_c['base']['functions']['loop']["end"])

print("Answers collected!")

all = {"libraries":libraries, "codeVars":codeVars, "settings":settings, "code":code}
y = json.dumps(all)
y = json.loads(y)

outputFileName = "M5StickC_GSR_generated.ino"
if main:
    result = jinja2.Environment(loader=jinja2.FileSystemLoader('./')).get_template(template)
else:
    result = jinja2.Environment(loader=jinja2.FileSystemLoader('../../.')).get_template(template)
result = result.render(templ=y)

outFile = open(outputFileName, "w")
outFile.write(result)
outFile.close()

correct = False
print(json_gq['complete_process']['q0'])
option = input(json_gq['complete_process']['q1'])
while not correct:
    if option == "0":
        option = input(json_gq['complete_process']['q2'])
        while not correct:
            if option == "0":
                correct = True
                command = "python " + uploadPy + " " + outputFileName
                if sys.platform.startswith("win"):
                    os.system('cmd /c "' + command + '"')
                elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
                    os.system(command)
                else:
                    raise EnvironmentError("Unsupported platform")
            else:
                option = input(json_q['error'])
    elif option == "1":
        correct = True
    else:
        option = input(json_q['error'])