from flask import request
import requests
import json
import datetime
import re
import os
import psycopg2
from werkzeug.utils import secure_filename
from flask import Flask,url_for, render_template, session, redirect, json, send_file,flash
from pydub import AudioSegment
import onnx
import torch
import onnxruntime
from omegaconf import OmegaConf
from moviepy.editor import *
from pydub.utils import make_chunks
import pandas as pd


app=Flask(__name__)
upload_lcation = 'C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static'
app.config["UPLOAD_FOLDER"]=upload_lcation

ALLOWED_EXTENSIONS = set(['mp4'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



conn = psycopg2.connect(
   database="KDI_DB", user='postgres', password='', host='127.0.0.1', port= ''
)



conn.autocommit = True

cursor = conn.cursor()



@app.route('/',methods=['GET','POST'])
def index():


    default_username='0'
    username=request.form.get('username',default_username)
    print(username)


    default_password='0'
    password=request.form.get('password',default_password)
    print(password)

    cursor.execute('''select * from kdi_user''')

    users=cursor.fetchall()
    conn.commit()


    for i in users:

        if i[5]==username and i[4]==password:
            session['username']=username
            return render_template('dashboard.html',name=username)




    return render_template('index.html')


@app.route('/signup',methods=['GET','POST'])
def signup():

    default_first_name='0'
    first_name=request.form.get('firstname',default_first_name)

    default_last_name='0'
    last_name=request.form.get('lastname',default_last_name)

    default_email='0'
    email=request.form.get('email',default_email)

    default_password='0'
    password=request.form.get('userpass',default_password)

    default_username='0'
    user_name=request.form.get('username',default_username)

    dir_name = "C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static\\"+user_name
    try:
        os.makedirs(dir_name)
    except:
        print("this is error")


    if len(first_name) ==1 and len(last_name)==1 and len(email)==1 and len(password)==1:
        pass
    else:
        cursor.execute("insert into kdi_user (user_first_name, user_last_name, user_email, user_password, user_user_name) values ('{0}','{1}','{2}','{3}','{4}')".format(first_name,last_name,email,password,user_name))
        conn.commit()
        return render_template('index.html')
    





    return render_template('signup.html')



@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if 'username' in session:
        username= session['username']


    if (request.method=="POST"):

        file = request.files['file1']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"]="C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static"+"\\"+username
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            mp3_folder=filename[:-4]
            mp3_folder_location = "C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static\\"+mp3_folder
            try:
                os.makedirs(mp3_folder_location)
            except:
                print("folder already exist")

            mp4_file=app.config["UPLOAD_FOLDER"]+"\\"+filename


            videoclip = VideoFileClip(mp4_file)

            mp3_file=mp3_folder_location+"\\"+mp3_folder+".mp3"
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file)

            audioclip.close()
            videoclip.close()


            sound = AudioSegment.from_mp3(mp3_file)
            mp3_folder_location_wav = "C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static\\"+mp3_folder+"wav"

            try:
                os.makedirs(mp3_folder_location_wav)
            except:
                print("folder already exist")

            sound.export("C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static"+"\\"+mp3_folder+"wav"+"\\"+mp3_folder+".wav", format="wav")

            myaudio = AudioSegment.from_file(mp3_folder_location_wav+"\\"+mp3_folder+".wav", "wav")
            chunk_length_ms = 80000
            chunks = make_chunks(myaudio,chunk_length_ms)
            count=0

            wav_folder_location_chunks = "C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static\\"+mp3_folder+"chunks"

            try:
                os.makedirs(wav_folder_location_chunks)
            except:
                print("folder already exist")

            for i, chunk in enumerate(chunks):
                count=count+1
                chunk_name = "{0}.wav".format(i)
                print ("exporting", chunk_name)
                chunk.export(wav_folder_location_chunks+"\\"+chunk_name, format="wav")


            #
            language = 'en'


            _, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt', language=language)
            (read_batch, split_into_batches,
             read_audio, prepare_model_input) = utils

            torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml', 'models.yml')
            models = OmegaConf.load('models.yml')
            available_languages = list(models.stt_models.keys())
            assert language in available_languages

            # torch.hub.download_url_to_file(models.stt_models.en.latest.onnx, 'model.onnx', progress=True)
            onnx_model = onnx.load('model.onnx')
            onnx.checker.check_model(onnx_model)
            ort_session = onnxruntime.InferenceSession('model.onnx')
            #
            data=[]
            print(count)
            for i in range(count):
                i=str(i)
                test_files = ["C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static"+"\\"+mp3_folder+"chunks"+"\\"+i+'.wav'] #wavname
                print(test_files)
                batches = split_into_batches(test_files, batch_size=10)
                input = prepare_model_input(read_batch(batches[0]))

                onnx_input = input.detach().cpu().numpy()
                ort_inputs = {'input': onnx_input}
                ort_outs = ort_session.run(None, ort_inputs)
                decoded = decoder(torch.Tensor(ort_outs[0])[0])
                data.append(decoded)

            print(data)






            print(filename,mp4_file)


            flash('Image successfully uploaded and displayed below')

            return render_template('dashboard.html',name=username,data=data,mm=mp4_file)
        else:
            flash('Allowed  types are -> MP4')
            return render_template('dashboard.html',name=username,)

        print(filename,mp4_file)

        return render_template('dashboard.html',name=username)




if __name__ == '__main__':
    app.secret_key='123'
    app.run(debug=True)
