from repositories.schedule_repository import ScheduleRepository
from config import db

class ScheduleService:
    def __init__(self, db_session):
        self.repository = ScheduleRepository(db_session)

    def create_schedule(self, admin_id, schedules):
        created_schedules = []
        for schedule in schedules:
            schedule_data = {
                "user_id": admin_id,
                "day_of_week": schedule.get('day_of_week'),
                "start_time": schedule.get('start_time'),
                "end_time": schedule.get('end_time'),
                "duration_minutes": schedule.get('duration_minutes')
            }

            if not all(schedule_data.values()):
                raise ValueError(f"Invalid schedule data: {schedule_data}")

            created_schedule = self.repository.create_schedule(schedule_data)
            created_schedules.append(created_schedule)
        return created_schedules

    def list_schedules(self, admin_id=None):
        return self.repository.get_schedules(admin_id)

    def get_available_times(self, schedule_id, day_of_week):
        return self.repository.get_schedules_for_date(schedule_id, day_of_week)
