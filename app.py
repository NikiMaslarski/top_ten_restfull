'''
curl -i -H "Content-Type: application/json" -X POST -d '{"team":"tsi","score":20}' http://localhost:5000/kukeri/teams
curl -i -H "Content-Type: application/json" -X PUT -d '{"score": 10}' http://localhost:5000/kukeri/teams/{team-name}

curl -i -H "Content-Type: application/json" -X POST -d '{"hostname":"tozi", "ipadr":"192.168.0.1", "port": 20}' http://localhost:5000/kukeri/hosts

'''



from flask import Flask, jsonify, make_response, request
import json
import querry_holder 
from flask import abort
import sqlite3

app = Flask(__name__)

#teams = [("tep",1), ("tebd",2), ("tegs",0)]

dataBase = querry_holder.DBHolder()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def convert_to_dict(team):
    return {"team":team[0].encode('ascii', 'ignore'),"score":team[1]}


@app.route('/kukeri/teams', methods=['GET'])
def get_tasks():

    data = dataBase.get_top10()
    
    result = []
#  teams.sort(key=lambda x: x[1])
    for item in data:
        result.append(convert_to_dict(item))

    return jsonify({"Teams":result})


@app.route('/kukeri/teams/<string:team>', methods=['GET'])
def get_score(team):
    result = dataBase.get_score(team)


    return str(result)


@app.route('/kukeri/teams/<string:team>', methods=['PUT'])
def update_score(team):
    if dataBase.update_score(team, request.json['score']):
        return 'success\n'

    return "Team doesn't exist\n"


@app.route('/kukeri/teams', methods = ['POST'])
def create_task():
    if dataBase.add_score_to_ladder(request.json['team'], 
        request.json['score']):
        return "Team already exists\n"
    return "success\n"


#-------------------------

def convert_host_dict(host):
    return {"hostname":host[0].encode('ascii', 'ignore'),
    "ipadr":host[1].encode('ascii', 'ignore'),
    "port":host[2]}


@app.route('/kukeri/hosts', methods=['GET'])
def get_hosts():

    data = dataBase.get_hosts()
    
    result = []
#  teams.sort(key=lambda x: x[1])
    for item in data:
        result.append(convert_host_dict(item))

    return jsonify({"Hosts":result})


@app.route('/kukeri/hosts/<string:hostname>', methods=['GET'])
def get_host_info(hostname):
    result = dataBase.get_host_info(hostname)

    if result is None:
        return "No such host"
    return json.dumps(convert_host_dict(result))


@app.route('/kukeri/hosts/<string:team>', methods=['PUT'])
def update_host(team):
    # if dataBase.update_host(team,
    #     request.json['score'], request.json[]):
    #     return 'success\n'

    return "Host doesn't exist\n"


@app.route('/kukeri/hosts', methods = ['POST'])
def create_host():
    if dataBase.create_host(request.json['hostname'], 
        request.json['ipadr'], request.json['port']):
        return "Host already exists\n"
    return "success\n"


if __name__ == '__main__':
    app.run(debug=True)