class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://your_username:your_password@localhost/forecast_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
