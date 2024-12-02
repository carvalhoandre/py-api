from repositories.schedule_repository import ScheduleRepository
from config import db

class ScheduleService:
    def __init__(self):
        self.repository = ScheduleRepository(db.session)

    def create_schedule(self, created_by, date, start_time, end_time):
        return self.repository.create_schedule(created_by, date, start_time, end_time)

    def get_available_slots(self):
        return self.repository.get_available_slots()
