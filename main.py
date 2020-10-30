import json
import jinja2
import os
import sys

with open('questions.json') as json_file:
    json_gq = json.load(json_file)

correct = False
if len(json_gq['language']) > 1:
    print("Select your language. Type your option.")
    i=1;
    languages = []
    for language in json_gq['language']:
        print(str(i)+") "+language)
        languages.append(language)
        i+=1

    while not correct:
        option = input()
        for i in range(len(json_gq['language'])):
            if str(i+1) == option:
                correct = True
                lang = languages[i]
        if not correct:
            option = input(json_gq['language']['en']['error'])
else:
    lang = "en"

json_gq = json_gq['language'][lang]
print(json_gq['introduction']['welcome'])
print(json_gq['sensors_list']['list_init'])

i = 1
sensors = []
for sensor in os.listdir("./Devices"):
    with open('./Devices/'+sensor+'/questions_sensor.json') as json_file:
        json_q = json.load(json_file)
        sensors.append(sensor)
        print(str(i) + ") " + json_q['language'][lang]['code_questions']['info']['name'])
    i += 1

option = input(json_gq['sensors_list']['i0'])
correct = False
while not correct:
    for x in range(i-1):
        if str(x+1) == option:
            correct = True
            command = "python ./Devices/"+sensors[x]+"/sensorGenerator.py " + lang
            if sys.platform.startswith("win"):
                os.system('cmd /c "' + command + '"')
            elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
                os.system(command)
            else:
                raise EnvironmentError("Unsupported platform")
    if not correct:
        option = input(json_gq['language'][lang]['error'])
