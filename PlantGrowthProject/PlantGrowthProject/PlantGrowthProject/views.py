"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from PlantGrowthProject import app, ProcessImg
#from PlantGrowthProject.ProcessImg import Compromise

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
#Compromise
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
        
        #execfile('ProcessImg.py')
        #os.system("python ProcessImg.py")
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
