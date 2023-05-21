# vits-vn
 Vietnamese TTS  with VITS

Original repo: https://github.com/jaywalnut310/vits

Text cleaner inspired by https://github.com/CjangCjengh/vits
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
# If you want to train with other languages, or other textcleaner for vietnamese, the following steps may be helpful
## Choose cleaners

1 - Create: file vietnamese.py in folder "text": setup sub functions for preprocess text, text to ipa 
2 - Add vietnamese_cleaners function to cleaners.py to process text files
3 - Create: file vietnamese_base.json in folder "configs"

- Fill "text_cleaners" in your_config_file.json
- Edit text/symbols.py for your language
- Remove unnecessary imports from text/cleaners.py

## Install requirements
```sh
pip install -r requirements.txt
```
## Create datasets
- Speaker ID should be between 0-803.
- About 50 audio-text pairs will suffice and 100-600 epochs could have quite good performance, but more data may be better. 
- Resample all audio to 22050Hz, 16-bit, mono wav files.
- Audio files should be >=1s and <=10s.
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

- Change 

  +> --text_index: 1 for single speaker | 2 for multiple speakers

  +> --filelists: 2 paths of train.text and val.text

  +> --text_learners: name of your cleaner (vietnamese_cleaners) was added to file cleaners.py before.

  for shorter run -> Change defaut args in preprocess.py 

```sh
# Single speaker
python preprocess.py --text_index 1 --filelists path/to/filelist_train.txt path/to/filelist_val.txt

# Mutiple speakers
python preprocess.py --text_index 2 --filelists path/to/filelist_train.txt path/to/filelist_val.txt
```
Edit "training_files" and "validation_files" in configs/config.json
<!-- ## Build monotonic alignment search
```sh
cd monotonic_align
python setup.py build_ext --inplace
cd ..
``` -->
## Train

- train.py (for single speaker) | train_ms.py (for multiple speakers) 

  +> Change file utils.py line 151 to path that save your model

  +> Change 

    ++> -c : path to config file of vietnamese_base.json

    ++> -m : path to checkpoint models (if existed)

```sh
# Single speaker
python train.py -c <config> -m <name_model>

# Mutiple speakers
python train_ms.py -c <config> -m <name_model>
```
## Inference
### Online
See [inference.ipynb](https://colab.research.google.com/drive/1H1u-NTGMMz61uOypK4u6vyJl7DD19-0k?usp=share_link)

