from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.appointment_service import AppointmentService
from utils.response_http_util import standard_response

appointment_bp = Blueprint('appointment', __name__)
appointment_service = AppointmentService()

@appointment_bp.route('/appointment', methods=['POST'])
@jwt_required()
def post_appointment():
    data = request.get_json()

    user_id = get_jwt_identity()
    schedule_id = data.get('schedule_id')
    appointment_date = data.get('appointment_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not (schedule_id and appointment_date and start_time and end_time):
        return standard_response(False, "Invalid data", 400)

    try:
        appointment = appointment_service.create_appointment(
            user_id=user_id,
            schedule_id=schedule_id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time
        )
        return standard_response(True, "Appointment created successfully", 201, appointment.to_dict())
    except ValueError as e:
        return standard_response(False, str(e), 400)
    except Exception as e:
        return standard_response(False, f"Unexpected error: {str(e)}", 500)

@appointment_bp.route('/appointment/<int:appointment_id>/confirm', methods=['PATCH'])
@jwt_required()
def confirm_appointment(appointment_id):
    data = request.get_json()
    status = data.get('status')

    if not status:
        return standard_response(False, "Status is required", 400)

    try:
        appointment = appointment_service.confirm_appointment(appointment_id, status)
        return standard_response(True, "Appointment status updated successfully", 200, appointment.to_dict())
    except ValueError as e:
        return standard_response(False, str(e), 400)
    except Exception as e:
        return standard_response(False, f"Unexpected error: {str(e)}", 500)
