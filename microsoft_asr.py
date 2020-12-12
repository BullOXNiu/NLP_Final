#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import azure.cognitiveservices.speech as speechsdk
import os
import time
import pandas as pd
import numpy as np

def from_file(file):
    speech_config = speechsdk.SpeechConfig(subscription="f9769ca0076f491e91cbd90a1c6ed97c", region="eastus")
    # audio_input = speechsdk.AudioConfig(filename=r"/Users/garyge/Desktop/NLP/final_project/audio_f0001/f0001_us_f0001_00001.wav")
    
    audio_input = speechsdk.AudioConfig(filename=file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
    result = speech_recognizer.recognize_once_async().get()
    return result.text
    
folder_path = r'C:\Users\markn\OneDrive\桌面\2020-2021\NLP\Final Project\Noisy Data'
filename_ls = os.listdir(folder_path)
df_result = pd.DataFrame(index=np.arange(1,len(filename_ls)+1), columns=['file_name','result'])
df_result.index.name = 'idx'
for idx, filename in enumerate(filename_ls):
    file = os.path.join(folder_path,filename)
    result = from_file(file)
    df_result.loc[idx+1,:] = [filename, result]
    time.sleep(0.1)
    if (idx+1)%50 == 0:
        print('processed %d' %(idx+1))
        
df_result.to_excel(r'C:\Users\markn\OneDrive\桌面\2020-2021\NLP\Final Project\Microsoft_api_audio_result.xlsx')
