from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from resources.user_resource import user_service
from services.schedule_service import ScheduleService
from utils.response_http_util import standard_response
from utils.auth_token import active_required
from config import db

schedule_bp = Blueprint('schedules', __name__)
schedule_service = ScheduleService(db.session)

@schedule_bp.route('/schedule', methods=['POST'])
@jwt_required()
@active_required
def post_schedule():
    data = request.get_json()
    schedules = data.get('schedules')
    user_id = get_jwt_identity()

    if not schedules:
        return standard_response(False, "Schedules data is required", 400)

    try:
        user = user_service.get_user_by_id(user_id)

        if user.role != 'admin':
            return standard_response(False, "Unauthorized: Only admins can create schedules", 403)

        created_schedules = schedule_service.create_schedule(user_id, schedules)
        return standard_response(True, "Schedules created successfully", 201,
                                  [schedule.to_dict() for schedule in created_schedules])
    except Exception as e:
        return standard_response(False, f"Error creating schedules: {str(e)}", 400)

@schedule_bp.route('/schedule', methods=['GET'])
@jwt_required()
@active_required
def get_schedules():
    user_id = get_jwt_identity()
    schedules = schedule_service.list_schedules(admin_id=user_id)

    if not schedules:
        return standard_response(True, "No schedules found", 200, [])

    return standard_response(True, "Schedules retrieved successfully", 200,
                              [schedule.to_dict() for schedule in schedules])

@schedule_bp.route('/schedule/<int:schedule_id>/available-times', methods=['GET'])
@jwt_required()
@active_required
def get_available_times(schedule_id):
    day_of_week = request.args.get('day_of_week')

    if not day_of_week:
        return standard_response(False, "Day of week is required", 400)

    try:
        available_times = schedule_service.get_available_times(schedule_id, day_of_week)
        return standard_response(True, "Available times retrieved successfully", 200,
                                  [schedule.to_dict() for schedule in available_times])
    except Exception as e:
        return standard_response(False, f"Error retrieving available times: {str(e)}", 400)
