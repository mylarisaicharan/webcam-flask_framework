from flask import Flask,Response,render_template
import cv2

app = Flask(__name__)                                                             #object created
camera =cv2.VideoCapture(0)                                                       #to capture video and 0 is for webcam

def generate_frames():
    while True:
        
        #read the camera frame
        success,frame=camera.read()                                                 #success and frame are variables,we get boolean values, is camera recording or not
        
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)                                   #encoding into .jpg the frame
            frame=buffer.tobytes()                                                  #converting buffer into bytes
             
        yield(b'--frame\r\n'                                                        #yelid used to generate frames continuoesly 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')           # return gives only few frames

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video') 
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

