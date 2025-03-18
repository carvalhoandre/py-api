from bson import ObjectId

from repositories.schedule_repository import ScheduleRepository

class ScheduleService:
    def __init__(self):
        self.repository = ScheduleRepository()

    def create_schedule(self, admin_id, schedules):
        created_schedules = []
        for schedule in schedules:
            schedule_data = {
                "admin_id": ObjectId(admin_id),
                "work_days": schedule.get("work_days"),
                "start_time": schedule.get("start_time"),
                "end_time": schedule.get("end_time"),
                "session_duration_minutes": schedule.get("duration_minutes")
            }

            if not all(schedule_data.values()):
                raise ValueError(f"Invalid schedule data: {schedule_data}")

            created_schedule = self.repository.create_schedule(schedule_data)
            created_schedules.append(created_schedule)
        return created_schedules

    def list_schedules(self, admin_id=None):
        return self.repository.get_schedules(admin_id)

    def get_available_times(self, schedule_id, day_of_week):
        schedule = self.repository.get_schedules_for_date(schedule_id, day_of_week)
        if not schedule:
            return []

        return schedule
