#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import base64
import pandas as pd
import numpy as np

IS_PY3 = sys.version_info.major == 3
 
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

API_KEY = '6W1mzIL9pWfgDos1y3R9GToN'
SECRET_KEY = 'jQRexujW3tLvANtLLmpuETqOTrdadzRB'

# 文件格式
FORMAT = 'wav'  # 文件后缀只支持 pcm/wav/amr

CUID = '123456PYTHON'
# 采样率
RATE = 16000;  # 固定值

#RESULT_DIR = os.getcwd()+'\\transcript'


# 普通版

DEV_PID = 1737;  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有

# 极速版 打开注释的话请填写自己申请的appkey appSecret ，并在网页中开通极速版（开通后可能会收费）

#DEV_PID = 1737
#ASR_URL = 'http://vop.baidu.com/server_api'
#SCOPE = 'brain_enhanced_asr'  # 有此scope表示有asr能力，没有请在网页里开通极速版

class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
#     params = {'grant_type': 'client_credentials',
#               'client_id': API_KEY,
#               'client_secret': SECRET_KEY}
#     post_data = urlencode(params)
#     post_data = post_data.encode('utf-8')
#     req = Request(TOKEN_URL, post_data)
#     try:
#         f = urlopen(req)
#         result_str = f.read()
#     except URLError as err:
# #        print('token http response http code : ' + str(err.code))
#         result_str = err.read()
#     result_str = result_str.decode()

# #    print(result_str)
#     result = json.loads(result_str)
# #    print(result)
#     if ('access_token' in result.keys() and 'scope' in result.keys()):
#         if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
#             raise DemoError('scope is not correct')
# #        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
#         return result['access_token']
#     else:
#         raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str =  result_str.decode()

    #print(result_str)
    result = json.loads(result_str)
    #print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        #print(SCOPE)
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
       # print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """

if __name__ == '__main__':
    token = fetch_token()

    """
    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(httpHandler)
    urllib2.install_opener(opener)
    """
    folder_path = r'/Users/garyge/Desktop/NLP/final_project/audio_f0001'

    filename_ls = os.listdir(folder_path)
    df_result = pd.DataFrame(index=np.arange(1,len(filename_ls)+1), columns=['file_name','result'])
    df_result.index.name = 'idx'
    for idx, filename in enumerate(filename_ls):
        file_path = os.path.join(folder_path,filename)
        id = filename.split('_')[0]

        speech_data = []
        with open(file_path, 'rb') as speech_file:
            speech_data = speech_file.read()
        length = len(speech_data)
        # if length == 0:
        #     print('file %s length read 0 bytes' % file_path)
        # else:
        #     params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
        #     params_query = urlencode(params);

        #     headers = {
        #         'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
        #         'Content-Length': length
        #     }

        #     url = ASR_URL + "?" + params_query
        if length == 0:
            raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
        speech = base64.b64encode(speech_data)
        if (IS_PY3):
            speech = str(speech, 'utf-8')
        params = {'dev_pid': DEV_PID,
             #"lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
        post_data = json.dumps(params, sort_keys=False)
#            print("url is", url);
#            print("header is", headers)
#req = Request(ASR_URL + "?" + params_query, speech_data, headers)
        req = Request(ASR_URL, post_data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json') 
        try:
            begin = timer()
            f = urlopen(req)
            result_str = f.read()
#                print("Request time cost %f" % (timer() - begin))
        except URLError as err:
            print('asr http response http code : ' + str(err.reason))
            result_str = err.read()
        if (IS_PY3):
            result_str = str(result_str, 'utf-8')
        try:
            body = json.loads(result_str)
    #            print(body)
            status = body['err_no']
            if status == 0:
                result = body['result'][0]
                df_result.loc[idx+1,:] = [filename,result]
            else:
                df_result.loc[idx+1,:] = [filename,'']
        except ValueError:
            print('The response is not json format string')
        time.sleep(0.2)
        if (idx+1)%50 == 0:
            print('processed %d' %(idx+1))
        if (idx==500):
            break

    df_result.to_excel(r'/Users/garyge/Desktop/NLP/final_project/baidu_api_audio_result.xlsx')
