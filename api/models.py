from database.db import db

class Video(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    published_at = db.Column(db.DateTime, nullable=False)
    thumbnail_url = db.Column(db.String(255))
    channel_id = db.Column(db.String(255), nullable=False)
    channel_title = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'published_at': self.published_at.isoformat(),
            'thumbnail_url': self.thumbnail_url,
            'channel_id': self.channel_id,
            'channel_title': self.channel_title
        }