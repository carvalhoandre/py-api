from bson import ObjectId
from flask import g, current_app

class AppointmentRepository:
    def __init__(self):
       pass

    @staticmethod
    def get_db():
        return current_app.config["mongo_db"]

    def create_appointment(self, appointment_data):
        """Create new appointment MongoDB."""
        schedule = g.mongo_db["schedules"].find_one({"_id": ObjectId(appointment_data["schedule_id"])})

        if not schedule:
            raise ValueError("Schedule not found")

        user = g.mongo_db["users"].find_one({"_id": ObjectId(appointment_data["user_id"])})

        if not user:
            raise ValueError("User not found")

        appointment_data["_id"] = ObjectId()  # Gera um ID único
        result = self.get_db()["appointment"].insert_one(appointment_data)

        return str(result.inserted_id)

    def get_appointments_by_status(self, status):
        """Get appointments by status."""
        return list(self.get_db()["appointment"].find({"status": status}))

    def get_appointment(self, schedule_id, appointment_date, start_time):
        """Get appointment by schedule and appointment date."""
        return self.get_db()["appointment"].find_one({
            "schedule_id": ObjectId(schedule_id),
            "appointment_date": appointment_date,
            "start_time": start_time
        })

    def get_by_id(self, appointment_id):
        """"Get appointment by appointment id."""""
        return self.get_db()["appointment"].find_one({"_id": ObjectId(appointment_id)})

    def get_appointments_for_date(self, schedule_id, appointment_date):
        """Get appointments by schedule and appointment date."""
        return list(self.get_db()["appointment"].find({
            "schedule_id": ObjectId(schedule_id),
            "appointment_date": appointment_date
        }))
