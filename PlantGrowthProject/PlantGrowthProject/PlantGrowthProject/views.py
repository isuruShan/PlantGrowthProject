"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, json, json, make_response, Response
from PlantGrowthProject import app
from flask.app import Flask
import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os
from flask import Flask, request
from werkzeug import secure_filename
from flask import send_file
import mahotas

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
@app.route('/home')
def home():
    #pimg.Compromise()
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

@app.route('/Report_02')
def Report_02():
    """Renders the about page."""
    return render_template(
        'Report_02.html',
        title='Report_02',
        year=datetime.now().year,
        message='Your application description page.'
    )

def Compromise(imageFile):
    #Detection of color green
    #START
    # load the image
    #img = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\5.JPG)
    #img = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\6.JPG") #Input the image
    image = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\Capture.png")

    #Color detection Green color
    #START

    # define range of green color in RGB
    lower_green = np.array([17, 15, 100], dtype = "uint8") #60,100,50
    upper_green = np.array([50, 56, 200], dtype = "uint8") #60,255,255

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower_green, upper_green)
    output = cv2.bitwise_and(image, image, mask = mask)
    #END

    #the Otsu's binarization
    gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    markers = cv2.watershed(output,markers)
    output[markers == -1] = [255,0,0]

    nWhitePixels = cv2.countNonZero(thresh) #this gives number of white pixels you have in the image
    numberAll = thresh.size #this gives number of all pixels you have in the image
    print(nWhitePixels)
    print(numberAll)

    cv2.imshow("images", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return imageFile

@app.route('/ajax', methods =  ['GET', 'POST'])
def ajax() :
    target = os.path.join(APP_ROOT, 'images/')
  
    if not os.path.isdir(target):
        os.mkdir(target)
    lstOfUploadedImages = os.listdir(os.path.join(APP_ROOT, 'images/'))
    ArrangedImages = sorted(lstOfUploadedImages)
    nBlackPixelArrylst = list()
    nAllPixelArrylst = list()

    for nImage in ArrangedImages:
        destination = "/".join([target, nImage])
        #Detection of color green
        #START
        # load the image
        imageNoHSV = cv2.imread(destination)
        image = cv2.cvtColor(imageNoHSV, cv2.COLOR_BGR2HSV)

        #Color detection Green color
        #START
        # define range of green color in HSV
        lower_green0 = np.array([45, 100, 50], dtype = "uint8")
        lower_green1 = np.array([60, 100, 50], dtype = "uint8")
        upper_green0 = np.array([60, 255, 255], dtype = "uint8")
        upper_green1 = np.array([75, 255, 255], dtype = "uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask0 = cv2.inRange(image, lower_green0, upper_green0)
        mask1 = cv2.inRange(image, lower_green1, upper_green1)

        #mask = cv2.inRange(image, lower_green, upper_green)
        output = cv2.bitwise_or(image, image, mask = mask0 + mask1)
        #END

        #the Otsu's binarization
        gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        # noise removal
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)

        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers+1

        # Now, mark the region of unknown with zero
        markers[unknown==255] = 0
        markers = cv2.watershed(output,markers)
        output[markers == -1] = [255,0,0]

        nWhitePixels = cv2.countNonZero(thresh) #this gives number of white pixels you have in the image
        numberAll = thresh.size #this gives number of all pixels you have in the image

        nBlackPixel = numberAll - nWhitePixels
        nBlackPixelArrylst.append(nBlackPixel)
        nAllPixelArrylst.append(numberAll)

        #cv2.imshow("images", thresh)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    FrameSize = "Test"
    f_read = open('FrameSize.txt', encoding='utf-8')
    for line in f_read:
        FrameSize = line
    f_read.close()

    jObj = {}
    jObj["FrameSize"]=FrameSize
    jObj["nBlackPixelArrylst"] = nBlackPixelArrylst
    jObj["nAllPixelArrylst"] = nAllPixelArrylst
    return Response(json.dumps(jObj), mimetype='application/json')

@app.route('/uploader' , methods = ['GET', 'POST'])
def Compromise():
     if request.method == 'POST':

        #Getting the FrameSize input and saving that in a txt file
        #START
        FrameSize = request.form["FrameSize"]
        with open("FrameSize.txt", "w+") as f_write:
            f_write.write(FrameSize)
        #END

        target = os.path.join(APP_ROOT, 'images/')

        if not os.path.isdir(target):
            os.mkdir(target)

        #here we save output examples
        targetForOutput = os.path.join(APP_ROOT, 'imagesOut/')
        if not os.path.isdir(targetForOutput):
            os.mkdir(targetForOutput)

        nBlackPixelArrylst = list()
        nAllPixelArrylst = list()
        noOfFiles = len(request.files.getlist("file"))
        if noOfFiles>1:
            for upFile in request.files.getlist("file"):
                
                filename = upFile.filename
                destination = "/".join([target, filename])
                
                upFile.save(destination)
                #Detection of color green
                #START
                # load the image
                imageNoHSV = cv2.imread(destination)
                image = cv2.cvtColor(imageNoHSV, cv2.COLOR_BGR2HSV)

                #Color detection Green color
                #START

                # define range of green color in RGB

                lower_green0 = np.array([45, 100, 50], dtype = "uint8") 
                lower_green1 = np.array([60, 100, 50], dtype = "uint8") 
                upper_green0 = np.array([60, 255, 255], dtype = "uint8") 
                upper_green1 = np.array([75, 255, 255], dtype = "uint8") 

                # find the colors within the specified boundaries and apply
                # the mask

                mask0 = cv2.inRange(image, lower_green0, upper_green0)
                mask1 = cv2.inRange(image, lower_green1, upper_green1)

                #mask = cv2.inRange(image, lower_green, upper_green)
                output = cv2.bitwise_or(image, image, mask = mask0 + mask1)
                #END

                #the Otsu's binarization
                gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
                ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

                # noise removal
                kernel = np.ones((3,3),np.uint8)
                opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

                # sure background area
                sure_bg = cv2.dilate(opening,kernel,iterations=3)

                # Finding sure foreground area
                dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
                ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

                # Finding unknown region
                sure_fg = np.uint8(sure_fg)
                unknown = cv2.subtract(sure_bg,sure_fg)

                # Marker labelling
                ret, markers = cv2.connectedComponents(sure_fg)

                # Add one to all labels so that sure background is not 0, but 1
                markers = markers+1

                # Now, mark the region of unknown with zero
                markers[unknown==255] = 0
                markers = cv2.watershed(output,markers)
                output[markers == -1] = [255,0,0]

                nWhitePixels = cv2.countNonZero(thresh) #this gives number of white pixels you have in the image
                numberAll = thresh.size #this gives number of all pixels you have in the image

                nBlackPixel = numberAll - nWhitePixels
                nBlackPixelArrylst.append(nBlackPixel)
                nAllPixelArrylst.append(numberAll)

                filename = upFile.filename
                destinationForOutput = "/".join([targetForOutput, filename])
                cv2.imwrite(destinationForOutput, thresh)

                #cv2.imshow("images", thresh)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

        ObjData = {}
        ObjData["nBlackPixelArrylst"] = nBlackPixelArrylst
        ObjData["nAllPixelArrylst"] = nAllPixelArrylst
        jsonData = json.dumps(ObjData)

        response = make_response(render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'))
        
        response.headers.set('Content-Security-Policy', "default-src 'self'")
        response.jsonData = jsonData

        #return response
        return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.',
        jsonData = jsonData)

if __name__ == '__main__':
    app.run(debug = True)

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
    app.run(port=50000, debug=True)