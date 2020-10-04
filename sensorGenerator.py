import json
import jinja2

# load json from file
with open('questions.json') as json_file:
    json_q = json.load(json_file)

with open('code.json') as json_file:
    json_c = json.load(json_file)

# Load and make questions
libraries = []
constants = []
codeVars = []
settings = []
code = []

remoteStore = False
frecuency = False
captivePortal = False
sensorType = 0

for lib in json_c['general_lib']:
    libraries.append(json_c['general_lib'][lib])

correct = False
print(json_q['introduction']['welcome'])
print(json_q['sensors_list']['list_init'])
i=1
for fileEntry in json_q['sensors_list']['elements']:
    print("\t(" + str(i) + ") " + fileEntry['name'] + ": " + fileEntry['description'])
    i+=1

while not correct:
    print(json_q['sensors_list']['i0'] + "\n")
    option = input(json_q['sensors_list']['i1'])
    if 1 <= int(option) <= 4:
        sensorType = int(option)
        correct = True
        if int(option) == 1:
            libraries.append(json_c['sensor_lib']['s0'])
            codeVars.append(json_c['sensor_vars']['s0'])
        elif int(option) == 2:
            libraries.append(json_c['sensor_lib']['s1'])
            for a in json_c['sensor_vars']['s1']:
                codeVars.append(json_c['sensor_vars']['s1'][a])
        elif int(option) == 3:
            for a in json_c['sensor_vars']['s2']:
                codeVars.append(json_c['sensor_vars']['s2'][a])
        elif int(option) == 4:
            libraries.append(json_c['sensor_lib']['other'])
            codeVars.append(json_c['sensor_vars']['other'])
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
            frecuency = True
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
    if sensorType == 1:
        code.append(json_c['code_blocks']['remote_server']['sensors']['titles']['title0'])
        code.append(json_c['code_blocks']['remote_server']['common']['c0'])
        code.append(json_c['code_blocks']['remote_server']['common']['c1'])
        code.append(json_c['code_blocks']['remote_server']['sensors']['jsons']['json0'])
        code.append(json_c['code_blocks']['remote_server']['common']['c2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c3'])
    elif sensorType == 2:
        code.append(json_c['code_blocks']['remote_server']['sensors']['titles']['title1'])
        code.append(json_c['code_blocks']['remote_server']['common']['c0'])
        code.append(json_c['code_blocks']['remote_server']['common']['c1'])
        code.append(json_c['code_blocks']['remote_server']['sensors']['jsons']['json2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c1'])
        code.append(json_c['code_blocks']['remote_server']['sensors']['jsons']['json3'])
        code.append(json_c['code_blocks']['remote_server']['common']['c4'])
        code.append(json_c['code_blocks']['remote_server']['sensors']['s2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c3'])
    elif sensorType == 3:
        code.append(json_c['code_blocks']['remote_server']['sensors']['titles']['title2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c0'])
        code.append(json_c['code_blocks']['remote_server']['common']['c1'])
        code.append(json_c['code_blocks']['remote_server']['sensors']['jsons']['json1'])
        code.append(json_c['code_blocks']['remote_server']['common']['c2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c3'])
    else:
        code.append(json_c['code_blocks']['remote_server']['sensors']['titles']['title3'])
        code.append(json_c['code_blocks']['remote_server']['common']['c0'])
        code.append(json_c['code_blocks']['remote_server']['common']['c1'])
        code.append(json_c['code_blocks']['remote_server']['sensors']['jsons']['json4'])
        code.append(json_c['code_blocks']['remote_server']['common']['c2'])
        code.append(json_c['code_blocks']['remote_server']['common']['c3'])

code.append(json_c['code_blocks']['start_sensor']['common']['f0'])
if remoteStore:
    code.append(json_c['code_blocks']['start_sensor']['common']['f3'])
if sensorType == 1:
    code.append(json_c['code_blocks']['start_sensor']['initialize']['i0'])
    if remoteStore:
        code.append(json_c['code_blocks']['start_sensor']['webserver']['w0'])
    if frecuency > 0:
        code.append(json_c['code_blocks']['start_sensor']['common']['f1'])
    code.append(json_c['code_blocks']['start_sensor']['body']['b0'])
    code.append(json_c['code_blocks']['start_sensor']['common']['f2'])
elif sensorType == 2:
    code.append(json_c['code_blocks']['start_sensor']['initialize']['i1'])
    if remoteStore:
        code.append(json_c['code_blocks']['start_sensor']['webserver']['w1'])
    code.append(json_c['code_blocks']['start_sensor']['body']['b1'])
    if frecuency > 0:
        code.append(json_c['code_blocks']['start_sensor']['common']['f1'])
    code.append(json_c['code_blocks']['start_sensor']['common']['f2'])
elif sensorType == 3:
    code.append(json_c['code_blocks']['start_sensor']['initialize']['i2'])
    if remoteStore:
        code.append(json_c['code_blocks']['start_sensor']['webserver']['w2'])
    if frecuency > 0:
        code.append(json_c['code_blocks']['start_sensor']['body']['b2'])
    code.append(json_c['code_blocks']['start_sensor']['common']['f2'])
else:
    code.append(json_c['code_blocks']['start_sensor']['initialize']['i3'])
    if remoteStore:
        code.append(json_c['code_blocks']['start_sensor']['webserver']['w3'])
    if frecuency > 0:
        code.append(json_c['code_blocks']['start_sensor']['common']['f1'])
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

outputFileName = "M5StickC_" + json_q['sensors_list']['elements'][sensorType-1]['name'] + ".ino"
result = jinja2.Environment(loader=jinja2.FileSystemLoader('./')).get_template('sensor-template.ino')
result = result.render(templ=y)
#print(result)

outFile = open(outputFileName, "w")
outFile.write(result)
outFile.close()