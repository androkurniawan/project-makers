# from crypt import methods
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import base64
from datetime import date, datetime, time

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:12345678@localhost:5432/HOTEL?sslmode=disable'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    superior = db.Column(db.Integer)
    deluxe = db.Column(db.Integer)
    standard = db.Column(db.Integer)
    total_price = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id', ondelete='CASCADE'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)
    hotel_name = db.Column(db.String)
    rating = db.Column(db.Integer)
    superior_id = db.Column(db.Integer, db.ForeignKey('superior.id', ondelete='CASCADE'))
    deluxe_id = db.Column(db.Integer, db.ForeignKey('deluxe.id', ondelete='CASCADE'))
    standard_id = db.Column(db.Integer, db.ForeignKey('standard.id', ondelete='CASCADE'))

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)

class Superior(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    facility = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id', ondelete='CASCADE'))
    booking_superior = db.relationship('Booking', backref='superior_rel')

class Deluxe(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    facility = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id', ondelete='CASCADE')) 
    booking_deluxe = db.relationship('Booking', backref='deluxe_rel')

class Standard(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    facility = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id', ondelete='CASCADE'))
    booking_standard = db.relationship('Booking', backref='standard_rel')

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    # booking_customer = db.relationship('Booking', backref='customer')

db.create_all()
db.session.commit()

# --------------- Basic Auth --------------- #
def auth_hotel1(auth):
    e = base64.b64decode(auth[6:])
    str_encode = e.decode('utf-8')
    lst = str_encode.split(':')
    user = lst[0]
    passw = lst[1]
    hotel = Hotel.query.filter_by(username=user).filter_by(password=passw).first()
    if not hotel:
        return {
            'message': 'None HOTEL ADMIN account in Database !'
        }
    else:
        return True

def auth_hotel2(auth):
    e = base64.b64decode(auth[6:])
    str_encode = e.decode('utf-8')
    lst = str_encode.split(':')
    user = lst[0]
    passw = lst[1]
    hotel = Hotel.query.filter_by(username=user).filter_by(password=passw).first()
    if hotel:
        return str(hotel.id)
    else:
        return 0

def auth_customer1(auth):
    e = base64.b64decode(auth[6:])
    str_encode = e.decode('utf-8')
    lst = str_encode.split(':')
    user = lst[0]
    passw = lst[1]
    customer = Customer.query.filter_by(username=user).filter_by(password=passw).first()
    if not customer:
        return {
            'message': 'None User account in Database !'
        }
    else:
        return True

def auth_customer2(auth):
    e = base64.b64decode(auth[6:])
    str_encode = e.decode('utf-8')
    lst = str_encode.split(':')
    user = lst[0]
    passw = lst[1]
    customer = Customer.query.filter_by(username=user).filter_by(password=passw).first()
    if customer:
        return str(customer.id)
    else:
        return 0

# --------------- Hotel --------------- #
@app.route('/hotel', methods=['POST'])
def create_hotel():
    data = request.get_json()
    hotel = Hotel.query.filter_by(username=data['username']).first()
    customer = Customer.query.filter_by(username=data['username']).first()
    # deluxe_cap = Deluxe.query.filter_by()
    if not hotel and not customer:
        h = Hotel(
            name = data['hotel_name'],
            username = data['username'],
            password = data['password'],
            city = data['city'],
            address = data['hotel_address'],
            phone = data['hotel_phone_number']
            # capacity_deluxe = Deluxe.stock,
            # capacity_superior = Superior.stock,
            # capacity_standard = Standard.
            )
        db.session.add(h)
        db.session.commit()
        return {"message" : "SUCCESSFULLY register a new Hotel."}
    else:
        return {"message" : "FAILED to register a new Hotel. May be username or hotel name or hotel phone number had been taken by another hotel."}
    
@app.route('/hotel', methods=['GET'])
def get_hotel():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_customer1(identity)
    if allow1 == True or allow2 == True:
        return jsonify(
            [
                {
                    'hotel_name' : hotel.name,
                    'city' : hotel.city,
                    'hotel_address' : hotel.address,
                    'hotel_phone' : hotel.phone
                } for hotel in Hotel.query.all()
            ]
            ), 201
    else:
        return {"message":"FAILED to get hotel data. Please check for username and password."}
    
@app.route('/hotel', methods=['PUT'])
def update_hotel():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_hotel2(identity)
    if allow1 == True:
        data = request.get_json()
        h1 = 'hotel_id'
        h2 = 'hotel_name'
        h3 = 'username'
        h4 = 'password'
        h5 = 'city'
        h6 = 'hotel_address'
        h7 = 'hotel_phone_number'
        if not h1 in data and not h2 in data and not h3 in data and not h4 in data and not h5 in data and not h6 in data and not h7 in data:
            return {"message" : "FAILED updating data. There is no field like that."}
        else:
            h = Hotel.query.filter_by(id=allow2).first()
            if h1 in data:
                h.id = data['hotel_id']
            if h2 in data:
                h.name = data['hotel_name']
            if h3 in data:
                h.username = data['username']
            if h4 in data:
                h.password = data['password']
            if h5 in data:
                h.city = data['city']
            if h6 in data:
                h.address = data['hotel_address']
            if h7 in data:
                h.phone = data['hotel_phone_number']
            db.session.commit()
            return {'message': 'SUCCESFULLY update data.'}, 201
    else:
        return {"message":"ACCESS DENIED !!! You can not update this Hotel data."}, 400

@app.route('/hotel/<iddelete>', methods=['DELETE'])    
def delete_hotel(iddelete):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == iddelete:
        try:
            h = Hotel.query.filter_by(id=iddelete).first()
            db.session.delete(h)
            db.session.commit()
        except:
            return {"message":"FAILED to delete Hotel. Before delete Hotel, you must UNLINK the rooms that using this Hotel."}, 400
        return {"message":"SUCCESSFULLY delete Hotel."}, 200
    else:
        return {"message":"ACCESS DENIED !!! You can not delete Hotel data."}, 400

# --------------- Customer --------------- #
@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer.query.filter_by(username=data['username']).first()
    hotel = Hotel.query.filter_by(username=data['username']).first()
    if not customer and not hotel:
        c = Customer(
            username = data['username'],
            password = data['password'],
            name = data['customer_name'],
            phone = data['customer_phone'],
            email = data['customer_email']
            )
        db.session.add(c)
        db.session.commit()
        return {"message" : "SUCCESSFULLY create a new Customer."}
    else:
        return {"message" : "FAILED to create Customer. The username had been taken."}

@app.route('/customer/<idget>', methods=['GET'])
def get_customer(idget):
    identity = request.headers.get('Authorization')
    allow = auth_customer2(identity)
    if allow == idget:
        customer = Customer.query.filter_by(id=idget).first()
        return jsonify(
            [
                {
                    'username' : customer.username,
                    'password' : customer.password,
                    'customer_name' : customer.name,
                    'customer_phone' : customer.phone,
                    'customer_email' : customer.email
                }
            ]
            ), 201
    else:
        return {"message":"FAILED to get customer data. Please check for username and password."}

@app.route('/customer/<idupdate>', methods=['PUT'])
def update_customer(idupdate):
    identity = request.headers.get('Authorization')
    allow = auth_customer2(identity)
    if allow == idupdate:
        data = request.get_json()
        c1 = 'customer_id'
        c2 = 'customer_name'
        c3 = 'username'
        c4 = 'password'
        c5 = 'customer_phone'
        c6 = 'customer_email'
        if not c1 in data and not c2 in data and not c3 in data and not c4 in data and not c5 in data and not c6 in data:
            return {"message" : "FAILED updating data. There is no field like that."}
        else:
            c = Customer.query.filter_by(id=idupdate).first()
            if 'customer_id' in data:
                c.id = data['customer_id']
            if 'customer_name' in data:
                c.name = data['customer_name']
            if 'username' in data:
                c.username = data['username']
            if 'password' in data:
                c.password = data['password']
            if 'customer_phone' in data:
                c.phone = data['customer_phone']
            if 'customer_email' in data:
                c.email = data['customer_email']
            db.session.commit()
            return {'message': 'SUCCESFULLY update data.'}, 201
    else:
        return {"message":"ACCESS DENIED !!! You can not update this Customer data."}, 400

@app.route('/customer/<iddelete>', methods=['DELETE'])
def delete_customer(iddelete):
    identity = request.headers.get('Authorization')
    allow = auth_customer2(identity)
    if allow == iddelete:
        try:
            c = Customer.query.filter_by(id=iddelete).first()
            db.session.delete(c)
            db.session.commit()
        except:
            return {"message":"FAILED to delete Customer."}, 400
        return {"message":"SUCCESSFULLY delete Customer."}, 200
    else:
        return {"message":"ACCESS DENIED !!! You can not delete Customer data."}, 400
    
# --------------- Superior --------------- #
@app.route('/hotel/<idpost>/superior', methods=['POST'])
def create_superior(idpost):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idpost:
        data = request.get_json()
        s = Superior(
                facility = data['room_facility'],
                stock = data['stock'],
                price = data['price'],
                hotel_id = idpost
                )
        db.session.add(s)
        db.session.commit()
        return {"message" : "SUCCESSFULLY create SUPERIOR room."}
    else:
        return {"message" : "FAILED to create Superior room. Access denied."}

@app.route('/hotel/<idget>/superior', methods=['GET'])
def get_superior(idget):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idget:
        return jsonify(
            [
                {
                    'room_facility' : superior.facility,
                    'stock' : superior.stock,
                    'hotel_id' : superior.hotel_id,
                    'price' : superior.price
                } for superior in Superior.query.filter_by(hotel_id=idget).all()
            ] 
            ), 201
    else:
        return {"message":"FAILED to get Superior room data. Please check for username and password."}

@app.route('/hotel/<idupdate>/superior', methods=['PUT'])
def update_superior(idupdate):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idupdate:
        data = request.get_json()
        s1 = 'room_facility'
        s2 = 'stock'
        s3 = 'price'
        if not s1 in data and not s2 in data and not s3 in data:
            return {"message" : "FAILED updating Superior data. There is no field like that."}
        else:
            s = Superior.query.filter_by(hotel_id=idupdate).first()
            if s1 in data:
                s.facility = data['room_facility']
            if s2 in data:
                s.stock = data['stock']
            if s3 in data:
                s.price = data['price']
            db.session.commit()
            return {'message': 'SUCCESFULLY update Superior room data.'}, 201
    else:
        return {"message":"ACCESS DENIED !!! You can not update this Superior room data."}, 400

@app.route('/hotel/<iddelete>/superior', methods=['DELETE'])
def delete_superior(iddelete):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == iddelete:
        try:
            s = Superior.query.filter_by(hotel_id=iddelete).first()
            if s:
                db.session.delete(s)
                db.session.commit()
            else:
                return {"message" : "There is no Superior room."}
        except:
            return {"message":"FAILED to delete Superior room."}, 400
        return {"message":"SUCCESSFULLY delete Superior room."}, 200
    else:
        return {"message":"ACCESS DENIED !!! You can not delete Superior room data."}, 400

# --------------- Deluxe --------------- #
@app.route('/hotel/<idpost>/deluxe', methods=['POST'])
def create_deluxe(idpost):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idpost:
        data = request.get_json()
        d = Deluxe(
                facility = data['room_facility'],
                stock = data['stock'],
                price = data['price'],
                hotel_id = idpost
                )
        db.session.add(d)
        db.session.commit()
        return {"message" : "SUCCESSFULLY create Deluxe room."}
    else:
        return {"message" : "FAILED to create Deluxe room. Access denied."}

@app.route('/hotel/<idget>/deluxe', methods=['GET'])
def get_delux(idget):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idget:
        return jsonify(
            [
                {
                    'room_facility' : deluxe.facility,
                    'stock' : deluxe.stock,
                    'hotel_id' : deluxe.hotel_id,
                    'price' : deluxe.price
                } for deluxe in Deluxe.query.filter_by(hotel_id=idget).all()
            ] 
            ), 201
    else:
        return {"message":"FAILED to get Deluxe room data. Please check for username and password."}

@app.route('/hotel/<idupdate>/deluxe', methods=['PUT'])
def update_deluxe(idupdate):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idupdate:
        data = request.get_json()
        d1 = 'room_facility'
        d2 = 'stock'
        d3 = 'price'
        if not d1 in data and not d2 in data and not d3 in data:
            return {"message" : "FAILED updating Deluxe data. There is no field like that."}
        else:
            d = Deluxe.query.filter_by(hotel_id=idupdate).first()
            if d1 in data:
                d.facility = data['room_facility']
            if d2 in data:
                d.stock = data['stock']
            if d3 in data:
                d.price = data['price']
            db.session.commit()
            return {'message': 'SUCCESFULLY update Deluxe room data.'}, 201
    else:
        return {"message":"ACCESS DENIED !!! You can not update this Deluxe room data."}, 400

@app.route('/hotel/<iddelete>/deluxe', methods=['DELETE'])
def delete_deluxe(iddelete):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == iddelete:
        try:
            d = Deluxe.query.filter_by(hotel_id=iddelete).first()
            if d:
                db.session.delete(d)
                db.session.commit()
            else:
                return {"message" : "There is no Deluxe room."}
        except:
            return {"message":"FAILED to delete Deluxe room."}, 400
        return {"message":"SUCCESSFULLY delete Deluxe room."}, 200
    else:
        return {"message":"ACCESS DENIED !!! You can not delete Deluxe room data."}, 400

# --------------- Standard --------------- #
@app.route('/hotel/<idpost>/standard', methods=['POST'])
def create_standard(idpost):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idpost:
        data = request.get_json()
        s = Standard(
                facility = data['room_facility'],
                stock = data['stock'],
                price = data['price'],
                hotel_id = idpost
                )
        db.session.add(s)
        db.session.commit()
        return {"message" : "SUCCESSFULLY create Standard room."}
    else:
        return {"message" : "FAILED to create Standard room. Access denied."}

@app.route('/hotel/<idget>/standard', methods=['GET'])
def get_standard(idget):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idget:
        return jsonify(
            [
                {
                    'room_facility' : standard.facility,
                    'stock' : standard.stock,
                    'hotel_id' : standard.hotel_id,
                    'price' : standard.price
                } for standard in Standard.query.filter_by(hotel_id=idget).all()
            ] 
            ), 201
    else:
        return {"message":"FAILED to get Standard room data. Please check for username and password."}

@app.route('/hotel/<idupdate>/standard', methods=['PUT'])
def update_standard(idupdate):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == idupdate:
        data = request.get_json()
        s1 = 'room_facility'
        s2 = 'stock'
        s3 = 'price'
        if not s1 in data and not s2 in data and not s3 in data:
            return {"message" : "FAILED updating Standard data. There is no field like that."}
        else:
            s = Standard.query.filter_by(hotel_id=idupdate).first()
            if s1 in data:
                s.facility = data['room_facility']
            if s2 in data:
                s.stock = data['stock']
            if s3 in data:
                s.price = data['price']
            db.session.commit()
            return {'message': 'SUCCESFULLY update Standard room data.'}, 201
    else:
        return {"message":"ACCESS DENIED !!! You can not update this Standard room data."}, 400

@app.route('/hotel/<iddelete>/standard', methods=['DELETE'])
def delete_standard(iddelete):
    identity = request.headers.get('Authorization')
    allow = auth_hotel2(identity)
    if allow == iddelete:
        try:
            s = Standard.query.filter_by(hotel_id=iddelete).first()
            if s:
                db.session.delete(s)
                db.session.commit()
            else:
                return {"message" : "There is no Standard room."}
        except:
            return {"message":"FAILED to delete Standard room."}, 400
        return {"message":"SUCCESSFULLY delete Standard room."}, 200
    else:
        return {"message":"ACCESS DENIED !!! You can not delete Standard room data."}, 400

# --------------- Booking --------------- #
@app.route('/booking', methods=['POST'])
def create_booking():
    identity = request.headers.get('Authorization')
    allow = auth_customer1(identity)
    if allow == True:
        c_id = auth_customer2(identity)
        data = request.get_json()
        s = Superior.query.filter_by(hotel_id=data['hotel_id']).first()
        d = Deluxe.query.filter_by(hotel_id=data['hotel_id']).first()
        st = Standard.query.filter_by(hotel_id=data['hotel_id']).first()
        h = Hotel.query.filter_by(id=data['hotel_id']).first()
        if (s.stock > 0 or d.stock > 0 or st.stock > 0) and (s.stock >= data['amount_of_superior_room'] and d.stock >= data['amount_of_deluxe_room'] and st.stock >= data['amount_of_standard_room']) and (data['amount_of_superior_room'] >= 0 and data['amount_of_deluxe_room'] >=0 and data['amount_of_standard_room'] >= 0):
            b = Booking(
                    booking_date = data['booking_date'],
                    checkin = data['check_in_date'],
                    checkout = data['check_out_date'],
                    superior = data['amount_of_superior_room'],
                    deluxe = data['amount_of_deluxe_room'],
                    standard = data['amount_of_standard_room'],
                    total_price = (data['amount_of_superior_room']*s.price) + (data['amount_of_deluxe_room']*d.price) + (data['amount_of_standard_room']*st.price),
                    hotel_id = data['hotel_id'],
                    customer_id = c_id,
                    hotel_name = h.name
                    )
            db.session.add(b)
            db.session.commit()
            return {"message" : "SUCCESSFULLY Booking a hotel."}
        else:
            return {"message" : "The amount of rooms booked cannot exceed stock and must be positive integer number."}
    else:
        return {"message" : "FAILED to Booking a hotel."}

@app.route('/booking', methods=['GET'])
def get_booking():
    identity = request.headers.get('Authorization')
    allow1 = auth_customer1(identity)
    allow3 = auth_hotel1(identity)
    if allow1 == True:
        allow2 = auth_customer2(identity)
        return jsonify(
            [
                {
                    'hotel_name' : booking.hotel_name,
                    'booking_date' : booking.booking_date,
                    'check_in_date' : booking.checkin,
                    'check_out_date' : booking.checkout,
                    'amount_of_superior_room' : booking.superior,
                    'amount_of_deluxe_room' : booking.deluxe,
                    'amount_of_standard_room' : booking.standard,
                    'total_price' : booking.total_price,
                    'rating' : booking.rating
                } for booking in Booking.query.filter_by(customer_id=allow2).all()
            ]
            ), 201
    elif allow3 == True:
        allow4 = auth_hotel2(identity)
        return jsonify(
            [
                {
                    'hotel_name' : booking.hotel_name,
                    'booking_date' : booking.booking_date,
                    'check_in_date' : booking.checkin,
                    'check_out_date' : booking.checkout,
                    'amount_of_superior_room' : booking.superior,
                    'amount_of_deluxe_room' : booking.deluxe,
                    'amount_of_standard_room' : booking.standard,
                    'total_price' : booking.total_price,
                    'rating' : booking.rating,
                    'customer_id' : booking.customer_id
                } for booking in Booking.query.filter_by(hotel_id=allow4).all()
            ]
            ), 201
    else:
        return {"message":"FAILED to get Booking records. Please check for username and password."}

@app.route('/booking', methods=['DELETE'])
def delete_booking():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_hotel2(identity)
    if allow1 == True:
        try:
            b = Booking.query.filter_by(hotel_id=allow2).first()
            if b:
                db.session.delete(b)
                db.session.commit()
            else:
                return {"message" : "There is no Booking record."}
        except:
            return {"message":"FAILED to delete a Booking."}, 400
        return {"message":"SUCCESSFULLY delete a Booking record."}, 200
    else:
        return {"message":"ACCESS DENIED !!! You can not delete Booking record data."}, 400

@app.route('/rating', methods=['PUT'])
def give_rating():
    identity = request.headers.get('Authorization')
    allow1 = auth_customer1(identity)
    allow2 = auth_customer2(identity)
    r = Booking.query.filter_by(customer_id=allow2).filter_by(rating=None).first()
    if allow1 == True:
        if not r:
            return {"message" : "You don't have a booking record that needs to be rated."}
        else:
            data = request.get_json()
            if not 'rating' in data:
                return {"message" : "FAILED give rating. There is no field like that."}
            else:
                if 'rating' in data:
                    r.rating = data['rating']
                db.session.commit()
                return {'message': 'SUCCESFULLY give rating.'}, 201
    else:
        return {"message":"ACCESS DENIED !!! You can not give rating to this booking."}, 400
  
# --------------- Most Popular Hotel --------------- #
@app.route('/tophotel', methods=['GET'])
def top_hotel():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_customer1(identity)
    if allow1 == True or allow2 == True:
        result = db.engine.execute(f'''SELECT hotel_id, hotel_name, COUNT(hotel_id) FROM booking GROUP BY hotel_id, hotel_name ORDER BY count DESC LIMIT 3 ''')
        x = []
        for y in result:
            x.append({'hotel_id':y[0], 'hotel_name':y[1], 'total_booking':y[2]})
        return jsonify(x)
    else:
        return {
            "message":"ACCESS DENIED !!! You can not see top hotels."
        }

# --------------- Most Hotels Rating Score --------------- #
@app.route('/toprating', methods=['GET'])
def top_rating():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_customer1(identity)
    if allow1 == True or allow2 == True:
        result = db.engine.execute(f'''SELECT hotel_id,hotel_name,AVG(rating)::numeric(10,2) FROM booking WHERE rating is not NULL group by hotel_id,hotel_name order by AVG DESC LIMIT 3''')
        x = []
        for y in result:
            x.append({'hotel_id':y[0], 'hotel_name':y[1], 'average_rating':y[2]})
        return jsonify(x)
    else:
        return {
            "message":"ACCESS DENIED !!! You can not see top rating Hotels."
        }

# --------------- Top Users --------------- #
@app.route('/topuser', methods=['GET'])
def top_user():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_customer1(identity)
    if allow1 == True or allow2 == True:
        result = db.engine.execute(f'''SELECT customer.id,name,COUNT(customer.id) FROM customer INNER JOIN booking ON booking.customer_id=customer.id GROUP BY customer.id,name ORDER BY COUNT DESC LIMIT 3;''')
        x = []
        for y in result:
            x.append({'customer_id':y[0], 'customer_name':y[1], 'number_of_booking':y[2]})
        return jsonify(x)
    else:
        return {
            "message":"ACCESS DENIED !!! You can not see top users."
        }

# --------------- Searching Hotels --------------- #
@app.route('/searching', methods=['GET'])
def search_hotel():
    data = request.get_json()
    k = db.engine.execute(f'''
        select COALESCE((su.stock - sum(xx.superior)),0) as avail_superior, COALESCE((de.stock - sum(xx.deluxe)),0) as avail_deluxe, COALESCE((st.stock - sum(xx.standard)),0) as avail_standard, city, address, name, su.stock as cap_su, de.stock as cap_de, st.stock as cap_st, ho.id as ident from booking as xx join superior as su on su.hotel_id = xx.hotel_id join deluxe as de on de.hotel_id = xx.hotel_id join standard as st on st.hotel_id = xx.hotel_id join hotel as ho on ho.id = xx.hotel_id where (xx.checkin, xx.checkout) overlaps ('{data['checkin']}'::date, '{data['checkout']}'::date) and xx.hotel_id in (select id from hotel) and ho.city ilike '%%{data['city']}%%' group by su.stock, de.stock, st.stock, city, address, name, ident
    ''')

    x = []
    for i in k:
        x.append({
                "hotel_name": i[5],
                "superior_stock": i[0],
                "deluxe_stock": i[1],
                "standard_stock": i[2],
                "city": i[3],
                "address": i[4]
            })
    if len(x) != 0:
        return {"Available_Hotels_and_its_stocks" : [x, another_result()]}
    else:
        return {"Available_Hotels_and_its_stocks" : initial_condition()}

def initial_condition():
    x = []
    m = db.engine.execute(f''' select id from hotel order by id ''')
    for j in m:
        x.append({
                    "hotel_name": Hotel.query.filter_by(id=j[0]).first().name,
                    "superior_stock": Superior.query.filter_by(hotel_id=j[0]).first().stock,
                    "deluxe_stock": Deluxe.query.filter_by(hotel_id=j[0]).first().stock,
                    "standard_stock": Standard.query.filter_by(hotel_id=j[0]).first().stock,
                    "city": Hotel.query.filter_by(id=j[0]).first().city,
                    "address": Hotel.query.filter_by(id=j[0]).first().address
                })
    return x

def another_result():
    data = request.get_json()
    k = db.engine.execute(f'''
        select COALESCE((su.stock - sum(xx.superior)),0) as avail_superior, COALESCE((de.stock - sum(xx.deluxe)),0) as avail_deluxe, COALESCE((st.stock - sum(xx.standard)),0) as avail_standard, city, address, name, su.stock as cap_su, de.stock as cap_de, st.stock as cap_st, ho.id as ident from booking as xx join superior as su on su.hotel_id = xx.hotel_id join deluxe as de on de.hotel_id = xx.hotel_id join standard as st on st.hotel_id = xx.hotel_id join hotel as ho on ho.id = xx.hotel_id where (xx.checkin, xx.checkout) overlaps ('{data['checkin']}'::date, '{data['checkout']}'::date) and xx.hotel_id in (select id from hotel) group by su.stock, de.stock, st.stock, city, address, name, ident
    ''')
    m = db.engine.execute(f''' select id from hotel order by id ''')
    x = []
    y = []
    z = []
    for a in m:
        z.append(a[0])
    for i in k:
        y.append(i[9])
    for c in z:
        if c not in y:
            x.append({
                "hotel_name": Hotel.query.filter_by(id=c).first().name,
                "superior_stock": Superior.query.filter_by(hotel_id=c).first().stock,
                "deluxe_stock": Deluxe.query.filter_by(hotel_id=c).first().stock,
                "standard_stock": Standard.query.filter_by(hotel_id=c).first().stock,
                "city": Hotel.query.filter_by(id=c).first().city,
                "address": Hotel.query.filter_by(id=c).first().address
            })
    return x
     
if __name__ == '__main__':
	app.run()