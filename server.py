from flask import Flask,request,render_template,flash,redirect,url_for,jsonify
import cvzone
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re
from chatbot_testing import ChatBot

app = Flask(__name__)
app.secret_key = 'akwged19823ybda239ihd'

model = tf.keras.models.load_model("model/cancer_model1.h5")

@app.route('/')
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
    image = img_array/255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/predict',methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        file_path = 'static/assests/temp.jpg'
        uploaded_file.save(file_path)
        # preprocessed_image = preprocess(file_path)
        print(uploaded_file)
        # prediction = model.predict(preprocessed_image)
        # predicted_label = np.round(prediction.flatten()).astype('int')
        # Remove the temporary file
        os.remove(file_path)
        # return jsonify({'prediction': predicted_label[0]})
        prediction = "yes it is a cancer"
        return jsonify({'prediction': prediction})
    else:
        return render_template('Predict.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message') 
    if not user_message:
        return jsonify({"response": "Please provide a question."})
    bot = ChatBot()
    result = bot.ask(user_message)
    return jsonify({"response": result})


if __name__ == '__main__':
    app.run(debug=True)