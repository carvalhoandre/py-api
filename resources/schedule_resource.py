from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from resources.user_resource import user_service
from services.schedule_service import ScheduleService
from utils.response_http_util import standard_response

schedule_bp = Blueprint('schedules', __name__)
schedule_service = ScheduleService()

@schedule_bp.route('/schedule', methods=['POST'])
@jwt_required()
def post_schedule():
    data = request.get_json()
    created_by = data.get('created_by')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not created_by or not date or not start_time or not end_time:
        return standard_response(False, "Invalid data", 400)

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except ValueError:
        return standard_response(False, "Invalid user ID", 400)

    user = user_service.get_user_by_id(user_id)

    if user.role != 'admin':
        return standard_response(False, "Unauthorized: Only admins can create schedules", 403)

    schedule = schedule_service.create_schedule(created_by, date, start_time, end_time)

    if not schedule:
        return standard_response(False, "Error in create schedule", 400)

    return standard_response(True, "Schedule create successful", 201, schedule.to_dict())

@schedule_bp.route('/schedule', methods=['GET'])
@jwt_required()
def get_available_slots():
    schedules = schedule_service.get_available_slots()

    if not schedules:
        return standard_response(True, "No available slots found", 200, [])


    return standard_response(True, "Available slots retrieved successfully", 200, [schedule.to_dict() for schedule in schedules]
)