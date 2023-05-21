%matplotlib inline
import matplotlib.pyplot as plt
import IPython.display as ipd

import os
import json
import math
import torch
from torch import nn
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
    parser.add_argument("--text", nargs="+", default= "xin ch\xE0o")

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

    _ = utils.load_checkpoint(path_to_model, net_g, None)


    dataset = TextAudioSpeakerLoader(hps.data.validation_files, hps.data)
    collate_fn = TextAudioSpeakerCollate()
    loader = DataLoader(dataset, num_workers=8, shuffle=False,
        batch_size=1, pin_memory=True,
        drop_last=True, collate_fn=collate_fn)
    data_list = list(loader)

    with torch.no_grad():
    x, x_lengths, spec, spec_lengths, y, y_lengths, sid_src = [x.cuda() for x in data_list[0]]
    sid_tgt1 = torch.LongTensor([1]).cuda()
    sid_tgt2 = torch.LongTensor([2]).cuda()
    sid_tgt3 = torch.LongTensor([4]).cuda()
    audio1 = net_g.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt1)[0][0,0].data.cpu().float().numpy()
    audio2 = net_g.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt2)[0][0,0].data.cpu().float().numpy()
    audio3 = net_g.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt3)[0][0,0].data.cpu().float().numpy()
    print("Original SID: %d" % sid_src.item())
    ipd.display(ipd.Audio(y[0].cpu().numpy(), rate=hps.data.sampling_rate, normalize=False))
    print("Converted SID: %d" % sid_tgt1.item())
    ipd.display(ipd.Audio(audio1, rate=hps.data.sampling_rate, normalize=False))
    print("Converted SID: %d" % sid_tgt2.item())
    ipd.display(ipd.Audio(audio2, rate=hps.data.sampling_rate, normalize=False))
    print("Converted SID: %d" % sid_tgt3.item())
    ipd.display(ipd.Audio(audio3, rate=hps.data.sampling_rate, normalize=False))