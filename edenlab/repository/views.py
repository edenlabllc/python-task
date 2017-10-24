from flask import request, jsonify, Blueprint, current_app, abort

from edenlab.repository.models import Repository, RepositorySchema
from edenlab.repository.pagination import Pagination
from edenlab.extensions import db


blueprint = Blueprint('repository', __name__, url_prefix='/repositories')


def build_url(url, page):
    """Helper function to build pagination url"""
    if page is None:
        return ''

    return str(url) + '?page=' + str(page)


@blueprint.route('/', methods=['GET'])
def get_repositories():
    order_by = request.args.get('order_by', 'stargazers_count')
    order = request.args.get('order', 'desc')

    result = {}

    if current_app.config['PAGINATION_ENABLED']:
        page = int(request.args.get('page', 1))
        per_page_default = current_app.config['DEFAULT_RESULTS_PER_PAGE']
        per_page = int(request.args.get('per_page', per_page_default))

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
        query = Repository.query

    query = query.order_by(' '.join((order_by, order)))
    repositories = [RepositorySchema().dump(x).data for x in
                    query.all()]
    result.update({'repositories': repositories})

    return jsonify(result)


@blueprint.route('/<int:repo_id>', methods=['GET'])
def get_repository(repo_id):
    repo = db.session.query(Repository).get(repo_id)

    if not repo:
        abort(404)

    return jsonify({'repository': RepositorySchema().dump(repo).data})
