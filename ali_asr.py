#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -*- coding: UTF-8 -*-
# Python 2.x引入httplib模块
# import httplib
# Python 3.x引入http.client模块
import http.client

import json
import os
import time
import pandas as pd
import numpy as np

def process(request, token, audioFile) :

    # 读取音频文件
    with open(audioFile, mode = 'rb') as f:
        audioContent = f.read()

    host = 'nls-gateway.cn-shanghai.aliyuncs.com'

    # 设置HTTP请求头部
    httpHeaders = {
        'X-NLS-Token': token,
        'Content-type': 'application/octet-stream',
        'Content-Length': len(audioContent)
        }


    # Python 2.x使用httplib
    # conn = httplib.HTTPConnection(host)

    # Python 3.x使用http.client
    conn = http.client.HTTPConnection(host)

    conn.request(method='POST', url=request, body=audioContent, headers=httpHeaders)

    response = conn.getresponse()
    #print('Response status and response reason:')
    #print(response.status ,response.reason)

    body = response.read()
    try:
        #print('Recognize response is:')
        body = json.loads(body)
        # print(body)

        status = body['status']
        if status == 20000000 :
            result = body['result']
            # print('Recognize result: ' + result)
        else :
            print('Recognizer failed!')

    except ValueError:
        print('The response is not json format string')

    conn.close()
    return result



appKey = 'Jl2XD2SUnYTtcIYp'
token = 'db63eb037e3548dfaf0b95a66f66f377'

# 服务请求地址
url = 'http://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'

# 音频文件
audioFile = '/path/to/nls-sample-16k.wav'
format = 'wav'
sampleRate = 16000
enablePunctuationPrediction  = True
enableInverseTextNormalization = True
enableVoiceDetection  = False

# 设置RESTful请求参数
request = url + '?appkey=' + appKey
request = request + '&format=' + format
request = request + '&sample_rate=' + str(sampleRate)

if enablePunctuationPrediction :
    request = request + '&enable_punctuation_prediction=' + 'true'

if enableInverseTextNormalization :
    request = request + '&enable_inverse_text_normalization=' + 'true'

if enableVoiceDetection :
    request = request + '&enable_voice_detection=' + 'true'

# print('Request: ' + request)

folder_path = r'/Users/garyge/Desktop/NLP/final_project/audio_f0001'

filename_ls = os.listdir(folder_path)
df_result = pd.DataFrame(index=np.arange(1,len(filename_ls)+1), columns=['file_name','result'])
df_result.index.name = 'idx'
for idx, filename in enumerate(filename_ls):
    file_path = os.path.join(folder_path,filename)
    result = process(request, token, file_path)
    df_result.loc[idx+1,:] = [filename, result]
    time.sleep(0.2)
    if (idx+1)%50 == 0:
        print('processed %d' %(idx+1))
df_result.to_excel(r'/Users/garyge/Desktop/NLP/final_project/ali_api_audio_result.xlsx')
