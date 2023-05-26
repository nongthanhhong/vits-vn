import matplotlib.pyplot as plt
import IPython.display as ipd
import soundfile as sf

import os
import json
import math
import torch
from torch import nn
import librosa
from torch.nn import functional as F
from torch.utils.data import DataLoader

import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
import argparse

from scipy.io.wavfile import write


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", default= "configs/vietnamese_base.json")
    parser.add_argument("--path_to_model", default= "/path/to/model.pth")
    parser.add_argument("--text", default= "xin ch\xE0o")

    args = parser.parse_args()

    config_path = args.config_path

    hps = utils.get_hparams_from_file(config_path)

    net_g = SynthesizerTrn(
        len(symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        **hps.model).cuda()
    
    _ = net_g.eval()

    path_to_model = args.path_to_model

    net_g, _, _, _ = utils.load_checkpoint(path_to_model, net_g, None)


    text = args.text
    stn_tst = get_text(text, hps)
    with torch.no_grad():
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
    ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate, normalize=False))
    sf.write('/content/test.wav', audio, hps.data.sampling_rate)