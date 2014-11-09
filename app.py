'''
curl -i -H "Content-Type: application/json" -X POST -d '{"team":"tsi","score":20}' http://localhost:5000/kukeri/teams
curl -i -H "Content-Type: application/json" -X PUT -d '{"score": 10}' http://localhost:5000/kukeri/teams/{team-name}
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


if __name__ == '__main__':
    app.run(debug=True)