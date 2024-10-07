def paginate_videos(videos, page, per_page):
    paginated_videos = videos.paginate(page=page, per_page=per_page)
    return {
        'videos': [video.to_dict() for video in paginated_videos.items],
        'total': paginated_videos.total,
        'pages': paginated_videos.pages,
        'current_page': paginated_videos.page,
        'has_next': paginated_videos.has_next,
        'has_prev': paginated_videos.has_prev
    }