from flask import Blueprint, request, jsonify
from models import RealTimeData, ForecastData
from sqlalchemy import func

log_blueprint = Blueprint('log', __name__)

@log_blueprint.route('/log', methods=['GET'])
def get_logs():
    date = request.args.get('date')
    data_type = request.args.get('type')

    if data_type == 'real_time':
        logs = RealTimeData.query.filter(func.date(RealTimeData.timestamp) == date).all()
        result = [
            {
                "timestamp": r.timestamp.isoformat(),
                "generation": r.generation,
                "charging": r.charging,
                "discharging": r.discharging,
                "load_amount": r.load_amount
            }
            for r in logs
        ]
    elif data_type == 'forecast':
        logs = ForecastData.query.filter(func.date(ForecastData.fcstDateTime) == date).all()
        result = [
            {
                "fcstDateTime": f.fcstDateTime.isoformat(),
                "powergen": f.powergen,
                "cum_powergen": f.cum_powergen,
                "irrad": f.irrad,
                "temp": f.temp,
                "wind": f.wind
            }
            for f in logs
        ]
    else:
        return jsonify({"message": "Invalid data type"}), 400

    return jsonify({"type": data_type, "logs": result}), 200
