from config import db

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    psychologist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    available = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "psychologist_id": self.psychologist_id,
            "date": self.date.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "available": self.available
        }