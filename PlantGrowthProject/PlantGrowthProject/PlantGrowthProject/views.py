"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from PlantGrowthProject import app
from flask import Flask, jsonify
from flask import abort
import cv2


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/hello/<name>')
def hello(name):
    return "hello" + name



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    img =  cv2.imread('../static/images/cover.jpeg')
    retval, threshold = cv2.threshold(img, 12, 255, cv2.THRESH_BINARY)

    grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    retval1, threshold1 = cv2.threshold(grayscaled, 12, 255, cv2.THRESH_BINARY)

    gaus = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})




if __name__ == '__main__':
    app.run(debug=True)