from flask import Flask, request, jsonify
import requests
from flask_mongoengine import MongoEngine
from model import Data
import json

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://vasia:123vasia@ds161121.mlab.com:61121/vasia',  # NOQA
}
MongoEngine(app)

@app.route('/')
def get_all():
    message = [data for data in Data.objects()]
    return jsonify({"response" : message})

@app.route('/add_new_language/<language>')
def add_new_language(language):
    request_url = 'https://api.github.com/search/repositories?q=rest+language:{}&sort=stars'.format(language)
    a = requests.get(request_url)

    the_dict = json.loads(a.text)
    posts = the_dict['items']
    for post in posts:
        data = Data(full_name = post['full_name'], html_url = post['html_url'], description = post['description'],stargazers_count = post['stargazers_count'],language =post['language'])
        data.save()

    return 'added'

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'This page not avalible: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/<language>')
def get_by_langue(language):
    message = [data for data in Data.objects(language = language)]
    return jsonify({"response" : message})


@app.route('/<language>/<full_name>')
def get_by_langue_and_name(language, full_name):
    message = [data for data in Data.objects(language = language, full_name = full_name)]
    return jsonify({"response" : message})


if __name__ == '__main__':
    app.run()
