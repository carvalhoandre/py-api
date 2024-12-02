from domain.schedule_domain import Schedule

class ScheduleRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_schedule(self, created_by , date, start_time, end_time):
        schedule = Schedule(
            created_by=created_by,
            date=date,
            start_time=start_time,
            end_time=end_time,
            available=True
        )

        self.db_session.add(schedule)
        self.db_session.commit()
        return schedule

    def get_available_slots(self):
        return self.db_session.query(Schedule).filter_by(available=True).all()