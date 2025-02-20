import csv
import os
from urllib import request

import qrcode
from flask import Flask, render_template, request, session, redirect, flash, url_for
from db_config import db
from models import Reservation, Destination, Ticket, TrainSchedule, Client
import plotly.express as px
import plotly.io as pio
import pandas as pd
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bilete.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_name = request.form.get('client-name')
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        ticket_type = request.form.get('ticket-type')
        adults = int(request.form.get('adults', 0))
        children = int(request.form.get('children', 0))
        travel_type = request.form.get('travel-type')
        travel_class = request.form.get('class')
        payment_method = request.form.get('payment')
        seat_number = request.form.get('seat_number')

        destination_obj = Destination(departure=departure, destination=destination)
        db.session.add(destination_obj)
        db.session.commit()

        client_obj = Client(name=client_name, type_ticket=ticket_type, no_adults=adults, no_childrens=children)
        db.session.add(client_obj)
        db.session.commit()

        ticket_obj = Ticket(type_trip=travel_type, classtype=travel_class, methodofpay=payment_method)
        db.session.add(ticket_obj)
        db.session.commit()

        reservation = Reservation(
            client_id=client_obj.id,
            destination_id=destination_obj.id,
            ticket_id=ticket_obj.id,
            qr_code_path="",
            seat_number = seat_number
        )
        db.session.add(reservation)
        db.session.commit()

        qr_data = f"""Nume pasager: {client_name}
                     Loc rezervat: {seat_number}
Plecare: {departure}
Destinație: {destination}
Adulți: {adults}
Copii: {children}
Tip bilet: {ticket_type}
Tip călătorie: {travel_type}
Clasa: {travel_class}
Plată: {payment_method}
"""

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image_path = "static/qr_code.png"
        qr_image.save(qr_image_path)

        reservation.qr_code_path = qr_image_path
        db.session.commit()

        return render_template(
            'confirmation.html',
            destination=destination_obj,
            client=client_obj,
            ticket=ticket_obj,
            qr_code_path=qr_image_path,
            seat_number = seat_number
        )

    return render_template('index.html')
db.init_app(app)

@app.route('/')
# def index():
#     return render_template('index.html')
@app.route('/train-schedule')
def train_schedule():
    schedules = TrainSchedule.query.all()
    return render_template('train_schedule.html', schedules=schedules)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


@app.route('/dashboard')
def dashboard():
    reservations = Reservation.query.all()
    destinations = Destination.query.all()
    tickets = Ticket.query.all()

    df_reservations = pd.DataFrame([(r.id, r.destination_id) for r in reservations], columns=['id', 'destination_id'])
    df_destinations = pd.DataFrame([(d.id, d.destination) for d in destinations], columns=['id', 'destination'])
    df_tickets = pd.DataFrame([(t.id, t.type_trip, t.methodofpay) for t in tickets],
                              columns=['id', 'type_trip', 'methodofpay'])

    df_reservations = df_reservations.merge(df_destinations, left_on='destination_id', right_on='id', how='left')

    fig_reservations = px.bar(df_reservations['destination'].value_counts().reset_index(),
                              x='destination', y='count',
                              labels={'destination': 'Destinație', 'count': 'Număr rezervări'},
                              title="📍 Numărul de rezervări pe destinație")
    graph_reservations = pio.to_json(fig_reservations)  #  NU FOLOSIM plotly.express.utils

    fig_tickets = px.pie(df_tickets, names='type_trip', title="🎫 Tipuri de bilete cumpărate")
    graph_tickets = pio.to_json(fig_tickets)

    fig_payment = px.bar(df_tickets['methodofpay'].value_counts().reset_index(),
                         x='methodofpay', y='count',
                         labels={'methodofpay': 'Metodă de plată', 'count': 'Număr tranzacții'},
                         title="💳 Metode de plată utilizate")
    graph_payment = pio.to_json(fig_payment)

    return render_template('dashboard.html', graph_reservations=graph_reservations,
                           graph_tickets=graph_tickets, graph_payment=graph_payment)


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "admin123":
            session['is_admin'] = True
            flash("🔓 Autentificare reușită ca Administrator!", "success")
            return redirect(url_for('index'))
        else:
            flash("❌ Eroare la autentificare. Verifică username-ul și parola.", "danger")

    return render_template('admin_login.html')

@app.route('/admin-logout')
def admin_logout():
    session.pop('is_admin', None)
    flash("🔒 Delogat cu succes!", "info")
    return redirect(url_for('index'))

@app.route('/trains', methods=['GET'])
def view_trains():
    if not session.get('is_admin'):
        flash("⛔ Acces interzis! Trebuie să fii administrator.", "danger")
        return redirect(url_for('index'))

    trains = TrainSchedule.query.all()
    return render_template("trains.html", trains=trains)


@app.route('/trains/add', methods=['GET', 'POST'])
def add_train():
    if request.method == "POST":
        train_number = request.form.get('train_number')
        departure_station = request.form.get('departure_station')
        arrival_station = request.form.get('arrival_station')
        departure_time = request.form.get('departure_time')
        arrival_time = request.form.get('arrival_time')
        train_type = request.form.get('train_type')

        new_train = TrainSchedule(
            train_number=train_number,
            departure_station=departure_station,
            arrival_station=arrival_station,
            departure_time=departure_time,
            arrival_time=arrival_time,
            train_type=train_type
        )
        db.session.add(new_train)
        db.session.commit()

        # Verifică dacă fișierul CSV există
        file_exists = os.path.exists("train_schedules.csv")

        # Scrie trenul în CSV
        with open("train_schedules.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    ["train_number", "departure_station", "arrival_station", "departure_time", "arrival_time",
                     "train_type"])  # Adaugă header doar dacă fișierul nu există

            writer.writerow(
                [train_number, departure_station, arrival_station, departure_time, arrival_time, train_type])

        flash("🚆 Tren adăugat cu succes și salvat în baza de date și CSV!", "success")
        return redirect(url_for('view_trains'))

    return render_template("add_train.html")

@app.route('/trains/edit/<int:train_id>', methods=['GET', 'POST'])
def edit_train(train_id):
    """Editează detaliile unui tren existent"""
    train = TrainSchedule.query.get_or_404(train_id)  # Caută trenul în baza de date

    if request.method == 'POST':
        # Obține datele din formular
        train.train_number = request.form.get('train_number')
        train.departure_station = request.form.get('departure_station')
        train.arrival_station = request.form.get('arrival_station')
        train.departure_time = request.form.get('departure_time')
        train.arrival_time = request.form.get('arrival_time')
        train.train_type = request.form.get('train_type')

        db.session.commit()  # Salvează modificările
        flash("✏ Tren editat cu succes!", "success")
        return redirect(url_for('view_trains'))

    return render_template("edit_train.html", train=train)


@app.route('/trains/delete/<int:train_id>', methods=['POST'])
def delete_train(train_id):
    """Șterge un tren din baza de date"""
    train = TrainSchedule.query.get_or_404(train_id)  # Caută trenul în baza de date

    db.session.delete(train)  # Șterge trenul
    db.session.commit()  # Salvează modificările

    flash("❌ Tren șters cu succes!", "danger")
    return redirect(url_for('view_trains'))


@app.route("/", methods=["GET", "POST"])
def seat_number():
    if request.method == "POST":
        seat_number = request.form.get("seat_number")
        # Procesează rezervarea și salvează în DB
        pass

    # Obține toate locurile deja rezervate
    reserved_seats = {r.qr_code_path for r in Reservation.query.all()}

    return render_template("index.html", reserved_seats=reserved_seats)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
