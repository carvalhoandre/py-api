from bson import ObjectId
from datetime import datetime

class Appointment:
    def __init__(self, user_id, schedule_id, appointment_date, start_time, end_time, status="pending", _id=None):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.user_id = ObjectId(user_id)
        self.schedule_id = ObjectId(schedule_id)
        self.appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d")
        self.start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        self.end_time = datetime.strptime(end_time, "%H:%M:%S").time()
        self.status = status

    def to_dict(self):
        """Update object attributes for MongoDB"""
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "schedule_id": self.schedule_id,
            "appointment_date": self.appointment_date.strftime("%Y-%m-%d"),
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """Create object from MongoDB dictionary"""
        return Appointment(
            _id=str(data["_id"]),
            user_id=str(data["user_id"]),
            schedule_id=str(data["schedule_id"]),
            appointment_date=data["appointment_date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            status=data.get("status", "pending")
        )
