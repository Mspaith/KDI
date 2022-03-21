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

You should be able to view the signin page.










