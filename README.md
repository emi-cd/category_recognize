# Battery
Sort batteries by category


## Main Idea
![summary](https://github.com/emi-cd/category_recognize/blob/img/imgs/summary.jpg?raw=true)


# Dependency
python : 3.6.6  
Packages : Please look requirements.txt  
tesseract : 4.0.0


# Setup
1) Set directory like below.  
.  
├── take_video.py  
├── main.py  
├── labeling_CNN.py  
├── labeling_OCR.py   
├── retraining.py  
├── README  
├── requirements.txt  
├── models  
│   ├── model1002_vgg16.h5  
│   └── old_model1002_vgg16.h5  
├── train_data  
│   ├── ALKALINE  
│   │   ├── 00000_0.jpg  
│   │   └── ...  
│   ├── LIION  
│   │   ├── 00001_0.jpg  
│   │   └── ...  
│   ├── NICD  
│   │   ├── 00002_0.jpg  
│   │   └── ...  
│   └── NIMH  
│       ├── 00003_0.jpg  
│       └── ...  
├── UNKNOWN  
│   └── 00004  
│       ├── 00004_0.jpg  
│       └── ...  
└── videos  
    ├── IMG_0120.mov  
    └── ...  
2) Install packages  
> pip install -r requirements.txt  
3) Install tesseract  
- If you have homebrew  
> brew install tesseract  


# Description
1) Take videos. These videos go to 'videos' directory.  
	Video's name is  battery's ID.  
2) Label the battery using by CNN. It return ['Alkaline', 'LIION', 'NIMH', 'NICD'] or 'UNKOWN'.  

If Label is not 'UNKNOWN':  
	3) Print ID, LABEL  
	4) Delete the video.  
	
Else:  
	3) Go to OCR. OCR recognize charactor. Also it should return ['Alkaline', 'LIION', 'NIMH', 'NICD'] or 'UNKOWN'.  
	
	If Label is not 'UNKNOWN':  
		4) These frames from the video go to 'train_data' directory.  
		5) Print ID, LABEL  
		6) Delete the video.  
		
	Else:  
		4) These frames from the video fo to 'UNKNOWN' directory.  
		5) Delete the video.  
		

## take_video.py  
	Take videos. Add a video to videos directory.  
	> python take_video.py
## main.py  
	The main flow.  Retrain the model or label the battery.
	> python main.py --mode LABEL  
	or  
	> python main.py --mode RETRAIN
### labeling_CNN.py  
	Determine the label of battery from the video. Use OCR.  
	> python labeling_CNN.py --path ./videos/00000.mov -M ./models/model.h5 --debug -N 3
### labeling_OCR.py  
	Determine the label of battery from the video. Use CNN.  
	> python labeling_OCR.py --path './videos/00000.mov' --debug
### retraining.py  
	Retraining the model. 
	> python retraining.py --model ./models/model.h5 --debug 
### split_video.py  
	This include cropping function and video_2_frame function.  
	Please use as a module.


# Usage
## Main flow
	> python main.py --mode LABEL  
	and  
	> python take_video.py
## Retraining the model 
	> python main.py --mode RETRAIN
