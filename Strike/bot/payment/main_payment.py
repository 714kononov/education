from flask import Flask, request

app = Flask(__name__)

@app.route('/payment_notification', methods=['POST'])
def payment_notification():
    payment_data = request.form
    # Здесь добавьте логику обработки платежа
    return 'OK'

if __name__ == '__main__':
    app.run()
