# -*- coding: utf-8 -*-
from datetime import datetime
import numpy as np
import traceback
import database
import matplotlib.pyplot as plt
import os
import scipy.stats as st


from zb_fun import *
from base_fun import (REF, SD_HHV, SD_LLV, CROSS_ARR, Cal_KDJ, Cal_BIAS, BARSLAST_ARR, Cal_MACD, Cal_VMACD, Cal_CCI,Cal_RSI)
def Return_interva(list,mean):
    list=sorted(list)
    lenth=len(list)-1
    for index,data in enumerate(list):
        if data<mean:
            continue
        elif index<=0.475*lenth:
            return list[0],list[int(lenth*0.95)]
        elif index>=0.525*lenth:
            return list[int(lenth*0.05)],list[lenth]
        else:
            return list[int(index-lenth*0.475)],list[int(index+lenth*0.475)]
def deal_data():
    try:
        import MySQLdb

        stock2NameDic = database.get_id_2_name()

        # start_date = datetime.now().date() #datetime.strptime("2016-11-29", "%Y-%m-%d").date()
        conn = MySQLdb.connect(host='192.168.1.239', user='root', passwd='nb2008xl', db='db_fp_data_new',
                               charset='utf8')
        cur = conn.cursor()
        # 提取最近250个交易日的起始日期
        cur.execute("SELECT DISTINCT code FROM gg_day ORDER BY code ASC")
        stock_stock_code_list = []
        for line in cur.fetchall():
            stock_stock_code = line[0]
            stock_stock_code_list.append(stock_stock_code)
        cur.close()
        conn.close()

        zb_list = ['Cal_MACD','Cal_VMACD', 'Cal_BIAS','Cal_KDJ','Cal_CCI','Cal_RSI']
        f = open('all_secuid.txt', 'w')
        for stock_stock_code in stock_stock_code_list:
            if 'if00' == stock_stock_code:
                continue
            if not os.path.exists('C:/Users/user/Desktop/secuid'):
                os.mkdir('C:/Users/user/Desktop/secuid')
            if not os.path.exists('C:/Users/user/Desktop/secuid/%s'%(stock_stock_code)):
                os.mkdir('C:/Users/user/Desktop/secuid/%s' % (stock_stock_code))
            all_datas = database.init_one_stock_data(stock_stock_code, 500)
            if stock_stock_code in all_datas:
                datas = all_datas[stock_stock_code]
            for zb_name in zb_list:
                b_tag = eval(zb_name)(datas)
                lenth = len(b_tag)
                if lenth <5:
                    for i in range(lenth):
                        data = []
                        data += [x for x in b_tag[i] if str(x) != 'nan']
                        data_array = np.array(data)
                        u = data_array.mean()
                        std = data_array.std()
                        # data_array_deal = (data_array - u) / std * np.sqrt(len(data))
                        data_array_deal = data_array
                        plt.figure()
                        plt.hist(data_array_deal, bins=100, color='g', normed=True)
                        plt.xlim(np.min(data_array_deal), np.max(data_array_deal))
                        label = "%s_%s_%d" % (stock_stock_code, zb_name, i)
                        s_fit = np.linspace(np.min(data_array_deal), np.max(data_array_deal))
                        plt.plot(s_fit, st.norm(u, std).pdf(s_fit), c='r')
                        plt.title("%s" % (label))
                        plt.savefig('C:\Users\user\Desktop\secuid\%s\%s.jpg' % (stock_stock_code,label))
                        plt.close()   #avoid warning too much
                        a, b = Return_interva(data, u)
                        if i == 0:
                            f.write('%s,%s,%d,%f,%f,' % (stock_stock_code, zb_name, lenth, a, b))
                        elif i == lenth - 1:
                            f.write('%f,%f\n' % (a, b))
                        else:
                            f.write('%f,%f,'% (a, b))
                else:
                    try:
                        data = []
                        data += [x for x in b_tag if str(x) != 'nan']
                        data_array = np.array(data)
                        u = data_array.mean()
                        std = data_array.std()
                        # data_array_deal = (data_array - u) / std * np.sqrt(len(data))
                        data_array_deal = data_array
                        plt.figure()
                        plt.hist(data_array_deal, bins=100, color='g', normed=True)
                        plt.xlim(np.min(data_array_deal), np.max(data_array_deal))
                        label = "%s_%s" % (stock_stock_code, zb_name)
                        s_fit = np.linspace(np.min(data_array_deal), np.max(data_array_deal))
                        plt.plot(s_fit, st.norm(u, std).pdf(s_fit), c='r')
                        plt.title("%s" % (label))
                        plt.savefig('C:\Users\user\Desktop\\secuid\%s\%s.jpg' % (stock_stock_code, label))
                        plt.close()
                        a, b = Return_interva(data, u)
                        f.write('%s,%s,1,%f,%f\n' % (stock_stock_code, zb_name, a, b))
                    except:
                         print "stock_code=%s zb_name=%s" % (stock_stock_code, zb_name), b_tag
        f.close()
    except:
        traceback.print_exc()
if __name__ == "__main__":
    deal_data()


