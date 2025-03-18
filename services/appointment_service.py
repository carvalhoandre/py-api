from repositories.appointment_repository import AppointmentRepository
from bson import ObjectId

class AppointmentService:
    def __init__(self):
        self.repository = AppointmentRepository()

    def create_appointment(self, user_id, schedule_id, appointment_date, start_time, end_time):
        existing_appointment = self.repository.get_appointment(schedule_id, appointment_date, start_time)
        if existing_appointment:
            raise ValueError("Appointment already exists")

        appointment_data = {
            "user_id": ObjectId(user_id),
            "schedule_id": ObjectId(schedule_id),
            "appointment_date": appointment_date,
            "start_time": start_time,
            "end_time": end_time,
            "status": "pending"
        }

        return self.repository.create_appointment(appointment_data)

    def confirm_appointment(self, appointment_id, status):
        appointment = self.repository.get_by_id(appointment_id)
        if not appointment:
            return None

        self.repository.collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": status}}
        )

        return self.repository.get_by_id(appointment_id)
