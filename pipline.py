import os
from access_info import AccessInfo
from gateway_info import GatewayInfo
from file_split import split_by_count, split_by_date, merge_by_date
from settings import Settings

def main(access_filename, login_gateway_filedir, logout_filedir, dates, count, logfilter_filename=''):

    # 按天切割 access 日志
    split_by_date(access_filename)

    # 按天合并 gateway 日志
    merge_by_date(login_gateway_filedir)

    # 生成 access csv 文件
    login_access_filedir, name = os.path.split(access_filename)
    login_access_filedir = os.path.join(login_access_filedir, 'date')
    if not os.path.exists(logout_filedir):
        os.mkdir(logout_filedir)
    for access_filename in os.listdir(login_access_filedir):
        if not os.path.isdir(os.path.join(login_access_filedir, access_filename)):
            if access_filename.split('.')[-1] in dates:
                logout_filename = os.path.join(logout_filedir, access_filename + '.csv')
                split_access_filename = os.path.join(login_access_filedir, access_filename)
                access_info = AccessInfo(split_access_filename, logout_filename)
                access_gen = access_info.get_access_info()
                access_info.gen_to_csv(access_gen)

    # 生成 gateway csv 文件
    merge_gateway_filedir =  os.path.join(login_gateway_filedir, 'date')
    for gateway_filename in os.listdir(merge_gateway_filedir):
        if not os.path.isdir(os.path.join(merge_gateway_filedir, gateway_filename)):
            if gateway_filename.split('.')[-1] in dates:
                logout_filename = os.path.join(logout_filedir, gateway_filename + '.csv')
                merge_gateway_filename = os.path.join(merge_gateway_filedir, gateway_filename)
                gateway_info = GatewayInfo(merge_gateway_filename, logout_filename, logfilter_filename=logfilter_filename)
                gateway_gen = gateway_info.get_gateway_info()
                gateway_info.gen_to_csv(gateway_gen)

    # 按行切割 csv 文件
    if settings.count or settings.count != 0:
        for filename in os.listdir(logout_filedir):
            if not os.path.isdir(os.path.join(logout_filedir, filename)):
                split_by_count(os.path.join(logout_filedir, filename), count)


if __name__ == '__main__':
    settings = Settings()
    dates = settings.dates
    access_filename = settings.access_filename
    login_gateway_filedir = settings.gateway_filedir
    logout_filedir = settings.logout_filedir
    count = settings.count
    logfilter_filename = settings.logfilter_filename

    main(access_filename, login_gateway_filedir, logout_filedir, dates, count)
        
