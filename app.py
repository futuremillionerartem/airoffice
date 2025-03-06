from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# Конфигурация БД
DB_CONFIG = {
    "dbname": "Аiroffice",
    "user": "postgres",
    "password": "POSTRESQL_2020",
    "host": "localhost",
    "port": "5432"
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/passengers')
def get_passengers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Получаем пассажиров с их билетами
        cursor.execute('''
            SELECT p.*, COUNT(t.ticketID) as tickets_count 
            FROM Passenger p 
            LEFT JOIN Ticket t ON p.passengerID = t.passengerID 
            GROUP BY p.passengerID
            ORDER BY p.last_name
        ''')
        passengers = cursor.fetchall()

        return jsonify([{
            'id': p[0],
            'name': f'{p[1]} {p[2]}',
            'birth': p[3].strftime('%d.%m.%Y'),
            'email': p[4],
            'phone': p[5],
            'tickets': p[6]
        } for p in passengers])

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/add_passenger', methods=['POST'])
def add_passenger():
    data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Passenger 
            (first_name, last_name, date_of_birth, email, phone)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING passengerID
        ''', (
            data['firstName'],
            data['lastName'],
            data['birthDate'],
            data['email'],
            data['phone']
        ))

        passenger_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'id': passenger_id})

    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)