from flask import Flask, request, Response, render_template
import logging
import psycopg2
from datetime import datetime, timezone
import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib.dates as mdates

app = Flask(__name__,  template_folder='template', static_folder='static')
logging.basicConfig(filename='pythonflasksensor.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s'
                    ' : %(message)s')


conn = psycopg2.connect(database="sensors",
                        host="127.0.0.1",
                        user="postgres",
                        password="password",
                        port="5432")



@app.route("/")
def hello_world():

    app.logger.info('Info level log')
    app.logger.warning('Warning level log')

    # return "<p>Hello, World2 Other branch!</p>"
    return render_template('index.html')

@app.route('/reading', methods=['POST'])
def handle_post():
    app.logger.info('Received POST request'+ request.form['temp'])
    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO sensor_data(reading_datetime, temp_reading, humidity_reading)
        VALUES (%s, %s, %s);
        """
        dt = datetime.now(timezone.utc)
        data = (dt, request.form['temp'], request.form['hum'])
        cursor.execute(insert_query, data)
        conn.commit()

    except psycopg2.Error as e:
        print("Database error:", e)
    finally:
        cursor.close()
    return "POST request received" , 200

@app.route('/temp', methods=['GET'])
def chart():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT reading_datetime, temp_reading FROM sensor_data")
        rows = cursor.fetchall()
        pd.DataFrame(data=rows)
        df = pd.DataFrame(rows, columns=['reading_datetime', 'temp_reading'])
        df['reading_datetime'] = pd.to_datetime(df['reading_datetime'])
        df['temp_reading'] = pd.to_numeric(df['temp_reading'], errors='coerce')

        df.set_index('reading_datetime', inplace=True)
        df.plot(title='Sensor Data Over Time', figsize=(15, 5))
        plt.xlabel('Time')
        plt.ylabel('Sensor Readings')
        plt.legend(['Temperature'])
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))

        image_stream = io.BytesIO()

        plt.savefig(image_stream, format='png')
        
        image_stream.seek(0)
        return Response(image_stream, mimetype='image/png')
    except FileNotFoundError:
        print("File not found error: chart.png")
    except pd.errors.EmptyDataError:
        print("Pandas empty data error: No data to plot")
    except psycopg2.Error as e:
        print("Database error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
        return "Error occurred while generating chart", 500
    # Ensure cursor is closed even if an error occurs
    finally:
        cursor.close()
    return "Chart data fetched", 200


@app.route('/humidity', methods=['GET'])
def chart_humidity():
    try:
        
        cursor = conn.cursor()
        cursor.execute("SELECT reading_datetime, humidity_reading FROM sensor_data")
        rows = cursor.fetchall()
        pd.DataFrame(data=rows)
        df = pd.DataFrame(rows, columns=['reading_datetime', 'humidity_reading'])
        df['reading_datetime'] = pd.to_datetime(df['reading_datetime'])
        df['humidity_reading'] = pd.to_numeric(df['humidity_reading'], errors='coerce')

        df.set_index('reading_datetime', inplace=True)
        df.plot(title='Sensor Data Over Time', figsize=(15, 5))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))
        plt.xlabel('Time')
        plt.ylabel('Sensor Readings')
        plt.legend(['Humidity'])
        image_stream2 = io.BytesIO()

        plt.savefig(image_stream2, format='png')
        
        image_stream2.seek(0)
        return Response(image_stream2, mimetype='image/png')
    except FileNotFoundError:
        print("File not found error: chart.png")
    except pd.errors.EmptyDataError:
        print("Pandas empty data error: No data to plot")
    except psycopg2.Error as e:
        print("Database error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
        return "Error occurred while generating chart", 500
    # Ensure cursor is closed even if an error occurs
    finally:
        cursor.close()
    return "Chart data fetched", 200


if __name__ == "__main__":
    app.run()