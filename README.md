# vits-vn
 Vietnamese TTS  with VITS

original repo: https://github.com/jaywalnut310/vits

## Online training
### colab
Thanks to [vits-finetuning](https://github.com/SayaSS/vits-finetuning)

See my modify [vits-vn](https://colab.research.google.com/drive/1H1u-NTGMMz61uOypK4u6vyJl7DD19-0k?usp=share_link)

# How to use
(Suggestion) Python == 3.7
## Clone this repository
```sh
git clone https://github.com/nongthanhhong/vits-vn.git
```

## Choose cleaners
- Fill "text_cleaners" in config.json
- Edit text/symbols.py
- Remove unnecessary imports from text/cleaners.py
## Install requirements
```sh
pip install -r requirements.txt
```
## Create datasets
### Single speaker
"n_speakers" should be 0 in config.json
```
path/to/XXX.wav|transcript
```
- Example
```
dataset/001.wav|Xin chào
```
### Mutiple speakers
Speaker id should start from 0 
```
path/to/XXX.wav|speaker id|transcript
```
- Example
```
dataset/001.wav|0|Xin chào
```
## Preprocess
If you have done this, set "cleaned_text" to true in config.json
```sh
# Single speaker
python preprocess.py --text_index 1 --filelists path/to/filelist_train.txt path/to/filelist_val.txt

# Mutiple speakers
python preprocess.py --text_index 2 --filelists path/to/filelist_train.txt path/to/filelist_val.txt
```
<!-- ## Build monotonic alignment search
```sh
cd monotonic_align
python setup.py build_ext --inplace
cd ..
``` -->
## Train
```sh
# Single speaker
python train.py -c <config> -m <name_model>

# Mutiple speakers
python train_ms.py -c <config> -m <name_model>
```
## Inference
### Online
See [inference.ipynb](https://colab.research.google.com/drive/1H1u-NTGMMz61uOypK4u6vyJl7DD19-0k?usp=share_link)

