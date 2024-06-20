#!/usr/bin/env python3
import requests
import mysql.connector
from datetime import datetime
import pytz

API_KEY = 'e42659b6b45ae7dd9ca5cfc3674528e84a28e254'
HOST = '140.238.244.101'
USER = 'root'
PASSWORD = '1lnli9uELkeWC7GfUQF01an3Yevq7wXbpkM7vskAyMI652tRhUnin4e8gD4DUOjy'
DATABASE = 'Project_X'

def fetch_data(api_key):
    api_url = "https://api.jcdecaux.com/vls/v1/stations"
    contract = "dublin"
    full_url = f"{api_url}?contract={contract}&apiKey={api_key}"

    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def connect_to_database(host, database, user, password):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def insert_data_to_db(conn, data):
    if conn is not None and data is not None:
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO stations (number, name, address, position_lat, position_lng, banking, bonus, status, contract_name, bike_stands, available_bike_stands, available_bikes, last_update)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name=VALUES(name),
        address=VALUES(address),
        position_lat=VALUES(position_lat),
        position_lng=VALUES(position_lng),
        banking=VALUES(banking),
        bonus=VALUES(bonus),
        status=VALUES(status),
        contract_name=VALUES(contract_name),
        bike_stands=VALUES(bike_stands),
        available_bike_stands=VALUES(available_bike_stands),
        available_bikes=VALUES(available_bikes),
        last_update=VALUES(last_update)
        """

        for station in data:
            try:
                last_update = datetime.fromtimestamp(int(station['last_update']) / 1000, pytz.timezone('Europe/Dublin'))
                values = (
                    station['number'], station['name'], station['address'],
                    station['position']['lat'], station['position']['lng'],
                    station['banking'], station['bonus'], station['status'],
                    station['contract_name'], station['bike_stands'],
                    station['available_bike_stands'], station['available_bikes'],
                    last_update
                )
                cursor.execute(insert_query, values)
            except mysql.connector.Error as e:
                print(f"Error inserting data: {e}")
                print(f"Data causing error: {values}")

        conn.commit()
        cursor.close()
        print("Data inserted/updated successfully.")
    else:
        print("No data to insert or database connection is not established.")

def main():
    data = fetch_data(API_KEY)
    conn = connect_to_database(HOST, DATABASE, USER, PASSWORD)
    insert_data_to_db(conn, data)
    if conn is not None:
        conn.close()

if __name__ == "__main__":
    main()
