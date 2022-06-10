# KDI
In this project,You’ll  build a web app that allows users to convert MP4 to text using pre train Deep learning model onnx.

# Dependencies
  - torch, 1.8+
  - torchaudio, latest version bound to PyTorch should work
  - omegaconf, latest just should work
  - onnx, latest just should work
  - onnxruntime, latest just should work

# Project Structure
This project has 3 major parts :
- mp4_text.py - This contains pre train mode onnx that receives wav file which is converted into the text
- template - This folder contains the HTML template (index.html,signup.html,dashboard.html)
- static - This folder contains the css folder with style files

# Running the project

- Ensure that you are in the project home directory.Run mp4_text.py using below command to start Flask Project

python mp4_text.py

By default, flask will run on port 5000.

Navigate to URL http://127.0.0.1:5000/ (or) http://localhost:5000

You should be able to view the signin page.First the user have to jump into the signup page and put their requried cridentials 
and then  jump into the signin page after the sucessful signin the user will be redirect into the dashboard page.On dashboard page the user have to insert the mp4.Using moviepy convert the mp4 into mp3 then i audioseqmet to convert mp3 into wav and split the wav file into the multipal chunks  the reason the get the optimization from the model the shorter the wav length the quicker the result we get.we used  silero model as onnx( [to](https://github.com/snakers4/silero-models) convert wav into the 










