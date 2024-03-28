from flask import Flask,request,render_template,flash,redirect,url_for,jsonify
import cvzone
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import re
from chatbot_testing import ChatBot

app = Flask(__name__)
app.secret_key = 'akwged19823ybda239ihd'

model = tf.keras.models.load_model("model/cancer_model1.h5")
@app.route('/')
# @app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            flash('Welcome, admin!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')
    

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.form['username']
#     password = request.form['password']
#     flash(f'Account created for {username}!','success')
#     return redirect(url_for('index'))


def preprocess(image_path):
    img = image.load_img(image_path, target_size=(96,96))
    img_array = image.img_to_array(img)
    img_array = img_array/255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/predict',methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        file_path = 'static/assests/temp.jpg'
        uploaded_file.save(file_path)
        preprocessed_image = preprocess(file_path)
        print(uploaded_file)
        prediction = model.predict(preprocessed_image)
        predicted_label = np.round(prediction.flatten()).astype('int')
        # Remove the temporary file
        os.remove(file_path)
        print(predicted_label[0])
        # Convert numpy.int32 or numpy.int64 to Python native int before returning
        return jsonify({'prediction': int(predicted_label[0])})
    else:
        return render_template('Predict.html')

@app.route('/chat', methods=['GET','POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form.get('message') 
        if not user_message:
            return jsonify({"response": "Please provide a question."})
        bot = ChatBot()
        result = bot.ask(user_message)
        return jsonify({"response": result})
    else:
        return render_template('chatbot.html')
@app.route('/payment', methods=['GET'])
def payment():
    return render_template('payment.html')
if __name__ == '__main__':
    app.run(debug=True)