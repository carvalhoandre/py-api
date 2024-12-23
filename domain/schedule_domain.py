from config import db

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    admin_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_days = db.Column(db.String(7), default="[0,1,1,1,1,1,0]")
    start_time = db.Column(db.Time, default="08:00:00")
    end_time = db.Column(db.Time,  default="16:00:00")
    session_duration_minutes = db.Column(db.Integer, default=50)

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id ": self.admin_id ,
            "work_days": self.work_days,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "session_duration_minutes": self.session_duration_minutes
        }
