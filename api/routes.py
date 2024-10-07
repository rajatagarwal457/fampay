from flask import Blueprint, request, jsonify
from api.models import Video
from api.utils import paginate_videos
from app import app
from services.youtube_service import fetch_videos_periodically
from sqlalchemy import or_

api_bp = Blueprint('api', __name__)

@api_bp.route('/update-term', methods=['POST'])
def update_term():
    fetch_videos_periodically(app, request.json['term'])
    return jsonify("search term updated")

@api_bp.route('/search', methods=['POST'])
def search_videos():

    query = request.json['query']
    page = request.json['page']
    per_page = request.json['per_page']

    if query:
        search_terms = query.split()
        search_condition = or_(*[
            or_(
                Video.title.ilike(f'%{term}%'),
                Video.description.ilike(f'%{term}%')
            )
            for term in search_terms
        ])
        videos = Video.query.filter(search_condition).order_by(Video.published_at.desc())
    else:
        videos = Video.query.order_by(Video.published_at.desc())

    paginated_videos = paginate_videos(videos, page, per_page)
    return jsonify(paginated_videos)