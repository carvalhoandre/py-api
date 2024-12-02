from repositories.appointment_repository import AppointmentRepository
from config import db

class AppointmentService:
    def __init__(self):
        self.repository = AppointmentRepository(db.session)

    def create_appointment(self, schedule_id, user_id):
        return self.repository.create_appointment(schedule_id, user_id)
