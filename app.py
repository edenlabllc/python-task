from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64))
    html_url = db.Column(db.String(256))
    language = db.Column(db.String(32))
    description = db.Column(db.String(2048), default='')
    stargazers_count = db.Column(db.Integer, default=0, index=True,
                                 unique=False)

    def __repr__(self):
        return '<Repository %s>' % self.full_name


class RepositorySchema(ModelSchema):
    class Meta:
        model = Repository


schema = RepositorySchema()
db.create_all()
db.session.commit()

import views

if __name__ == '__main__':
    app.run()
