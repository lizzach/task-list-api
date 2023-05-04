from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            id=cls.id,
            title=data_dict["title"],
            description=data_dict["description"]
        )

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description
        )
