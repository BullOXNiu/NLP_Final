#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import time
import pandas as pd
import numpy as np

authenticator = IAMAuthenticator('GuNuWLs7h5Fmgprj8kQGdLHicJYEpseDTaT4dk1yJFDA')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url('https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/35041025-5b0c-4a02-9b3e-cc021ae9ac8f')

folder_path = r'C:\Users\markn\OneDrive\桌面\2020-2021\NLP\Final Project\Noisy Data'

filename_ls = os.listdir(folder_path)
df_result = pd.DataFrame(index=np.arange(1,len(filename_ls)+1), columns=['file_name','result'])
df_result.index.name = 'idx'
for idx, filename in enumerate(filename_ls):
    file_path = os.path.join(folder_path,filename)

    with open(file_path, 'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav'
            ).get_result()
        jtype = json.dumps(speech_recognition_results, indent=2)
        results = json.loads(jtype)
        transcript = results['results'][0]['alternatives'][0]['transcript']
        df_result.loc[idx+1,:] = [filename, transcript]
    time.sleep(0.1)
    if (idx+1)%50 == 0:
        print('processed %d' %(idx+1))

df_result.to_excel(r'/Users/garyge/Desktop/NLP/final_project/IBM_api_audio_result.xlsx')
