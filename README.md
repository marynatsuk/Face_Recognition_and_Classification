# Face_Recognition_and_Classification
This repository contains programming scripts for face recognition in videos and their classification based on the following characteristics: Gender, Age and Emotion.
  1. Gender and Age classification model: https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/weights.28-3.73.hdf5
  2. Emotion classification model trained on [IMDB-WIKI dataset](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/) using CNN.
  3. Face recognition uses Haar-Classifier
  
# Program overview
This project was created to be used via surveillance systems to get reports based on customers` demographics. Using this analysis shops would be able to get more detailed statistics of their customers' audience and be able to provide more customer-friendly services.
Project uses next technologies:
  - tkinter for UI
  - MySQL database for saving results of the analysis
  - YoutubeAPI for parsing video data from Youtube
  - Pandas, matplotlib and Seborn for results analysis and visual presentation

## Program interface (overview)
![image](https://user-images.githubusercontent.com/73252923/217768630-f548e820-26d8-441f-99fc-319ff9dafd87.png)

## Face recognition and classification
![image](https://user-images.githubusercontent.com/73252923/217768219-885dd01c-cb60-4554-89d3-54fb07264fad.png)

## Video clasiffication 
![image](https://user-images.githubusercontent.com/73252923/217769050-96ad754a-2246-4d0d-ac8e-963d5ec9b130.png)
---
# How to use this program?
1. Download the project as an archive.
2. Open projects in IDE of your choice.
3. Install libraries based on `requirements.txt`
4. Run `main.py`

# Additional information
If you have any additional questions, contact me on [LinkedIn](https://www.linkedin.com/in/marinatsuk/)
