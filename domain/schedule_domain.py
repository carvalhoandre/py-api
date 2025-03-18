from datetime import time
from bson import ObjectId

class Schedule:
    def __init__(self, admin_id, work_days, start_time, end_time, session_duration_minutes, _id=None):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.admin_id = ObjectId(admin_id)
        self.work_days = work_days
        self.start_time = time.fromisoformat(start_time) if isinstance(start_time, str) else start_time
        self.end_time = time.fromisoformat(end_time) if isinstance(end_time, str) else end_time
        self.session_duration_minutes = session_duration_minutes

    def to_dict(self):
        return {
            "_id": str(self._id),
            "admin_id": str(self.admin_id),
            "work_days": self.work_days,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "session_duration_minutes": self.session_duration_minutes
        }

    @staticmethod
    def from_dict(data):
        return Schedule(
            _id=data.get("_id"),
            admin_id=data["admin_id"],
            work_days=data["work_days"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            session_duration_minutes=data["session_duration_minutes"]
        )
