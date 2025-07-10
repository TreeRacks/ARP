from flask import Flask, render_template, request
import os
import sys
from rectangle_motion import RectangleMotion
import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO


rclpy.init()
node = RectangleMotion()
app = Flask(__name__)

def draw_rectangle(x_len=0.5, y_len=0.5):
    try:
        print("gonna do it")
        node.draw_square(x_len,y_len)
        # node.draw_SFU()
        print("i did it")
    except KeyboardInterrupt:
        rclpy.shutdown()
    return f"Drew a rectangle with dimensions: {x_len} x {y_len}"

def mystery_action():
    try:
        print("gonna do it")
        # node.draw_square()
        node.draw_SFU()
        print("i did it")
    except KeyboardInterrupt:
        rclpy.shutdown()
    return "You triggered the mystery action!"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'draw_rectangle' in request.form:
            x_len = request.form.get('x_len', '').strip()
            y_len = request.form.get('y_len', '').strip()
            
            if x_len.isdigit() and y_len.isdigit():
                result = draw_rectangle(float(x_len), float(y_len))
            else:
                print("Undefined Dimensions, Running Default")
                result = draw_rectangle()
        elif 'mystery' in request.form:
            result = mystery_action()
    return render_template('index.html', result=result)

@app.route('/kill', methods=['POST'])
def kill():
    GPIO.output(16, GPIO.LOW)
    os._exit(0)  # This will stop the program (Flask server)
if __name__ == '__main__':
    app.run(debug=True)
