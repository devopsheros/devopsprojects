from flask import Flask, render_template, request, session
import psycopg2, random, string, secrets, os



app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

print(os.environ['POSTGRES_DB'])
conn = psycopg2.connect(database=f"{os.environ['POSTGRES_DB']}", user=f"{os.environ['POSTGRES_USER']}", password=f"{os.environ['POSTGRES_PASSWORD']}", host=f"{os.environ['POSTGRES_HOST']}",port='5432')
cursor = conn.cursor()


def generate_ticket_id():
    length = 10
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/')
def sign_up_page():
    return render_template('sign-up.html')

@app.route('/sign-in')
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
        print(ticket_id, correct_ticket_id)
        if correct_ticket_id[0][0] == ticket_id:
            cursor.execute(f"DELETE FROM tickets WHERE ticket_number = '{ticket_id}'")
            conn.commit()
            return render_template('delete.html')
        else:
            return render_template('wrong.html')


if __name__ == "__main__":
    app.run(debug=True)