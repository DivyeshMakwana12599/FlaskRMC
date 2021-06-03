import json

data = json.load(open('data.json'))



City = "Ahmedabad"
Area = "Area1"
Pipe = "Pipe4"

args = {
    "PH Value": 4,
    "ORPmeterValue": 90,
    "Temprature": 39.6,
    "Turbidity": 0.15,
    "Conductivity": 250
}

# data[City] = {Area:Pipe}
# data[City][Area] = {Pipe:args}

# print(data)

if not(City in data):
    data[City] = {Area:Pipe}
    data[City][Area] = {Pipe:args}
elif not(Area in data[City]):
    data[City][Area] = {Pipe:args}
elif not(Pipe in data[City][Area]):
    data[City][Area][Pipe] = args

print(data)

json.dump(data, open('data1.json','w'), indent=4)