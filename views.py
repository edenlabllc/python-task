from app import db, app, Repository, schema
from flask import request, abort, jsonify
from pagination import Pagination
from config import WITH_PAGINATION, DEFAULT_RESULTS_PER_PAGE


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

        query = pagination.paginate(Repository)

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
