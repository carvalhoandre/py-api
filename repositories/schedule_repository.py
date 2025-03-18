from bson import ObjectId
from flask import g, current_app

from domain.schedule_domain import Schedule

class ScheduleRepository:
    def __init__(self):
        pass

    @staticmethod
    def get_db():
        return current_app.config["mongo_db"]

    def create_schedule(self, schedule_data):
        schedule = Schedule(**schedule_data)
        result = self.get_db()["schedule"].insert_one(schedule.to_dict())

        return str(result.inserted_id)

    def get_schedules(self, admin_id=None):
        query = {}

        if admin_id:
            query["admin_id"] = ObjectId(admin_id)

        schedules = self.get_db()["schedule"].find(query)

        return [Schedule.from_dict(schedule) for schedule in schedules]

    def get_schedules_for_date(self, schedule_id, day_of_week):
        schedule = self.get_db()["schedule"].find_one({"_id": ObjectId(schedule_id)})

        if not schedule:
            return None

        if day_of_week not in schedule["work_days"]:
            return None

        return Schedule.from_dict(schedule)
