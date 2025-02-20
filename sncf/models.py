
from db_config import db


class Client(db.Model):
    __tablename__ = 'clients'
    __table_args__ = {'extend_existing': True}  #  Adăugat pentru a permite redefinirea

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type_ticket = db.Column(db.String(50), nullable=False)
    no_adults = db.Column(db.Integer, nullable=False, default=0)
    no_childrens = db.Column(db.Integer, nullable=False, default=0)

    reservations = db.relationship('Reservation', back_populates='client')


class Destination(db.Model):
    __tablename__ = 'destinations'
    __table_args__ = {'extend_existing': True}  #  Permite extinderea tabelului existent

    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)

    reservations = db.relationship("Reservation", back_populates="destination")


class Ticket(db.Model):
    __tablename__ = 'tickets'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    type_trip = db.Column(db.String(50), nullable=True)
    classtype = db.Column(db.String(50), nullable=True)
    methodofpay = db.Column(db.String(50), nullable=True)

    reservations = db.relationship("Reservation", back_populates="ticket")


class Reservation(db.Model):
    __tablename__ = 'reservations'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    train_id = db.Column(db.Integer, db.ForeignKey('train_schedules.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    qr_code_path = db.Column(db.String(255), nullable=True)
    seat_number = db.Column(db.String(10), nullable=False)

    client = db.relationship("Client", back_populates="reservations")
    destination = db.relationship("Destination", back_populates="reservations")
    ticket = db.relationship("Ticket", back_populates="reservations")
    train = db.relationship("TrainSchedule")  #


# Modelul TrainSchedule
class TrainSchedule(db.Model):
        __tablename__ = 'train_schedules'
        __table_args__ = {'extend_existing': True}

        id = db.Column(db.Integer, primary_key=True)
        train_number = db.Column(db.String(50), nullable=False)
        departure_station = db.Column(db.String(100), nullable=False)
        arrival_station = db.Column(db.String(100), nullable=False)
        departure_time = db.Column(db.String(10), nullable=False)
        arrival_time = db.Column(db.String(10), nullable=False)
        train_type = db.Column(db.String(50), nullable=False)


def __repr__(self):
        return f"<Train {self.train_number} {self.departure_station} -> {self.arrival_station}>"
