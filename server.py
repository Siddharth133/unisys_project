import flask as Flask,request,render_template,flash,redirect,url_for,jsonify
import cv2
import numpy as np
from keras.preprocessing import image
from keras.models import load_model

app = Flask(__name__)
app.secret_key = 'akwged19823ybda239ihd'
model = load_model('cancer_model.h5')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        flash( 'Login success','success')
    else:
        flash('Login failed','danger')
    redirect(url_for('index'))
    

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    flash(f'Account created for {username}!','success')
    return redirect(url_for('index'))


def preprocess(image_path):
    image = image.load_img(image_path, target_size=(96,96))
    image = image.img_to_array(image)
    image = image/255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict')
def predict():
    img = form.image.data
    # ye form wala dekh na hoga frontend se thoda
    preprocessed_image = preprocess(img)    
    prediction = model.predict(preprocessed_image)
    predicted_label = np.round(prediction.flatten()).astype('int')
    return jsonify({'prediction': predicted_label[0]})

if __name__ == '__main__':
    app.run(debug=True)