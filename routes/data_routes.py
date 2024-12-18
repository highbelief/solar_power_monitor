from flask import Blueprint, jsonify
from models import RealTimeData, ForecastData

data_blueprint = Blueprint('data', __name__)

@data_blueprint.route('/real_time', methods=['GET'])
def get_real_time_data():
    data = RealTimeData.query.order_by(RealTimeData.timestamp.desc()).all()
    result = [
        {
            "timestamp": r.timestamp.isoformat(),
            "generation": r.generation,
            "charging": r.charging,
            "discharging": r.discharging,
            "load_amount": r.load_amount
        }
        for r in data
    ]
    return jsonify(result), 200

@data_blueprint.route('/forecast', methods=['GET'])
def get_forecast_data():
    data = ForecastData.query.order_by(ForecastData.fcstDateTime.desc()).all()
    result = [
        {
            "fcstDateTime": f.fcstDateTime.isoformat(),
            "powergen": f.powergen,
            "cum_powergen": f.cum_powergen,
            "irrad": f.irrad,
            "temp": f.temp,
            "wind": f.wind
        }
        for f in data
    ]
    return jsonify(result), 200
