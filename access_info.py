#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
# from collections import namedtuple
from urllib.parse import unquote

# AccessInfo = namedtuple('AccessInfo', 
#                         ['timestamp','clientip', 'request', 'referer', 'mobile', 'classNumber',
#                          'token', 'umid', 'adtag', 'type', 'tagValue', 'channel'])

class AccessInfo:

    def __init__(self, login_filename, logout_filename):
        self.login_filename = login_filename
        self.logout_filename = logout_filename

    def get_access_info(self):
        re_timestamp = re.compile(r'(?<="@timestamp":").*?(?=")')
        re_clientip = re.compile(r'(?<="clientip":").*?(?=")')
        re_request = re.compile(r'(?<="request":").*?(?=")')
        re_referer = re.compile(r'(?<="referer":").*?(?=")', re.S)
        re_mobile = re.compile(r'(?<=mobile=)\d+')
        re_class_number = re.compile(r'(?<=classNumber=)\d+')
        re_token = re.compile(r'(?<=token=).*?(?=&|/|%2F)')
        re_umid = re.compile(r'(?<=umid=).*?(?=&)')
        re_adtag = re.compile(r'(?<=adtag=).*?(?=&|")', re.I)
        re_type = re.compile(r'(?<=type=).*?(?=&|")')
        re_tag_value = re.compile(r'(?<=tagValue=).*?(?=&|")')
        re_channel = re.compile(r'(?<=channel=).*?(?=[ ]|&|")')

        timestamp = clientip = request = referer = mobile = class_number = token = umid = adtag = type = tag_value = channel =  ""

        with open(self.login_filename, encoding='utf-8') as f:
            for line in f:
                line = unquote(str(line)) # URL 解码
                line = line.strip()
                line = line.replace(",", " ")
                if len(line) != 0:
                    if '@timestamp' in line:
                        timestamp = re_timestamp.search(line).group()
                    if 'clientip":"' in line:
                        clientip = re_clientip.search(line).group()
                    if 'request":"' in line:
                        request =  re_request.search(line).group()
                    if 'referer":"' in line:
                        referer =  re_referer.search(line).group()
                    # line_dict = eval(line)
                    # if '@timestamp' in line:
                    #     timestamp = line_dict['@timestamp']
                    # if 'clientip":"' in line:
                    #     timestamp = line_dict['clientip']
                    # if 'request":"' in line:
                    #     request = line_dict['request']
                    # if 'referer":"' in line:
                    #     referer = line_dict['referer']
                    if '?mobile=' in line:
                        mobile =  re_mobile.search(line)
                        if mobile != None: 
                            mobile = mobile.group()
                        else:
                            mobile = ''
                    if 'classNumber=' in line:
                        class_number = re_class_number.search(line)
                        if class_number != None:
                            class_number = class_number.group()
                        else:
                            class_number = ''
                    if 'token=' in line:
                        token = re_token.search(line).group()  
                    if 'umid=' in line:
                        umid = re_umid.search(line).group()
                    if 'adtag=' in line or 'ADTAG=' in line:
                        adtag = re_adtag.search(line).group()
                    if 'type=' in line:
                        type = re_type.search(line).group()
                    if 'tagValue=' in line:
                        tag_value = re_tag_value.search(line).group()
                    if 'channel=' in line:
                        channel = re_channel.search(line).group()
                    if adtag != "" or type != "" or tag_value != "" or channel != "":
                        yield (timestamp, clientip, request, referer, mobile, class_number, token, umid, adtag, type, tag_value, channel)

    def gen_to_csv(self, info_gen):
        titles = ["timestamp", "clientip", "request", "referer", "mobile", "class_number", "token", "umid", "adtag", "type", "tag_value", "channel"]
        print('write start %s' % self.logout_filename)
        with open(self.logout_filename, 'w', encoding='utf-8') as f:
            for title in titles:
                f.write(str(title))
                f.write(",")
            f.write("\n")
        
            for line in info_gen:
                for i in line:
                    f.write(str(i).strip())
                    f.write(",")
                f.write("\n")

if __name__ == '__main__':
    pass

        



