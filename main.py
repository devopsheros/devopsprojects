from flask import Flask, render_template, request, session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
import psycopg2, random, string, secrets, os


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


conn = psycopg2.connect(database=f"{os.environ['POSTGRES_DB']}", user=f"{os.environ['POSTGRES_USER']}", password=f"{os.environ['POSTGRES_PASSWORD']}", host=f"{os.environ['POSTGRES_HOST']}",port='5432')
cursor = conn.cursor()

def create_data():
    # create engine
    engine = create_engine(f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:5432/{os.environ["POSTGRES_DB"]}')

    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # create base class
    Base = declarative_base()

    # define State class
    class states(Base):
        __tablename__ = 'states'

        id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        state_code = Column(String(2), nullable=False)
        state_name = Column(String(50), nullable=False)

    # define Ticket class
    class tickets(Base):
        __tablename__ = 'tickets'

        id = Column(Integer, primary_key=True, autoincrement=True)
        ticket_number = Column(String(10), nullable=False)
        departure = Column(String(50), nullable=False)
        arrival = Column(String(50), nullable=False)
        departure_time = Column(DateTime, nullable=False)
        arrival_time = Column(DateTime, nullable=False)
        ticket_price = Column(Numeric(10, 2), nullable=False)
        users = Column(String(50), nullable=False)

    # define Flight class
    class flight(Base):
        __tablename__ = 'flights'

        id = Column(Integer, primary_key=True, autoincrement=True)
        departure_state = Column(String(255), nullable=False)
        arrival_state = Column(String(255), nullable=False)
        departure_time = Column(DateTime, nullable=False)
        arrival_time = Column(DateTime, nullable=False)
        price = Column(Numeric(10, 2), nullable=False)

    class users(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(255), nullable=False)
        password = Column(String(255), nullable=False)
        email = Column(String(255), nullable=False)

    # create tables
    Base.metadata.create_all(engine)

    # insert states
    session.execute(text("""
    INSERT INTO states(state_code, state_name)
    VALUES
        ('AL','Alabama'),
        ('AK','Alaska'),
        ('AZ','Arizona'),
        ('AR','Arkansas'),
        ('CA','California'),
        ('CO','Colorado'),
        ('CT','Connecticut'),
        ('DC','District of Columbia'),
        ('DE','Delaware'),
        ('FL','Florida'),
        ('GA','Georgia'),
        ('HI','Hawaii'),
        ('ID','Idaho'),
        ('IL','Illinois'),
        ('IN','Indiana'),
        ('IA','Iowa'),
        ('KS','Kansas'),
        ('KY','Kentucky'),
        ('LA','Louisiana'),
        ('ME','Maine'),
        ('MD','Maryland'),
        ('MA','Massachusetts'),
        ('MI','Michigan'),
        ('MN','Minnesota'),
        ('MS','Mississippi'),
        ('MO','Missouri'),
        ('MT','Montana'),
        ('NE','Nebraska'),
        ('NV','Nevada'),
        ('NH','New Hampshire'),
        ('NJ','New Jersey'),
        ('NM','New Mexico'),
        ('NY','New York'),
        ('NC','North Carolina'),
        ('ND','North Dakota'),
        ('OH','Ohio'),
        ('OK','Oklahoma'),
        ('OR','Oregon'),
        ('PA','Pennsylvania'),
        ('RI','Rhode Island'),
        ('SC','South Carolina'),
        ('SD','South Dakota'),
        ('TN','Tennessee'),
        ('TX','Texas'),
        ('UT','Utah'),
        ('VT','Vermont'),
        ('VA','Virginia'),
        ('WA','Washington'),
        ('WV','West Virginia'),
        ('WI','Wisconsin'),
        ('WY','Wyoming');
    """))
    session.commit()

    # insert flights
    session.execute(text("""
    INSERT INTO flights (departure_state, arrival_state, departure_time, arrival_time, price)
    SELECT s1.state_name, s2.state_name,
        (NOW() + INTERVAL '1 day' * FLOOR(RANDOM() * 30))::DATE + TIME '00:00:00' + INTERVAL '1 hour' * FLOOR(RANDOM() * 24),
        (NOW() + INTERVAL '1 day' * FLOOR(RANDOM() * 30) + INTERVAL '1 day' + INTERVAL '1 hour' * FLOOR(RANDOM() * 24))::DATE + TIME '00:00:00' + INTERVAL '1 hour' * FLOOR(RANDOM() * 24),
        CAST((RANDOM() * 500 + 50) AS NUMERIC(10,2))
    FROM states s1
    CROSS JOIN states s2
    WHERE s1.state_name != s2.state_name
    AND (NOW() + INTERVAL '1 day' * FLOOR(RANDOM() * 30))::DATE + TIME '00:00:00' + INTERVAL '1 hour' * FLOOR(RANDOM() * 24) <
        (NOW() + INTERVAL '1 day' * FLOOR(RANDOM() * 30) + INTERVAL '1 day' + INTERVAL '1 hour' * FLOOR(RANDOM() * 24))::DATE + TIME '00:00:00' + INTERVAL '1 hour' * FLOOR(RANDOM() * 24);

    """))
    session.commit()

    # organize flights
    session.execute(text("""
    UPDATE flights
    SET arrival_time = departure_time, departure_time = arrival_time
    WHERE arrival_time < departure_time;
    """))
    session.commit()

    # close the connection
    session.close()
    engine.dispose()


def generate_ticket_id():
    length = 10
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods = ['POST', 'GET'])
def sign_up_page():
    return render_template('sign-up.html')

@app.route('/sign-in', methods = ['POST', 'GET'])
def sign_in_page():
    return render_template('sign-in.html')


@app.route('/shop', methods = ['POST', 'GET'])
def shop_page():
    if request.method == 'POST':
      try:
        email = request.form['email']
      except:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        user_database_password = cursor.execute(f"SELECT password FROM users WHERE name = '{session['username']}'")
        user_database_password = cursor.fetchall()
        if user_database_password[0][0] == password:
          try:
            user_existing_flights = cursor.execute(f"SELECT departure,arrival,departure_time,arrival_time FROM tickets WHERE users = '{session['username']}'")
            user_existing_flights = cursor.fetchall()
            return render_template('shop.html', name = username, flights = user_existing_flights)
          except:
            return render_template('shop.html', name = username)
        else:
            return render_template('wrong.html')
      else:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        cursor.execute(f"INSERT INTO users (name,password,email) VALUES('{session['username']}','{password}','{email}')")
        conn.commit()
        return render_template('shop.html', name = username)


@app.route('/ticket',  methods = ['POST', 'GET'])
def buy_page():
    if request.method == 'POST':
        try:
          destination = request.form['buy-destination']
          departure = request.form['buy-deprature']
          flight_match = cursor.execute(f"SELECT * FROM flights WHERE arrival_state  = '{destination}' AND departure_state = '{departure}'")
          flight_match = cursor.fetchall()
          flight_array = []
          for i in range(len(flight_match)):
              flight_object = {"departure":flight_match[i][1], "destination":flight_match[i][2], "departure_time": flight_match[i][3].strftime("%Y-%m-%d %H:%M"), "arrival_time": flight_match[i][4].strftime("%Y-%m-%d %H:%M"), "price": f'{flight_match[i][5]} $'}
              flight_array.append(flight_object)
          return render_template('ticket.html',available_flights = flight_array, action = 'buy')
        except:
          session['delete-destination'] = request.form['delete-destination']
          session['delete-departure'] = request.form['delete-departure']
          flight_match = cursor.execute(f"SELECT * FROM tickets WHERE arrival  = '{session['delete-destination']}' AND departure = '{session['delete-departure']}' AND users = '{session['username']}'")
          flight_match = cursor.fetchall()
          return render_template('ticket.html', flight = flight_match[0] , action = 'delete')


@app.route('/payment', methods = ['POST','GET'])
def purchase_page():
    if request.method == 'POST':
        session['global_user_destination'] = request.form['destination']
        session['global_user_departure'] = request.form['departure']
        session['global_user_departure_time'] = request.form['departure_time']
        session['global_user_arrival_time'] = request.form['arrival_time']
        session['global_price'] = request.form['price'].replace('$','')
        return render_template('payment.html')


@app.route('/success',  methods = ['POST', 'GET'])
def success_page():
    if request.method == 'POST':
        ticket_id = generate_ticket_id()
        cursor.execute(f"INSERT INTO tickets (ticket_number,departure,arrival,departure_time,arrival_time,ticket_price,users) VALUES('{ticket_id}','{session['global_user_departure']}','{session['global_user_destination']}','{session['global_user_departure_time']}','{session['global_user_arrival_time']}','{session['global_price']}','{session['username']}')")
        conn.commit()
        return render_template('success.html', ticket = ticket_id)


@app.route('/delete', methods = ['POST', 'GET'])
def delete_page():
    if request.method == 'POST':
        correct_ticket_id = cursor.execute(f"SELECT ticket_number FROM tickets WHERE arrival  = '{session['delete-destination']}' AND departure = '{session['delete-departure']}' AND users = '{session['username']}'")
        correct_ticket_id = cursor.fetchall()
        ticket_id = request.form['delete-ticket-id']
        if correct_ticket_id[0][0] == ticket_id:
            cursor.execute(f"DELETE FROM tickets WHERE ticket_number = '{ticket_id}'")
            conn.commit()
            return render_template('delete.html')
        else:
            return render_template('wrong.html')

first_iteration = 0
if __name__ == "__main__":
    if first_iteration == 0 or os.path.exists("stop.txt") :
        create_data()
        first_iteration = 1
        file = open("stop.txt", "w")
        file.write("stop using create_data function")

    app.run(host="0.0.0.0")