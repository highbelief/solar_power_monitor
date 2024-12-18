from database import db

class RealTimeData(db.Model):
    __tablename__ = 'real_time_data'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, unique=True)
    generation = db.Column(db.Float)
    charging = db.Column(db.Float)
    discharging = db.Column(db.Float)
    reactive_power = db.Column(db.Float)   # 무효 전력
    power_factor = db.Column(db.Float)     # 역률
    frequency = db.Column(db.Float)        # 주파수
    rs_voltage = db.Column(db.Float)       # RS 선간 전압
    ss_voltage = db.Column(db.Float)       # SS 선간 전압
    load_amount = db.Column(db.Float)      # 부하량

    def to_dict(self):
        """객체를 JSON 직렬화 가능한 형태로 변환"""
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class ForecastData(db.Model):
    __tablename__ = 'forecast_data'
    id = db.Column(db.Integer, primary_key=True)
    fcstDateTime = db.Column(db.DateTime, nullable=False, unique=True)
    powergen = db.Column(db.Float, nullable=False)
    cum_powergen = db.Column(db.Float)
    irrad = db.Column(db.Float)
    temp = db.Column(db.Float)
    wind = db.Column(db.Float)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
