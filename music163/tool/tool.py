# -*- coding:utf-8 -*-

import base64
from Crypto.Cipher import AES

# result type:
# 100: artist
# 10:  album
# 1:   song
_RESULT_TYPE = 10
_URL_WEAPI_CLOUDSEARCH_GET_WEB = "http://music.163.com/weapi/cloudsearch/get/web?csrf_token="
_MODULUS = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
_NONCE = '0CoJUm6Qyw8W8jud'
_PUB_KEY = '010001'


def aes_encrypt(text, sec_key):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(sec_key, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


# 获取参数
def get_params(page):  # page为传入页数
    first_key = _NONCE
    second_key = 16 * 'F'
    if page == 1:  # 如果为第一页
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = aes_encrypt(first_param, first_key)

    else:
        offset = str((page - 1) * 20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')
        h_encText = aes_encrypt(first_param, first_key)
    h_encText = aes_encrypt(h_encText, second_key)
    return h_encText


# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey
