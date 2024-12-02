from domain.appointment_domain import Appointment
from domain.schedule_domain import Schedule
from domain.user_domain import User


class AppointmentRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_appointment(self, schedule_id, user_id):
        schedule = self.db_session.query(Schedule).get(schedule_id)

        if not schedule or not schedule.available:
            return None

        user = self.db_session.query(User).get(user_id)

        if not user:
            return None

        appointment = Appointment(schedule_id =  schedule_id, user_id = user_id)

        schedule.available = False
        self.db_session.add(appointment)
        self.db_session.commit()

        return appointment
    