# Battery
Sort batteries by category

## Main Idea
![summary](https://github.com/emi-cd/category_recognize/blob/img/imgs/flow.png?raw=true)



# Testing environment
python : 3.6.6  
Packages : Please look requirements.txt  
tesseract 3.05.02  
OS : macOS High Sierra 10.13.2


# Setup
## 1) Set directory  
Set directory like below. But you don't need to prepare 'train_data', 'UNKNOWN' and 'videos' directory.  
**Please be careful that you have to put the model.** That model is used for prediction.   

.  
├── **take_video.py**  
├── **main.py**  
├── **labeling_CNN.py**  
├── **labeling_OCR.py**   
├── **retraining.py**  
├── README  
├── requirements.txt  
├── **models**  
│   ├── model.h5  
│   └── ...  
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

## 2) Install packages  
You can install necessary packages with the following command.  
```
pip install -r requirements.txt  
```

## 3) Install tesseract  
- If you have homebrew  
```
brew install tesseract  
```



# Description
	1) Take videos. These videos go to 'videos' directory.  
		Video's name is  battery's ID.  
	2) Label the battery using by CNN. It return ['ALKALINE', 'LIION', 'NIMH', 'NICD'] or 'UNKNOWN'.  

	If Label is not 'UNKNOWN':  
		3) Print ID, LABEL  
		4) Delete the video.  
	Else:  
		3) Go to OCR. OCR recognize charactor. Also it should return ['ALKALINE', 'LIION', 'NIMH', 'NICD'] or 'UNKNOWN'.

		If Label is not 'UNKNOWN':  
			4) These frames from the video go to 'train_data' directory.  
			5) Print ID, LABEL  
			6) Delete the video.  
		Else:  
			4) These frames from the video go to 'UNKNOWN' directory.  
			5) Delete the video.  

## take_video.py  
Take videos. And add that video to videos directory.  
You have to attach USB camera. If a red circle is in the upper left, it is recorded. If you want to stop this program, please enter 'q'. It is repeating.  
The first battery is 00000, the next is 00001, 00002, .... When that number goes to 99999, it goes back to 00000. Since this number is saved, even if you stop the program once, it starts with the next number. 
```
python take_video.py
```
- Argment
	- '-T', '--time' : You can decide ength of video. Default is 20 seconds.
- Output : The window like below will appear  
![video](https://github.com/emi-cd/category_recognize/blob/img/imgs/video.png?raw=true)


## main.py  
The main flow.  Retrain the model or label the battery. This program is repeating.
Please see detail each packages.
```
python main.py
```

```
python main.py --retrain
```
- Argment
	- '-R', '--retrain' : Mode of Retraining.
	- '-I', '--input' : Path to the input video directory. Default is './videos'.
	- '--model' : Choose model. Default is "./models/model.h5". In labeling mode, it is used for prediction and retraining this model in retraining mode.
	- '-T', '--train' : It is use in retraining mode. Path to the training data directory. Default is './train_data'.
	- '--debug' : Debug mode. Show more information when it running.
- Output : Output is like below. [ID, Label]   
	![Output image](https://github.com/emi-cd/category_recognize/blob/img/imgs/output.png?raw=true)

### labeling_CNN.py  
Determine the label of battery from the vide by CNN.
```  
python labeling_CNN.py --path ./videos/00000.mov -M ./models/model.h5 -N 5
```
Now IMAGE_SIZE is 224 and **CORRECT_PROB is 0.95**. If the accuracy is 95% or more, the label will be determined. Less than 95% will be 'UNKNOWN'.

- Argment
	- '-P', '--path' : Path to the video. It is required.
	- '-M', '--model' : Choose model. Default is "./models/model.h5". But you have to choice a valid model.
	- '-N', '--number' : Get this number of frames from the video and determine the label. Default is 3.  
	So it decide from 3 labels like ['NIMH', 'NIMH', 'NIMH'] and it returns 'NIMH'. If it gets ['NIMH', 'NIMH', 'UNKNOWN'] or ['NIMH', 'NIMH', 'NICD'], it returns 'UNKNOWN'.
	- '--debug' : Debug mode. Show more information when it running.



### labeling_OCR.py  
Determine the label of battery from the video by OCR.  
```
python labeling_OCR.py --path './videos/00000.mov' --debug
```
The frames from movie go to 'train_data' directory. For example, OCR detect 'NIMH', these frames go to 'train_data/NIMH'. (You can change this directory by using argment.) If OCR cannot detect Label, these data go to 'UNKNOWN' directory.

- Argment
	- '-P', '--path' : Path to the video. Default is './videos'.
	- '-F', '--frame' : Pick this number of frames from video. Default is 30.
	- '-D', '--dest' : The path to the training data. Default is './train_data'.
	- '--debug' : Debug mode. Show more information when it running.

### retraining.py  
Retraining the model.
```
python retraining.py --model ./models/model.h5 --debug
```
- Argment
	- '-M', '--model' : The model for retraining. Default is "./models/model.h5". But you have to choice a valid model.
	- '-T', '--train' : Path to the train data. Default is ./train_data'. It have to have each labels directory.
	- '-N', '--number' : The number os training data. Default is 1000. After retraining, the data is reduced to this number.
	- '--debug' : Debug mode. Show more information when it running.

### split_video.py  
This include cropping function and video_2_frame function.  
You can use like below.
```python
import split_video
imgs = split_video.video_2_frames(./movie.mov, 30)
```
It returns list of 'Image' objects.



# Usage
## Main flow
You should run this 2 programs.

```
python main.py  
```
```
python take_video.py
```

## Retraining the model
It takes time, so I recommend that you do it occasionally.
```
python main.py -R
```
