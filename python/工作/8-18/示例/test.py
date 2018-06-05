# -*- coding: utf-8 -*-
import traceback
import database
import matplotlib.pyplot as plt
import scipy.stats as st
import os
from zb_fun import *
import sys
sys.path.append("../profile")
from sd_profile import sd_profile
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
@sd_profile("test.prof")
def deal_data():
    if not os.path.exists('C:/Users/user/Desktop/dp'):
        os.mkdir('C:/Users/user/Desktop/dp')
    # sql_list=['dp_day','dp_m60','dp_m30','dp_m15','dp_m5']
    sql_list = ['dp_day']
    for sql_name in sql_list:
        zb_list = ['Cal_MACD', 'Cal_VMACD', 'Cal_BIAS', 'Cal_KDJ', 'Cal_CCI', 'Cal_RSI']
        all_datas = database.init_dp_data_mn(sql_name, start_date=datetime(2000, 1, 1, 0, 0, 0).date())
        if not os.path.exists('C:/Users/user/Desktop/dp/%s'%(sql_name)):
            os.mkdir('C:/Users/user/Desktop/dp/%s' % (sql_name))
        f = open('C:/Users/user/Desktop/dp/%s/write_interval.txt'%(sql_name), 'w')
        for code in all_datas:
            datas = all_datas[code]
            for zb_name in zb_list:
                b_tag = eval(zb_name)(datas)
                lenth = len(b_tag)
                # print "stock_stock_code=%s"%(code),lenth,zb_name,type(b_tag),b_tag
                if lenth <= 3:
                    for i in range(lenth):
                        data = []
                        data += [x for x in b_tag[i] if str(x) != 'nan']
                        data_array = np.array(data)
                        u = data_array.mean()
                        std = data_array.std()
                        data_array_deal = data_array
                        plt.figure()
                        plt.hist(data_array_deal, bins=100, color='g', normed=True)
                        plt.xlim(np.min(data_array_deal), np.max(data_array_deal))
                        label = "%s_%s_%d" % (code, zb_name, i)
                        s_fit = np.linspace(np.min(data_array_deal), np.max(data_array_deal))
                        plt.plot(s_fit, st.norm(u, std).pdf(s_fit), c='r')
                        plt.title("%s" % (label))
                        plt.savefig('C:\Users\user\Desktop\dp\%s\%s.jpg' % (sql_name, label))
                        plt.close()
                        a, b = Return_interva(data, u)
                        if i == 0:
                            f.write('%s,%s,%d,%f,%f,' % (code, zb_name, lenth, a, b))
                        elif i == lenth - 1:
                            f.write('%f,%f\n' % (a, b))
                        else:
                            f.write('%f,%f,' % (a, b))
                else:
                    # try:
                    data_temp = []
                    data_temp += [x for x in b_tag if str(x) != 'nan']
                    data=[]
                    for d in data_temp:
                        if d >-10000 and d<10000:
                            data.append(d)
                    data_array = np.array(data)
                    u = data_array.mean()
                    std = data_array.std()
                    data_array_deal = data_array
                    plt.figure()
                    plt.hist(data_array_deal, bins=100, color='g', normed=True)
                    plt.xlim(np.min(data_array_deal), np.max(data_array_deal))
                    label = "%s_%s" % (code, zb_name)
                    s_fit = np.linspace(np.min(data_array_deal), np.max(data_array_deal))
                    plt.plot(s_fit, st.norm(u, std).pdf(s_fit), c='r')
                    plt.title("%s" % (label))
                    plt.savefig('C:\Users\user\Desktop\dp\%s\%s.jpg' % (sql_name, label))
                    plt.close()
                    a, b = Return_interva(data, u)
                    f.write('%s,%s,1,%f,%f\n' % (code, zb_name, a, b))
                    # except:
                    #     print "stock_code=%s zb_name=%s" % (code, zb_name),lenth, b_tag
        f.close()
if __name__ == "__main__":
    deal_data()
