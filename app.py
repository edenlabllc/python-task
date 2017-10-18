import os
from flask import Flask, jsonify, abort
from flask import request
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema

DB_NAME = 'db.sqlite3'
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
db = SQLAlchemy(app)


class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64))
    html_url = db.Column(db.String(256))
    language = db.Column(db.String(32))
    description = db.Column(db.String(2048), default=None)
    stargazers_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Repository %s>' % self.full_name


class RepositorySchema(ModelSchema):
    class Meta:
        model = Repository

schema = RepositorySchema()

db.create_all()
db.session.commit()


@app.route('/api/v1.0/repositories', methods=['GET'])
def get_repositories():
    order_by = request.args.get('order_by', 'stargazers_count')
    order = request.args.get('order', 'asc')

    return jsonify({'repositories':
                    [schema.dump(x).data for x in
                     db.session.query(Repository).order_by(' '.join((
                         order_by, order))).all()]})


@app.route('/api/v1.0/repositories/<int:repo_id>', methods=['GET'])
def get_repository(repo_id):
    repo = db.session.query(Repository).get(repo_id)

    if not repo:
        abort(404)

    return jsonify({'repository': schema.dump(repo).data})


if __name__ == '__main__':
    app.run()
