from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import base64
from datetime import date, datetime, time

app = Flask(__name__)
db = SQLAlchemy(app)

# app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:12345678@localhost:5432/HOTEL?sslmode=disable'

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    superior_capacity = db.Column(db.Integer, nullable=False)
    deluxe_capacity = db.Column(db.Integer, nullable=False)
    standard_capacity = db.Column(db.Integer, nullable=False)
    superior_facility = db.Column(db.String, nullable=False)
    deluxe_facility = db.Column(db.String, nullable=False)
    standard_facility = db.Column(db.String, nullable=False)
    superior_price = db.Column(db.Integer, nullable=False)
    deluxe_price = db.Column(db.Integer, nullable=False)
    standard_price = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    booking_hotel = db.relationship('Booking', backref='hotel_rel')

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    booking_customer = db.relationship('Booking', backref='customer_rel')

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
    rating = db.Column(db.Integer)

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
    if not hotel and not customer:
        h = Hotel(
            name = data['hotel_name'],
            username = data['username'],
            password = data['password'],
            superior_capacity = data['superior_capacity'],
            deluxe_capacity = data['deluxe_capacity'],
            standard_capacity = data['standard_capacity'],
            superior_facility = data['superior_facility'],
            deluxe_facility = data['deluxe_facility'],
            standard_facility = data['standard_facility'],
            superior_price = data['superior_price'],
            deluxe_price = data['deluxe_price'],
            standard_price = data['standard_price'],
            city = data['city'],
            address = data['hotel_address'],
            phone = data['hotel_phone']
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
    allow2 = auth_hotel2(identity)
    if allow1 == True:
        return jsonify(
            [
                {
                    'hotel_id': hotel.id,
                    'hotel_name': hotel.name,
                    'username': hotel.username,
                    'password': hotel.password,
                    'superior_capacity': hotel.superior_capacity,
                    'superior_facility': hotel.superior_facility,
                    'superior_price': hotel.superior_price,
                    'deluxe_capacity': hotel.deluxe_capacity,
                    'deluxe_facility': hotel.deluxe_facility,
                    'deluxe_price': hotel.deluxe_price,
                    'standard_capacity': hotel.standard_capacity,
                    'standard_facility': hotel.standard_facility,
                    'standard_price': hotel.standard_price,
                    'city' : hotel.city,
                    'hotel_address' : hotel.address,
                    'hotel_phone' : hotel.phone
                } for hotel in Hotel.query.filter_by(id=allow2).all()
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
        h5 = 'superior_capacity'
        h6 = 'superior_facility'
        h7 = 'superior_price'
        h8 = 'deluxe_capacity'
        h9 = 'deluxe_facility'
        h10 = 'deluxe_price'
        h11 = 'standard_capacity'
        h12 = 'standard_facility'
        h13 = 'standard_price'
        h14 = 'city'
        h15 = 'hotel_address'
        h16 = 'hotel_phone'
        if not h1 in data and not h2 in data and not h3 in data and not h4 in data and not h5 in data and not h6 in data and not h7 in data and not h8 in data and not h9 in data and not h10 in data and not h11 in data and not h12 in data and not h13 in data and not h14 in data and not h15 in data and not h16 in data:
            return {"message" : "FAILED updating data. There is no field like that."}
        else:
            hotel = Hotel.query.filter_by(id=allow2).first()
            if h1 in data:
                hotel.id = data[h1]
            if h2 in data:
                hotel.name = data[h2]
            if h3 in data:
                hotel.username = data[h3]
            if h4 in data:
                hotel.password = data[h4]
            if h5 in data:
                hotel.superior_capacity = data[h5]
            if h6 in data:
                hotel.superior_facility = data[h6]
            if h7 in data:
                hotel.superior_price = data[h7]
            if h8 in data:
                hotel.deluxe_capacity = data[h8]
            if h9 in data:
                hotel.deluxe_facility = data[h9]
            if h10 in data:
                hotel.deluxe_price = data['h10']
            if h11 in data:
                hotel.standard_capacity = data[h11]
            if h12 in data:
                hotel.standard_facility = data[h12]
            if h13 in data:
                hotel.standard_price = data[h13]
            if h14 in data:
                hotel.city = data[h14]
            if h15 in data:
                hotel.address = data[h15]
            if h16 in data:
                hotel.phone = data[h16]
            db.session.commit()
            return {'message': 'SUCCESFULLY update data.'}, 201
    else:
        return {"message":"ACCESS DENIED !!! You can not update Hotel data."}, 400

@app.route('/hotel', methods=['DELETE'])    
def delete_hotel():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_hotel2(identity)
    if allow1 == True:
        h = Hotel.query.filter_by(id=allow2).first()
        db.session.delete(h)
        db.session.commit()
        return {"message":"SUCCESSFULLY delete Hotel."}, 200
    else:
        return {"message":"ACCESS DENIED !!! You can not delete Hotel."}, 400

# --------------- New Customer or Sign Up c --------------- #
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
        return {"message" : "SUCCESSFULLY register."}
    else:
        return {"message" : "FAILED to register. The username had been taken."}

@app.route('/customer', methods=['GET'])
def get_customer():
    identity = request.headers.get('Authorization')
    allow1 = auth_customer1(identity)
    allow2 = auth_customer2(identity)
    if allow1 == True:
        customer = Customer.query.filter_by(id=allow2).first()
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

@app.route('/customer', methods=['PUT'])
def update_customer():
    identity = request.headers.get('Authorization')
    allow1 = auth_customer1(identity)
    allow2 = auth_customer2(identity)
    if allow1 == True:
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
            c = Customer.query.filter_by(id=allow2).first()
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
        return {"message":"ACCESS DENIED !!! You can not update Customer data."}, 400

@app.route('/customer', methods=['DELETE'])
def delete_customer():
    identity = request.headers.get('Authorization')
    allow1 = auth_customer1(identity)
    allow2 = auth_customer2(identity)
    if allow1 == True:
        try:
            c = Customer.query.filter_by(id=allow2).first()
            db.session.delete(c)
            db.session.commit()
        except:
            return {"message":"FAILED to delete Customer."}, 400
        return {"message":"SUCCESSFULLY delete Customer."}, 200
    else:
        return {"message":"ACCESS DENIED !!! You can not delete Customer data."}, 400
    
# --------------- Booking --------------- #
@app.route('/booking', methods=['POST'])
def create_booking():
    identity = request.headers.get('Authorization')
    allow = auth_customer1(identity)
    if allow == True:
        c_id = auth_customer2(identity)
        data = request.get_json()
        k = db.engine.execute(f'''
            select hotel.id as hotel_id,coalesce(avail_superior,5) as avail_sup,coalesce(avail_deluxe,5) as avail_del,coalesce(avail_standard,5) as avail_stan,hotel.name,hotel.city,hotel.address from hotel left outer join (select COALESCE((ho.superior_capacity - sum(bb.superior)),0) as avail_superior,
            COALESCE((ho.deluxe_capacity - sum(bb.deluxe)),0) as avail_deluxe, COALESCE((ho.standard_capacity - sum(bb.standard)),0) as avail_standard, city, address, name, ho.superior_capacity as cap_su,ho.deluxe_capacity as cap_de,ho.standard_capacity as cap_st, ho.id as idhotel from booking as bb join hotel as ho on ho.id = bb.hotel_id where (bb.checkin, bb.checkout) overlaps ('{data['check_in_date']}'::date, '{data['check_out_date']}'::date) and bb.hotel_id in (select id from hotel) group by ho.superior_capacity, ho.deluxe_capacity, ho.standard_capacity, city, address, name, idhotel) as virtual on virtual.idhotel=hotel.id where hotel.id = {data['hotel_id']};
        ''')
        h = Hotel.query.filter_by(id=data['hotel_id']).first()
        for i in k:
            if (0 <= data['amount_of_superior_room'] <= i[1]) and (0 <= data['amount_of_deluxe_room'] <= i[2]) and (0 <= data['amount_of_standard_room'] <= i[3]) and (data['check_in_date'] < data['check_out_date']):
                b = Booking(
                        checkin = data['check_in_date'],
                        checkout = data['check_out_date'],
                        superior = data['amount_of_superior_room'],
                        deluxe = data['amount_of_deluxe_room'],
                        standard = data['amount_of_standard_room'],
                        total_price = (data['amount_of_superior_room']*h.superior_price) + (data['amount_of_deluxe_room']*h.deluxe_price) + (data['amount_of_standard_room']*h.standard_price),
                        hotel_id = data['hotel_id'],
                        customer_id = c_id,
                        )
                db.session.add(b)
                db.session.commit()
                return {"message" : "SUCCESSFULLY Booking a hotel."}
            else:
                return {"message" : "Please check the date and the amount of its rooms. The amount of rooms booked cannot exceed stock and must be positive integer number."}
    else:
        return {"message" : "FAILED Booking a hotel. Please check username and password."}

@app.route('/booking', methods=['GET'])
def get_booking():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_hotel2(identity)
    allow3 = auth_customer1(identity)
    allow4 = auth_customer2(identity)
    if allow1 == True:
        return jsonify(
            [
                {
                    'hotel_id' : booking.hotel_id,
                    'check_in_date' : booking.checkin,
                    'check_out_date' : booking.checkout,
                    'amount_of_superior_room' : booking.superior,
                    'amount_of_deluxe_room' : booking.deluxe,
                    'amount_of_standard_room' : booking.standard,
                    'total_price' : booking.total_price,
                    'rating' : booking.rating
                } for booking in Booking.query.filter_by(hotel_id=allow2).all()
            ]
            ), 201
    elif allow3 == True:
        return jsonify(
            [
                {
                    'hotel_name' : booking.hotel_id,
                    'check_in_date' : booking.checkin,
                    'check_out_date' : booking.checkout,
                    'amount_of_superior_room' : booking.superior,
                    'amount_of_deluxe_room' : booking.deluxe,
                    'amount_of_standard_room' : booking.standard,
                    'total_price' : booking.total_price,
                    'rating' : booking.rating,
                    'customer_id' : booking.customer_id
                } for booking in Booking.query.filter_by(customer_id=allow4).all()
            ]
            ), 201
    else:
        return {"message":"FAILED to get Booking records. Please check for username and password."}

@app.route('/booking', methods=['DELETE'])
def delete_booking():
    identity = request.headers.get('Authorization')
    allow1 = auth_customer1(identity)
    allow2 = auth_customer2(identity)
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
        return {"message":"ACCESS DENIED !!! You can not give rating."}, 400
  
# --------------- Most Popular Hotel --------------- #
@app.route('/tophotel', methods=['GET'])
def top_hotel():
    identity = request.headers.get('Authorization')
    allow1 = auth_hotel1(identity)
    allow2 = auth_customer1(identity)
    if allow1 == True or allow2 == True:
        result = db.engine.execute(f'''SELECT hotel_id, COUNT(hotel_id) FROM booking GROUP BY hotel_id ORDER BY count DESC LIMIT 3 ''')
        x = []
        for y in result:
            x.append({'hotel_id':y[0], 'total_booking':y[1]})
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
        result = db.engine.execute(f'''SELECT hotel_id,AVG(rating)::numeric(10,2) FROM booking WHERE rating is not NULL group by hotel_id order by AVG DESC LIMIT 3''')
        x = []
        for y in result:
            x.append({'hotel_id':y[0], 'average_rating':y[1]})
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
    if data['checkin'] < data['checkout']:
        k = db.engine.execute(f'''
            select hotel.id as hotel_id,coalesce(avail_superior,hotel.superior_capacity) as avail_sup,coalesce(avail_deluxe,hotel.deluxe_capacity) as avail_del,coalesce(avail_standard,hotel.standard_capacity) as avail_stan,hotel.name,hotel.city,hotel.address from hotel left outer join (select COALESCE((ho.superior_capacity - sum(bb.superior)),0) as avail_superior,COALESCE((ho.deluxe_capacity - sum(bb.deluxe)),0) as avail_deluxe, COALESCE((ho.standard_capacity - sum(bb.standard)),0) as avail_standard, city, address, name, ho.superior_capacity as cap_su,ho.deluxe_capacity as cap_de,ho.standard_capacity as cap_st, ho.id as idhotel from booking as bb join hotel as ho on ho.id = bb.hotel_id where (bb.checkin, bb.checkout) overlaps ('{data['checkin']}'::date, '{data['checkout']}'::date) and bb.hotel_id in (select id from hotel) group by ho.superior_capacity, ho.deluxe_capacity, ho.standard_capacity, city, address, name, idhotel) as virtual on virtual.idhotel=hotel.id where hotel.city ILIKE '%%{data['city']}%%' order by id;
        ''')

        x = []
        for i in k:
            x.append({
                    "_hotel_id": i[0],
                    "_hotel_name": i[4],
                    "superior_stock": i[1],
                    "deluxe_stock": i[2],
                    "standard_stock": i[3],
                    "city": i[5],
                    "address": i[6]
                })
        return jsonify(x)
    else:
        return {"message" : "Please enter the dates correctly."}
     
if __name__ == '__main__':
	app.run()

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
from flask_cors import CORS, cross_origin

CORS(app, supports_credentials=True) 
# --------------- Login --------------- #
@app.route('/login', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'], supports_credentials=True)
def login():
    identity = request.headers.get('Authorization')
    allow1 = auth_customer1(identity)
    if allow1 == True:
        return "True bro"
    else:
        return "False bro"