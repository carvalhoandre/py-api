from domain.schedule_domain import Schedule

class ScheduleRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_schedule(self, schedule_data):
        schedule = Schedule(**schedule_data)
        self.db_session.add(schedule)
        self.db_session.commit()
        return schedule

    def get_schedules(self, admin_id=None):
        query = Schedule.query
        if admin_id:
            query = query.filter_by(user_id=admin_id)
        return query.all()

    def get_schedules_for_date(self, schedule_id, day_of_week):
        return Schedule.query.filter_by(id=schedule_id, day_of_week=day_of_week).all()
