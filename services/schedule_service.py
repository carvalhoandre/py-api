from repositories.schedule_repository import ScheduleRepository
from config import db

class ScheduleService:
    def __init__(self):
        self.repository = ScheduleRepository(db.session)

    def create_schedule(self, psychologist_id, date, start_time, end_time):
        return self.repository.create_schedule(psychologist_id, date, start_time, end_time)

    def get_available_slots(self, date):
        return self.repository.get_available_slots(date)
