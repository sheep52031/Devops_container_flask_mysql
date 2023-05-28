from flask import Flask, request, render_template
import pymysql
import os
import time

app = Flask(__name__, static_url_path="/source", template_folder="./tmpfolder")

# Configure MySQL
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mysql')
MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD', '')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'shop')



def wait_for_mysql():
    connected = False
    while not connected:
        try:
            mysql = pymysql.connect(host=MYSQL_HOST,
                                    user='root', 
                                    password=MYSQL_ROOT_PASSWORD,
                                    db=MYSQL_DATABASE,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
            
            connected = True
        except pymysql.err.OperationalError as e:
            print("Waiting for MySQL server to be ready...")
            time.sleep(3)

    return mysql

mysql = wait_for_mysql()

# Define the form route
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get the form data
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            # If name or email is missing, render the form again with an error message
            return render_template('index.html', error_msg='Please enter both name and email')


        # Store the data in the database
        with mysql.cursor() as cursor:
            sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
            cursor.execute(sql, (name, email))
        mysql.commit()

        # Return a success message
        return render_template('success.html')
    else:
        # Render the form template
        return render_template('index.html', error_msg='')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


