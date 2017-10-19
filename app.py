import os

from flask import Flask, jsonify, abort
from flask import request
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import and_

WITH_PAGINATION = os.environ.get('WITH_PAGINATION', 1)
DEFAULT_RESULTS_PER_PAGE = 15
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
    stargazers_count = db.Column(db.Integer, default=0, index=True, unique=False)

    def __repr__(self):
        return '<Repository %s>' % self.full_name


class RepositorySchema(ModelSchema):
    class Meta:
        model = Repository

schema = RepositorySchema()

db.create_all()
db.session.commit()


class Pagination:
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    def validate(self):
        """Validate own fields"""
        if self.page <= 0 or self.page > self.last:
            raise ValueError('Requested page not found')
        if self.per_page <= 0:
            raise ValueError('per_page parameter must be greater than 0')

    @property
    def next(self):
        """Get next page number"""
        if self.page == self.last:
            # Last page has to next page
            return None

        return self.page + 1

    @property
    def prev(self):
        """Get previous page number"""
        if self.page == 1:
            # First page has no prev page
            return None

        return self.page - 1

    @property
    def last(self):
        """Get last page number"""
        if self.total_count == 0:
            # First page will be the last in this case
            return 1

        return (self.total_count // self.per_page +
                (self.total_count % self.per_page > 0)) - 1

    @property
    def start_id(self):
        """Return lower id boundary"""
        return self.page * self.per_page + 1

    @property
    def end_id(self):
        """Return upper id boundary"""
        return self.page * self.per_page + self.per_page

    def paginate(self):
        """Build DB query with regards to requested pagination"""
        if self.page < 2:
            # Return results of first page
            query = (db.session
                     .query(Repository)
                     .filter(Repository.id <= self.per_page))
        else:
            query = (db.session
                     .query(Repository)
                     .filter(and_(Repository.id >= self.start_id,
                                  Repository.id <= self.end_id)))

        return query


def build_url(url, page):
    """Helper function to build pagination url"""
    if page is None:
        return ''

    return str(url) + '?page=' + str(page)


@app.route('/api/v1.0/repositories', methods=['GET'])
def get_repositories():
    order_by = request.args.get('order_by', 'stargazers_count')
    order = request.args.get('order', 'desc')

    result = {}

    if WITH_PAGINATION:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', DEFAULT_RESULTS_PER_PAGE))

        total_count = db.session.query(Repository).count()
        pagination = Pagination(page, per_page, total_count)

        try:
            pagination.validate()
        except ValueError:
            abort(404)

        query = pagination.paginate()

        result.update({
            'first': str(request.url_rule),
            'next': build_url(request.url_rule, pagination.next),
            'prev': build_url(request.url_rule, pagination.prev),
            'last': build_url(request.url_rule, pagination.last),
        })
    else:
        query = db.session.query(Repository)

    repositories = [schema.dump(x).data for x in
                    query.order_by(' '.join((order_by, order))).all()]
    result.update({'repositories': repositories})

    return jsonify(result)


@app.route('/api/v1.0/repositories/<int:repo_id>', methods=['GET'])
def get_repository(repo_id):
    repo = db.session.query(Repository).get(repo_id)

    if not repo:
        abort(404)

    return jsonify({'repository': schema.dump(repo).data})


@app.errorhandler(404)
def page_not_found(e):
    return str(e), 404


if __name__ == '__main__':
    app.run()
