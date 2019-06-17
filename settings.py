import os
import datetime

class Settings:

    def __init__(self):

        # 定义解析的 access 日志文件
        self.access_filename = './access_login/access.log'
        
        # 定义解析的 gateway 日志目录
        self.gateway_filedir = './gateway_login/'

        # 定义过滤的 order_number 文件
        self.logfilter_filename = ''

        # 定义 access 输出文件
        self.logout_filedir = './logout/'

        # 定义时间范围，为空不限制
        self.start_date = '2019-06-01'
        self.end_date = '2019-06-06'
        self.dates = self.date_range()

        # 定义切割 csv 文件的行数，如果为 0 或 '' 不切割
        self.count = 0

    def date_range(self):
        dates = []
        dt = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
        date = self.start_date[:]
        while date <= self.end_date:
            dates.append(date)
            dt = dt + datetime.timedelta(1)
            date = dt.strftime("%Y-%m-%d")
        return dates

if __name__ == '__main__':
    settings = Settings()
    print(type(settings.dates[0]))
