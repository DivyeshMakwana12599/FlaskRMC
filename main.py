from flask import Flask
from flask_restful import Api, Resource, reqparse
import json


app = Flask(__name__)
api = Api(app)
data = json.load(open("data.json"))
data_status = data

data_put_args = reqparse.RequestParser()
data_post_args = reqparse.RequestParser()

# args for put method
data_put_args.add_argument(
    "PH Value", type=float, help="Send the PH value from the Sensor", required=False
)
data_put_args.add_argument(
    "ORPmeterValue",
    type=float,
    help="Send the ORP meter value from the Sensor",
    required=False,
)
data_put_args.add_argument(
    "Temperature",
    type=float,
    help="Send the Temperature value from the Sensor",
    required=True,
)
data_put_args.add_argument(
    "Turbidity",
    type=float,
    help="Send the Turbidity value from the Sensor",
    required=False,
)
data_put_args.add_argument(
    "Conductivity",
    type=float,
    help="Send the Conductivity from the Sensor",
    required=False,
)

# args for post method
data_post_args.add_argument(
    "PH Value", type=float, help="Send the PH value from the Sensor", required=False
)
data_post_args.add_argument(
    "ORPmeterValue",
    type=float,
    help="Send the ORP meter value from the Sensor",
    required=False,
)
data_post_args.add_argument(
    "Temperature",
    type=float,
    help="Send the Temperature value from the Sensor",
    required=True,
)
data_post_args.add_argument(
    "Turbidity",
    type=float,
    help="Send the Turbidity value from the Sensor",
    required=False,
)
data_post_args.add_argument(
    "Conductivity",
    type=float,
    help="Send the Conductivity from the Sensor",
    required=False,
)


def checkStatus():
    global data_status, data
    data_status = data
    for city in data:
        for area in data[city]:
            for pipe in data[city][area]:
                if "PH Value" in data[city][area][pipe]:
                    if (
                        data[city][area][pipe]["PH Value"] < 6
                        or data[city][area][pipe]["PH Value"] > 8
                    ):
                        data_status[city][area][pipe] = False
                        return
                if "ORPmeterValue" in data[city][area][pipe]:
                    if (
                        data[city][area][pipe]["ORPmeterValue"] < 80
                        or data[city][area][pipe]["ORPmeterValue"] > 100
                    ):
                        data_status[city][area][pipe] = False
                        return
                if "Temperature" in data[city][area][pipe]:
                    if (
                        data[city][area][pipe]["Temperature"] < 30
                        or data[city][area][pipe]["Temperature"] > 40
                    ):
                        data_status[city][area][pipe] = False
                        return
                if "Turbidity" in data[city][area][pipe]:
                    if (
                        data[city][area][pipe]["Turbidity"] < 0.14
                        or data[city][area][pipe]["Turbidity"] > 0.20
                    ):
                        data_status[city][area][pipe] = False
                        return
                if "Conductivity" in data[city][area][pipe]:
                    if (
                        data[city][area][pipe]["Conductivity"] < 200
                        or data[city][area][pipe]["Conductivity"] > 260
                    ):
                        data_status[city][area][pipe] = False
                        return
                data_status[city][area][pipe] = True


class WelcomePage(Resource):
    def get(self):
        return "Welcome to Muncipal Corpration", 200


class MuncipalCorprationGet(Resource):
    def get(self, City, Area):
        return {(City + " " + Area): data_status[City][Area]}, 200


class MuncipalCorprationPutPostDel(Resource):
    def put(self, City, Area, Pipe):
        global data
        args = data_put_args.parse_args()
        for Value in args:
            data[City][Area][Pipe][Value] = args[Value]
        json.dump(data, open("data.json", "w"))
        checkStatus()
        data = json.load(open("data.json"))
        return {City + " " + Area + " " + Pipe: data[City][Area][Pipe]}, 201

    def post(self, City, Area, Pipe):
        global data
        args = data_post_args.parse_args()
        if not (City in data):
            data[City] = {Area: Pipe}
            data[City][Area] = {Pipe: args}
        elif not (Area in data[City]):
            data[City][Area] = {Pipe: args}
        elif not (Pipe in data[City][Area]):
            data[City][Area][Pipe] = args
        json.dump(data, open("data.json", "w"))
        checkStatus()
        data = json.load(open("data.json"))
        return {City + " " + Area + " " + Pipe: data[City][Area][Pipe]}, 201

    def delete(self, City, Area, Pipe):
        global data
        if Pipe in data[City][Area]:
            del data[City][Area][Pipe]
        json.dump(data, open("data.json", "w"))
        checkStatus()
        data = json.load(open("data.json"))
        return City + " " + Area + " " + Pipe + " Deleted", 200


api.add_resource(MuncipalCorprationGet, "/<string:City>/<string:Area>")
api.add_resource(
    MuncipalCorprationPutPostDel, "/<string:City>/<string:Area>/<string:Pipe>"
)
api.add_resource(WelcomePage, "/")


if __name__ == "__main__":
    checkStatus()
    data = json.load(open("data.json"))
    app.run(debug=True)
