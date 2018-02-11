# -*- coding: UTF-8 -*-

from flask import request
from flask import Flask
from flask import render_template
from ele import ele_red_packet


app = Flask(__name__)


@app.route('/',methods=['POST','GET'])
def phone_number_form():
    if request.method == 'POST':
        phone_number = request.form['phone']
        get_red_packet = ele_red_packet(phone_number)
        return render_template('index.html', phone_number=get_red_packet)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    app.debug=1
