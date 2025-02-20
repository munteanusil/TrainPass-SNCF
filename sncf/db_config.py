import qrcode
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Inițializează instanța de SQLAlchemy
db = SQLAlchemy()

from models import Client, Destination, Ticket, Reservation, TrainSchedule

app = Flask(__name__)

# Configurare baza de date SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bilete.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inițializează baza de date
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Logica pentru rezervări și generarea QR Code
    pass

@app.route('/train-schedule')
def train_schedule():
    schedules = TrainSchedule.query.all()
    return render_template('train_schedule.html', schedules=schedules)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not TrainSchedule.query.first():
            train1 = TrainSchedule(
                train_number="IC123",
                departure_station="Paris",
                arrival_station="Lyon",
                departure_time="08:30",
                arrival_time="10:45",
                train_type="Intercity"
            )
            train2 = TrainSchedule(
                train_number="TGV789",
                departure_station="Paris",
                arrival_station="Nice",
                departure_time="09:15",
                arrival_time="14:30",
                train_type="TGV"
            )
            db.session.add_all([train1, train2])
            db.session.commit()
    app.run(debug=True)







