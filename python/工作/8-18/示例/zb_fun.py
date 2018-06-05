# -*- coding: utf-8 -*-
"""
Created on Wed May 25 14:06:19 2016

@author: Administrator
"""
import sys
sys.path.append('C:/lc/quant/replay_trade')
from base_fun import * 

# 拐头卖的指标
def gt_sell(v_data,n):
    #(MACD_DIF<REF(MACD_DIF,1) AND COUNT(REF(MACD_DIF,1)>=REF(MACD_DIF,2),10)>=10)
    v_data_ref_1 = REF(v_data,1)
    v_data_ref_2 = REF(v_data,2)
    
    flag = (v_data<v_data_ref_1)[-1] and sum((v_data_ref_1>v_data_ref_2)[-1*n:])>=n
    return flag    

# 向下拐头
def gt_down(v_data):
    #v_data_ref_1 = REF(v_data,1)
    #flag = (v_data<v_data_ref_1)[-1]
    return v_data[-1]<v_data[-2]

# 连续最近n周期值往上
def lx_up(v_data,n):
    v_data_ref_1 = REF(v_data,1)
    return sum((v_data>=v_data_ref_1)[-1*n:])>=n

# 向上拐头
def gt_up(v_data):
    #v_data_ref_1 = REF(v_data,1)
    #flag = (v_data<v_data_ref_1)[-1]
    return v_data[-1]>v_data[-2]

# 连续最近n周期值往下
def lx_down(v_data,n):
    v_data_ref_1 = REF(v_data,1)
    return sum((v_data<=v_data_ref_1)[-1*n:])>=n
    
# 获取开盘的分钟数
def get_open_minutes(dt_list):
    
    open_minutes = 0
    for i in range(1,len(dt_list),1):
        open_minutes = open_minutes + 1
        if dt_list[-1*(i+1)].date() != dt_list[-1].date():
            #print "i:" + str(i)
            #print dt_list[i].date().strftime("%Y-%m-%d")
            #print dt_list[-1].date().strftime("%Y-%m-%d")
            return open_minutes
    if dt_list[-1].hour<11 or (dt_list[-1].hour==11 and dt_list[-1].minute<=30):
        return int(dt_list[-1].hour*60+dt_list[-1].minute - 9.5*60)
    else:
        return int(dt_list[-1].hour*60+dt_list[-1].minute - 9.5*60-1.5*60)

# 求n个和函数
def reduce_sum(v_data, n):
    
    result = np.nan * np.ones(v_data.shape)
    
    for i in range(v_data.shape[0]):
        if 0==i:
            result[i] = sum(v_data[-1*n-i:])
        else:
            result[i] = sum(v_data[-1*n-i:-1*i])

# 判断是不是强势股
def is_strong(close, volume, dt_list):
#    黄色线:=SUM(C*V,UP_TO_NOW_MINUTES)/SUM(V,UP_TO_NOW_MINUTES),COLORYELLOW,LINETHICK1;
#   统计时长:=MIN(UP_TO_NOW_MINUTES,15);
#   strong:COUNT(CLOSE>=黄色线,统计时长)>=统计时长*0.8 AND 统计时长>=2;
    #print dt_list
    #print int(dt_list[-1].hour*60+dt_list[-1].minute - 9.5*60)
    open_minutes=get_open_minutes(dt_list)
    #print "open_minutes:" + str(open_minutes)
    #print "dt_list:" + str(dt_list[-1])
    #print "close:" + str(close[-1])
    #print "volume:" + str(volume[-1])
    #print "close:" 
    #print close
    #print dt_list
    count_minute = min(open_minutes,15)
    #print 'count_minute'
    #print count_minute
    strong_array = np.nan * np.ones(count_minute)
    #print strong_array
    for i in range(min(count_minute,len(volume))):
        if i>0:
            
            yellow_line = round(sum( (close*volume)[-1*open_minutes:-1*i] ) / sum( volume[-1*open_minutes:-1*i] ),2)
        else:
            yellow_line = round(sum( (close*volume)[-1*open_minutes:] ) / sum( volume[-1*open_minutes:] ),2)
            #print "yellow_line:" + str(yellow_line) + ',close:' + str(close[-1]) + ',' + str(close[-1]>=yellow_line)
        
        #yellow_line_array[i] = yellow_line
        #print strong_array[-(i+1)]
        #print close[-(i+1)]
        strong_array[-(i+1)] = close[-(i+1)]>=yellow_line
        
    #print strong_array
    if sum(strong_array)>=count_minute*0.8 and count_minute>=2:
        return True
    else:
        return False

if __name__ == '__main__':
    
    macd_dif = np.array([11,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,1])
    close = np.array([11,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,1])
    print gt_sell(macd_dif,10)
    print gt_sell(macd_dif,5)
    print gt_sell(close,2)
    pass