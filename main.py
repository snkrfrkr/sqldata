import os, time
import requests
import http.client
from datetime import datetime
import mysql.connector

pi3 = "192.168.123.215:5000"
pi2 = "localhost:5000"
try:
    while(True):
        cnx = mysql.connector.connect(user='grafana', password='lociam',
                                  host='127.0.0.1',
                                  database='db_values')

        cur = cnx.cursor()

        conn_pi2 = http.client.HTTPConnection(pi2)
        conn_pi3 = http.client.HTTPConnection(pi3)

        payload = ""

        now = datetime.now()

        conn_pi3.request("GET", "/temp", payload)
        conn_pi2.request("GET", "/temp", payload)

        res_sleep = conn_pi3.getresponse()
        res_life = conn_pi2.getresponse()
        data_sleep = res_sleep.read()
        data_life = res_life.read()
        time.sleep(2)

        read_t_sleep = data_sleep.decode("utf-8").strip()
        read_t_life = data_life.decode("utf-8").strip()

        conn_pi3.request("GET", "/feuchte", payload)
        conn_pi2.request("GET", "/feuchte", payload)

        res_sleep = conn_pi3.getresponse()
        res_life = conn_pi2.getresponse()
        data_sleep = res_sleep.read()
        data_life = res_life.read()
        time.sleep(2)

        read_h_sleep = data_sleep.decode("utf-8").strip()
        read_h_life = data_life.decode("utf-8").strip()

        '''
        '''
        read_temp_sleep = float(read_t_sleep)
        read_hum_sleep = float(read_h_sleep)
        read_temp_life = float(read_t_life)
        read_hum_life = float(read_h_life)

        add_data = ("INSERT INTO tab_values "
                   "(temp_sleep, hum_sleep, temp_life, hum_life, zeit) "
                   "VALUES (%s, %s, %s, %s, %s)")

        current_data = (read_temp_sleep, read_hum_sleep, read_temp_life, read_hum_life, now)

        cur.execute(add_data, current_data)

        cnx.commit()

        cur.close()
        cnx.close()
        print(read_temp_sleep)
        print(read_hum_sleep)
        print(read_temp_life)
        print(read_hum_life)
    
except Exception as e:
    print(e)
