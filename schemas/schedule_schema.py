from marshmallow import Schema, fields

class ScheduleSchema(Schema):
    admin_id = fields.Int(required=True)
    day_of_week = fields.Str(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    duration_minutes = fields.Int(required=True)
