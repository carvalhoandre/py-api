from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.schedule_service import ScheduleService
from utils.response_http_util import standard_response

schedule_bp = Blueprint('schedules', __name__)
schedule_service = ScheduleService()

@schedule_bp.route('/schedule', methods=['POST'])
@jwt_required()
def post_schedule():
    data = request.get_json()
    psychologist_id = data.get('psychologist_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not psychologist_id or not date or not start_time or not end_time:
        return standard_response(False, "Invalid data", 400)

    schedule = schedule_service.create_schedule(psychologist_id, date, start_time, end_time)

    if not schedule:
        return standard_response(False, "Error in create schedule", 400)

    return standard_response(True, "Schedule create successful", 201, schedule)

@schedule_bp.route('/schedule', methods=['GET'])
@jwt_required()
def get_available_slots():
    data = request.get_json()
    date = data.get('date')

    if not date:
        return standard_response(False, "Invalid data", 400)

    schedules = schedule_service.get_available_slots(data)

    if not schedules:
        return standard_response(False, "Error in create schedule", 400)

    return standard_response(True, f"Available slots in {data}", 200, schedules)