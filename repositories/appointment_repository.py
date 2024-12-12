from domain.appointment_domain import Appointment
from domain.schedule_domain import Schedule
from domain.user_domain import User


class AppointmentRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_appointment(self, appointment_data):
        schedule = self.db_session.query(Schedule).get(appointment_data['schedule_id'])

        if not schedule:
            raise ValueError("Schedule not found")

        user = self.db_session.query(User).get(appointment_data['user_id'])

        if not user:
            raise ValueError("User not found")

        appointment = Appointment(**appointment_data)

        self.db_session.add(appointment)
        self.db_session.commit()

        return appointment

    def get_appointments_by_status(self, status):
        return Appointment.query.filter_by(status=status).all()

    def get_appointment(self, schedule_id, appointment_date, start_time):
        return Appointment.query.filter_by(
            schedule_id=schedule_id,
            appointment_date=appointment_date,
            start_time=start_time
        ).first()

    def get_by_id(self, appointment_id):
        return Appointment.query.get(appointment_id)

    def get_appointments_for_date(self, schedule_id, appointment_date):
        return Appointment.query.filter_by(schedule_id=schedule_id, appointment_date=appointment_date).all()
