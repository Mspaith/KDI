# KDI Video Archive Natural Language Processing 

In this project, You’ll build a web app that allows users to convert .MP4 files to text using pre train on a Deep learning model call onnx.
The project was to build a purpose-built video Archives platform that will allow a user to seamlessly stream KDI content, without having to use excel spreadsheet or translator. Furthermore, to explore the opportunity of a language learning model that can understand design vernacular using graph databases to see and compare nuances. 
The project was to build a purpose-built video Archives platform that will allow us to seamlessly stream KDI content, without having to use excel spreadsheet, code or hire a developer. Furthermore, to explore the opportunity of a language learning model that can understand design vernacular using graph databases to see and compare nuances. 

[Link] Demo Video


# Dependencies
  - torch, 1.8+
  - torchaudio, latest version bound to PyTorch should work
  - omegaconf, latest just should work
  - onnx, latest just should work
  - onnxruntime, latest just should work

# Architecture 
This project has 3 major parts :
- mp4_text.py - This contains pre train mode onnx that receives wav file which is converted into the text
- template - This folder contains the HTML template (index.html,signup.html,dashboard.html)
- static - This folder contains the css folder with style files
[KDI USER FLOW.pdf](https://github.com/Mspaith/KDI/files/9455707/KDI.USER.FLOW.pdf)

<img width="878" alt="Screen Shot 2022-08-30 at 1 46 49 PM" src="https://user-images.githubusercontent.com/53205087/187518336-c627fefc-bdc0-4370-a4f3-7d98f8844136.png">



## For Developers:
. Comprehensive Documentation begins in the Developer Guide
. To run locally, see project instructions above.

## Quick Start
The local setup can be done for all components. In order to test the full set up, this must be done locally in some capacity. For now we will set up all components including AWS cloud and containerizing implimentation. 

# Pre-Rec:
- Python and Virtual Environmeent Installation
- Pre-recs for AWS, is setting it up
- User must install Filezilla to upload the code in the backend AWS server
-     Using sfttp protocol wit the following host ID:  54.196.228.231 
-     Port MS is 22
- Upload files to Filezilla and connect to AWS

# Running the project

- Ensure that you are in the project home directory.Run mp4_text.py using below command to start Flask Project

python mp4_text.py

By default, flask will run on port 5000.

Navigate to URL http://127.0.0.1:5000/ (or) http://localhost:5000

You should be able to view the signin page.
- 1) Jump into the signup page and put your requried cridentials. after the sucessful signin jump into the signin page. 
- The user will be redirect into the dashboard page. 
- 2)On dashboard page the user has to insert the mp4.Using moviepy to convert the mp4 into mp3. 
- 3)Then using the library audioseqmet to convert mp3 into wav and split the wav file into multipal chunks. The reasoning is to get the best optimization from the model. The shorter the wav length the quicker results we get. 
- 4) We use the silero model as [onnx](https://github.com/snakers4/silero-models) to convert the wav into text for grammmer correction.
- 5) We use the T5 grammer correction model to allow the user to download the text. Included in the T5 model is word count located in the CSV file. Users will get the text with word count.


## Research Summary 
This project reduces the the practise and continued data that is delivered in the KDI bi weekly exchanges to better see trends and patter of particular design venecular. 

# Contact 
Implimentation and Model: Paith Philemon
Business: Eugene Park







