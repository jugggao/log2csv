import re
import csv
from urllib.parse import unquote

class GatewayInfo:

    def __init__(self, login_filename, logout_filename, logfilter_filename=''):
        self.login_filename = login_filename
        self.logout_filename = logout_filename
        self.logfilter_filename = logfilter_filename
    
    def order_number_filter(self):
        with open(self.logfilter_filename, encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            column_1 = [row[0] for row in reader]
            return column_1

    def get_gateway_info(self):
        re_time = re.compile(r'^\d{4}-\d{2}-\d{2}[ ]\d{2}:\d{2}:\d{2}.\d+\b')
        re_ip = re.compile(r'(?<=ip\[).*?(?=\])')
        re_session_id = re.compile(r'(?<="sessionId":").*?(?=")')
        re_result_url = re.compile(r'(?<="resultUrl":").*?(?=")')
        re_open_id = re.compile(r'(?<="openId":").*?(?=")')
        re_order_number = re.compile(r'(?<="orderNumber":")\d+?(?=")')
        
        ip = session_id = result_url = open_id = ''
        with open(self.login_filename, encoding='utf-8') as f:
            for line in f:
                if 'orderNumber' in line and 'sessionId' in line:
                    line = unquote(str(line)) # URL 解码
                    line = line.strip()
                    line = line.replace(",", " ")
                    order_number = re_order_number.search(line)
                    if order_number != None:
                        order_number = order_number.group()
                    else:
                        order_number = ''
                    time = re_time.search(line).group()
                    if 'ip[' in line:
                        ip = re_ip.search(line).group()
                    if 'sessionId' in line:
                        session_id = re_session_id.search(line)
                        if session_id != None:
                            session_id = session_id.group()
                        else:
                            session_id = ''
                    if 'resultUrl' in line:
                        result_url = re_result_url.search(line)
                        if result_url != None:
                            result_url = result_url.group()
                        else:
                            result_url = ''
                    if 'openId' in line:
                        open_id = re_open_id.search(line)
                        if open_id != None:
                            open_id = open_id.group()
                        else:
                            open_id = ''
                    if self.logfilter_filename and (order_number not in self.order_number_filter()):
                        continue
                    else:
                        yield time, ip, session_id, order_number, result_url, open_id
                            
    def gen_to_csv(self, info_gen):
        titles = ["time", "ip", "session_id", "order_number", "result_url", "open_id", ]
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

    login_filename = './gateway_login/gateway.log.2019-06-03'
    logout_filename = './logout/gateway_all.2019-06.03.csv'
    # logfilter_filename = './log_filter/orderNumber_filter.csv'
    logfilter_filename = ''

    gateway_info = GatewayInfo(login_filename, logout_filename, logfilter_filename=logfilter_filename)
    gateway_info_gen = gateway_info.get_gateway_info()
    gateway_info.gen_to_csv(gateway_info_gen)
