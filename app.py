from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from config import Config
from database import db
from models import RealTimeData, ForecastData
from datetime import datetime, timedelta
from sqlalchemy import func
import pytz

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 로그인 사용자 정보 (하드코딩)
USERS = {"admin": "password"}

# 대한민국 시간대 설정
KST = timedelta(hours=9)

@app.route('/')
def index():
    return redirect(url_for('login'))

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

# 대한민국 시간대 설정
KST = pytz.timezone('Asia/Seoul')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # UTC -> KST 변환
    now_kst = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(KST)
    start_of_day = now_kst.replace(hour=0, minute=0, second=0, microsecond=0)

    # 하루치 데이터 가져오기
    real_time_data = RealTimeData.query.filter(RealTimeData.timestamp >= start_of_day).all()
    forecast_data = ForecastData.query.filter(ForecastData.fcstDateTime >= start_of_day).all()

    # 최신 데이터 가져오기
    latest_data = RealTimeData.query.order_by(RealTimeData.timestamp.desc()).first()

    # 시간 변환 함수 (KST로 변환)
    # KST로 변환하는 함수
    def to_kst(data):
        result = data.to_dict()
        if hasattr(data, 'timestamp') and data.timestamp:  # RealTimeData 처리
            result['timestamp'] = data.timestamp.astimezone(KST).strftime("%Y-%m-%d %H:%M:%S")
        if hasattr(data, 'fcstDateTime') and data.fcstDateTime:  # ForecastData 처리
            result['fcstDateTime'] = data.fcstDateTime.astimezone(KST).strftime("%Y-%m-%d %H:%M:%S")
        return result

    real_time_data_serialized = [to_kst(data) for data in real_time_data]
    forecast_data_serialized = [to_kst(data) for data in forecast_data]
    latest_data_serialized = to_kst(latest_data) if latest_data else {}

    return render_template('dashboard.html',
                           real_time_data=real_time_data_serialized,
                           forecast_data=forecast_data_serialized,
                           latest_data=latest_data_serialized)



# 로그
@app.route('/log', methods=['GET', 'POST'])
def log():
    if 'username' not in session:
        return redirect(url_for('login'))

    logs = []
    data_type = "real_time"  # 기본값
    if request.method == 'POST':
        date = request.form['date']
        data_type = request.form['data_type']
        date_start = datetime.strptime(date, "%Y-%m-%d")
        date_end = date_start + timedelta(days=1)

        # 선택된 데이터 타입에 따라 테이블 필터링
        if data_type == 'real_time':
            logs = RealTimeData.query.filter(
                RealTimeData.timestamp >= date_start,
                RealTimeData.timestamp < date_end
            ).all()
        elif data_type == 'forecast':
            logs = ForecastData.query.filter(
                ForecastData.fcstDateTime >= date_start,
                ForecastData.fcstDateTime < date_end
            ).all()

    return render_template('log.html', logs=logs, data_type=data_type)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
