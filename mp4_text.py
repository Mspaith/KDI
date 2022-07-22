from flask import request
import requests
import json
import datetime
import re
import os
import psycopg2
from io import StringIO
import csv
import Caribe as cb
from collections import Counter
from werkzeug.utils import secure_filename
from flask import Flask,url_for, render_template, session, redirect, json, send_file,flash,jsonify
from pydub import AudioSegment
import onnx
import torch
import onnxruntime
from omegaconf import OmegaConf
from moviepy.editor import *
from pydub.utils import make_chunks
import pandas as pd
import glob
from pathlib import Path
from happytransformer import TTSettings
from happytransformer import  HappyTextToText
from more_itertools import sliced
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import  seaborn as sns
from nltk.corpus import stopwords
stop = stopwords.words('english')


app=Flask(__name__,static_folder=os.path.join(os.path.dirname(__file__),"static"))
upload_lcation = os.path.join(os.path.dirname(__file__),"static")
app.config["UPLOAD_FOLDER"]=upload_lcation

ALLOWED_EXTENSIONS = set(['mp4'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS






conn = psycopg2.connect(
   database="KDI_DB", user='postgres', password='', host='127.0.0.1', port= '5432')


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

    # dir_name = app.config["UPLOAD_FOLDER"]+"//"+user_name
    dir_name = os.path.join(app.config["UPLOAD_FOLDER"],user_name)
    try:
        os.makedirs(dir_name)
    except:
        print("this is error")


    if len(first_name) ==1 and len(last_name)==1 and len(email)==1 and len(password)==1:
        pass
    else:
        cursor.execute('''select user_user_name from kdi_user''')
        users=cursor.fetchall()
        conn.commit()
        user_name_list=[]
        for i in users:
            user_name_list.append(i[0])
        print(user_name_list)
        if user_name in user_name_list:
                flash("Username is already exit")
                return render_template('signup.html')
        else:
            cursor.execute("insert into kdi_user (user_first_name, user_last_name, user_email, user_password, user_user_name) values ('{0}','{1}','{2}','{3}','{4}')".format(first_name,last_name,email,password,user_name))
            conn.commit()
            return redirect(url_for('index'))






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
            # app.config["UPLOAD_FOLDER"]=app.config["UPLOAD_FOLDER"]+"\\"+username
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],username, filename))

            mp3_folder=filename[:-4]
            mp3_folder_location = os.path.join(app.config["UPLOAD_FOLDER"],mp3_folder)
            try:
                os.makedirs(mp3_folder_location)
            except:
                print("folder already exist")

            mp4_file=os.path.join(app.config["UPLOAD_FOLDER"],username,filename)


            videoclip = VideoFileClip(mp4_file)

            mp3_file=os.path.join(app.config["UPLOAD_FOLDER"],mp3_folder,mp3_folder+".mp3")
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file)

            audioclip.close()
            videoclip.close()


            sound = AudioSegment.from_mp3(mp3_file)
            mp3_folder_location_wav = os.path.join(app.config["UPLOAD_FOLDER"],mp3_folder+"wav")

            try:
                os.makedirs(mp3_folder_location_wav)
            except:
                print("folder already exist")

            sound.export(os.path.join(app.config["UPLOAD_FOLDER"],mp3_folder+"wav",mp3_folder+".wav"), format="wav")

            myaudio = AudioSegment.from_file(os.path.join(app.config["UPLOAD_FOLDER"],mp3_folder+"wav",mp3_folder+".wav"), "wav")
            chunk_length_ms = 80000
            chunks = make_chunks(myaudio,chunk_length_ms)
            count=0

            wav_folder_location_chunks = os.path.join(app.config["UPLOAD_FOLDER"],mp3_folder+"chunks")

            try:
                os.makedirs(wav_folder_location_chunks)
            except:
                print("folder already exist")

            for i, chunk in enumerate(chunks):
                count=count+1
                chunk_name = "{0}.wav".format(i)
                print ("exporting", chunk_name)
                chunk.export(os.path.join(app.config["UPLOAD_FOLDER"],mp3_folder+"chunks",chunk_name), format="wav")


            #
            language = 'en'
            _, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt', language=language)
            (read_batch, split_into_batches,
             read_audio, prepare_model_input) = utils

            torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml', 'models.yml')
            print("test1")
            models = OmegaConf.load('models.yml')
            available_languages = list(models.stt_models.keys())
            assert language in available_languages
            print("test2")
            #torch.hub.download_url_to_file(models.stt_models.en.latest.onnx, 'model.onnx', progress=True)
            onnx_model = onnx.load('model.onnx')
            print("test3")
            onnx.checker.check_model(onnx_model)
            print("test")
            ort_session = onnxruntime.InferenceSession("model.onnx")
            print("test")
            #
            data=[]
            print(count)
            for i in range(count):
                i=str(i)
                test_files = [os.path.join(app.config["UPLOAD_FOLDER"],mp3_folder+"chunks",i+'.wav')] #wavname
                print(test_files)
                batches = split_into_batches(test_files, batch_size=10)
                input = prepare_model_input(read_batch(batches[0]))

                onnx_input = input.detach().cpu().numpy()
                ort_inputs = {'input': onnx_input}
                ort_outs = ort_session.run(None, ort_inputs)
                decoded = decoder(torch.Tensor(ort_outs[0])[0])
                print(decoded)



                data.append(decoded)

            print(data)
            correction_data=[]
            happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
            beam_settings =  TTSettings(num_beams=5, min_length=1, max_length=1000)
            full_sentences=' '.join(data)
            new_full_sentences=list(sliced(full_sentences, 200))

            for dd in new_full_sentences:
                output_text_1 = happy_tt.generate_text(dd, args=beam_settings)
                print(output_text_1.text)
                correction_data.append(output_text_1.text)




            str1 = ''.join(correction_data)
            new_str1=re.sub('([A-Z])', r' \1', str1)
            word_freq=Counter(new_str1.split()).most_common()
            df_freq=pd.DataFrame(word_freq,columns=["words","count"])


            cursor.execute("select video_name from video_words where video_name=%s",(filename,))
            video_name=cursor.fetchall()
            conn.commit()
            print(video_name,filename)

            video_name_list=[]
            for i in video_name:
                for j in i:
                    video_name_list.append(j)
            print(video_name_list)




            for i in word_freq:
                if filename in video_name_list:
                    pass
                else:
                    cursor.execute("insert into video_words (video_name, video_words, words_count) values (%s,%s,%s);",(filename,i[0],str(i[1])))
            conn.commit()
















            print(filename,mp4_file)


            flash('MP4 successfully uploaded and Press Download Button For The Text')
            df=pd.DataFrame(correction_data,columns=["Text"])
            df=pd.concat([df,df_freq],axis=1)

            global new_filename

            new_filename =filename[:-4]


            #
            df.to_csv(os.path.join(app.config["UPLOAD_FOLDER"],username,new_filename+".csv"),index=False)
            # p="C:\\Users\\C_v\\PycharmProjects\\flask_ONNX\\static"+"\\"+username+"\\"+new_filename+".csv"

            return render_template('dashboard.html',image = url_for("static", filename=username+"/"+filename),data=data,name=username)
        else:
            flash('Allowed  types are  MP4')
            return render_template('dashboard.html',name=username,)

        print(filename,mp4_file)

    return render_template('dashboard.html',name=username)

@app.route('/download')
def download():
    if 'username' in session:
        username= session['username']
    try:

        print(new_filename)
        # new_filename='khu'
        print(app.config["UPLOAD_FOLDER"])
        p=os.path.join(app.config["UPLOAD_FOLDER"],username,new_filename+".csv")



        return send_file(p,
                        mimetype='text/csv',
                        download_name=new_filename+'.csv')
    except Exception as error:
        flash('Hi Please try to Upload MP4 First')
        return redirect(url_for("dashboard"))


@app.route('/videos',methods=['GET','POST'])
def videos():
    if 'username' in session:
        username= session['username']
    path=os.path.join(app.config["UPLOAD_FOLDER"],username)
    print(path)
    all_files = glob.glob(os.path.join(path , "*.mp4"))

    data=[]
    print(all_files)
    for filename in all_files:
        my_path=Path(filename)
        filename=my_path.name
        data.append(filename)
        print(data)

    default_video_name='0'
    video_name=request.form.get('search',default_video_name)

    cursor.execute("select video_words, words_count from video_words where video_name=%s",(video_name,))
    words_count_data=cursor.fetchall()
    words_count_list=[]
    for i in words_count_data:
        words_count_list.append(i)
    new_df=pd.DataFrame(words_count_list,columns=["words","count"])
    df=new_df.head(5)
    df["count"]=df["count"].astype(str).astype('int64')
    words = df["words"].to_numpy()
    count = df["count"].to_numpy()

    fig1, ax1 = plt.subplots()
    ax1.bar(words, count,color='g')
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.title("Top 5 words with occurance")
    figure_loc=os.path.join(path,video_name+".png")
    fig1.savefig(figure_loc,format="png")
    plt.close(fig1)


    new_df["words"]= new_df["words"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    new_df["words"]=new_df["words"].str.strip()
    new_df = new_df.replace(r'^s*$', float('NaN'), regex = True)
    new_df=new_df.dropna()
    new_df=new_df.head(5)
    imp_words = new_df["words"].to_numpy()
    imp_count = new_df["count"].to_numpy()

    fig2, ax2 = plt.subplots()
    ax2.bar(imp_words, imp_count,color='r')
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.title("Top 5 Meaningful words")
    figure_loc_1=os.path.join(path,video_name+"1.png")
    fig2.savefig(figure_loc_1,format="png")
    plt.close(fig2)








    for i in data:
        print(i)
        if i==video_name:
            print(i)
            print(video_name)

            # figure_loc=os.path.join(path,video_name+".png")
            # plot1.savefig(figure_loc,format="png")
            #
            #
            # figure_loc_1=os.path.join(path,video_name+"1.png")
            # plot2.savefig(figure_loc_1,format="png")

            return render_template('videos.html',name=username,search_video=video_name,languages=data,new_df=new_df)




            # return render_template('videos.html',name=username,image = url_for("static", filename=username+"/"+filename))


    return render_template('videos.html',name=username,image=data,languages=data)





if __name__ == '__main__':
    app.secret_key='123'
    app.url_map.strict_slashes = True
    app.run(host="0.0.0.0",debug=True)
