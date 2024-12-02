from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.appointment_service import AppointmentService
from utils.response_http_util import standard_response

appointment_bp = Blueprint('appointment', __name__)
appointment_service = AppointmentService()

@appointment_bp.route('/appointment', methods=['POST'])
@jwt_required()
def post_schedule():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    user_id = data.get('user_id')

    if not schedule_id or not user_id:
        return standard_response(False, "Invalid data", 400)

    appointment = appointment_service.create_appointment(schedule_id, user_id)

    if not appointment:
        return standard_response(False, "Slot not available", 400)

    return standard_response(True, "Schedule create successful", 201, appointment.to_dict())
