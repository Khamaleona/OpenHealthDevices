import json
import jinja2
import os
import sys

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

libraries = []
constants = []
codeVars = []
settings = []
code = []
remoteStore = False
wifi = False
period = False
captivePortal = False
correct = False
option = ""
lang = ""

# if len(json_gq['language']) > 1:
#     print("Select your language. Type your option.")
#     i=1;
#     languages = []
#     for language in json_gq['language']:
#         print(str(i)+") "+language)
#         languages.append(language)
#         i+=1
#
#     while not correct:
#         option = input()
#         if 1 <= int(option) <= len(json_gq['language'])+1:
#             correct = True
#             lang = languages[int(option)-1]
#         else:
#             option = input(json_gq['language']['en']['error'])
# else:
#     lang = "en"

if len(sys.argv) == 2 and len(json_gq['language']) > 1:
    lang = str(sys.argv[0]) #storing language
else: lang = "en"

json_q = json_q['language'][lang]
print("Sensor selected: " + json_q['code_questions']['info']['name'])

json_gq = json_gq['language'][lang]
print(json_gq['introduction']['welcome'])

for lib in json_c['general_lib']:
    libraries.append(json_c['general_lib'][lib])

for var in json_c['sensor_vars']:
    codeVars.append(json_c['sensor_vars'][var])

option = input(json_q['code_questions']['measures']['q0'])
while not correct:
    if option == "1":
        option = input(json_q['code_questions']['measures']['q1'])
        while not correct:
            if option.isnumeric():
                period = int(option)
                correct = True
                constants.append(json_c['constants']['c0'])
                constants.append(json_c['constants']['c1'] + str(period))
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
        wifi = True
        correct = True
        for lib in json_c['wifi_lib']:
            libraries.append(json_c['wifi_lib'][lib])
    elif option == "1":
        wifi = False
        correct = True
    else:
        option = input(json_q['error'])

correct = False
option = input(json_q['code_questions']['remoteStore']['q0'])
while not correct:
    if option == "0":
        remoteStore = True
        correct = True
        for lib in json_c['storing_lib']:
            libraries.append(json_c['storing_lib'][lib])
    elif option == "1":
        remoteStore = False
        correct = True
    else:
        option = input(json_q['error'])

correct = False
print(json_q['code_questions']['captive_portal']['q0'])
option = input(json_q['code_questions']['captive_portal']['q1'])
while not correct:
    if option == "0":
        correct = True;
        captivePortal = True;
        for a in json_c['settings']['captive_portal']:
            settings.append(json_c['settings']['captive_portal'][a])
        if remoteStore:
            for a in json_c['settings']['remote_server']:
                settings.append(json_c['settings']['remote_server'][a])
            for a in json_c['settings']['wifi']:
                settings.append(json_c['settings']['wifi'][a])
    elif option == "1":
        correct = True;
        captivePortal = False;
    else:
        option = input(json_q['error'])

json_c = json_c['functions']

if wifi:
    for a in json_c['wifi']:
        code.append(json_c['wifi'][a])

if remoteStore:
    for a in json_c['remote_server']:
        code.append(json_c['remote_server'][a])
    for a in json_c['ip']:
        code.append(json_c['ip'][a])

if captivePortal:
    for a in json_c['captive_portal']:
        code.append(json_c['captive_portal'][a])

code.append(json_c['start_sensor']['base']['f0'])
if remoteStore:
    code.append(json_c['start_sensor']['remote_server']['f0'])
code.append(json_c['start_sensor']['base']['f1'])
if remoteStore:
    code.append(json_c['start_sensor']['remote_server']['f1'])
code.append(json_c['start_sensor']['base']['f2'])
if period > 0:
    code.append(json_c['start_sensor']['base']['f3'])
code.append(json_c['start_sensor']['base']['f4'])

if remoteStore:
    for a in json_c['credentials']:
        code.append(json_c['credentials'][a])

code.append(json_c['setup']['init'])
if captivePortal:
    code.append(json_c['setup']['portal'])
code.append(json_c['setup']['end'])

code.append(json_c['loop']['init'])
if captivePortal:
    code.append(json_c['loop']['portal'])
else:
    code.append(json_c['loop']['noPortal'])
code.append(json_c['loop']['end'])

print("Answers collected!")

all = {"libraries":libraries, "constants":constants, "codeVars":codeVars, "settings":settings, "code":code}
y = json.dumps(all)
y = json.loads(y)

outputFileName = "M5StickC_TMP117_generated.ino"
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
