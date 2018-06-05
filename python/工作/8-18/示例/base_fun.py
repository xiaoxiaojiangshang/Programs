# -*- coding: utf-8 -*-
"""
Created on Thu May 12 17:44:50 2016

@author: Administrator
"""
from talib.abstract import *
from talib import func
import talib
import copy
import numpy as np
from datetime import *

def get_dp_market(stock_code):
    if stock_code=='000001':
        return 'SH'
    elif stock_code=='399006' or stock_code=='399005':
        return 'SZ'
    if stock_code[0]=='6':
        return 'SH'
    else:
        return 'SZ'

def get_dp_code(stock_code):
    
    if stock_code[0]=='6':
        return '000001'
    elif stock_code[0]=='3':
        return '399006'
    elif stock_code[0]=='0':
        return '399005'
    elif stock_code[0]=='1':
        return '399006'
    else:
        return ''

def dt1m_2_dt60m(dt):

    date = dt.date()
    tm = dt.time()
    dt_m60 = ""
    if tm>=time(9,30,0) and tm<=time(10,30,0):
        dt_m60 = datetime.combine(date, time(10,30,0))
    elif tm>=time(10,31,0) and tm<=time(11,30,0):
        dt_m60 = datetime.combine(date, time(11,30,0))
    elif tm>=time(13,0,0) and tm<=time(14,0,0):
        dt_m60 = datetime.combine(date, time(14,0,0))
    elif tm>=time(14,1,0) and tm<=time(15,0,0):
        dt_m60 = datetime.combine(date, time(15,0,0))

    return dt_m60

#早盘买入时间
def is_zp_buy_time(dt):

     if (dt.hour==8 and dt.minute>=35) or (dt.hour==9 and dt.minute<=31):
         return 1
     else:	
         return 0


#盘中买入时间
def is_pz_buy_time(dt):

     if (dt.time().hour==9 and dt.time().minute>=32) or (dt.time().hour>=10 and dt.time().hour<=13) or (dt.time().hour==14 and dt.time().minute<=35):
         return 1
     else:
         return 0
	


#尾盘买入时间
def is_wp_buy_time(dt):


    if dt.time().hour==14 and dt.time().minute>=55 and dt.time().minute<=59:
        return 1
    else:
        return 0

def get_pre_close(cur, stock_code):
    
    sql_str = "SELECT datetime,close_ FROM gg_day WHERE code='%s' ORDER BY datetime ASC"%(stock_code)
    #print sql_str

    
    pre_close_dic={} # 头一天的开盘价
    
    cur.execute(sql_str)
    ret_tuple = cur.fetchall()
    if 0==len(ret_tuple):
        return
    index = 0
    for line in ret_tuple:

        if index>=1:
            dt = line[0]
            pre_close_ = float(ret_tuple[index-1][1])
            pre_close_dic[dt.date()] = pre_close_
        
        index = index + 1
        
    return pre_close_dic

# 获取大盘走势指标	
def get_dp_qs_kpzf(cur, dp_code):
    # 开始:大盘趋势 --------------------------------------------------------------
    sql_str = "SELECT datetime,dpzs,kpzf FROM dp_day WHERE code='%s' ORDER BY datetime ASC"%(dp_code)
    #print sql_str

    dp_qs_dic = {}    
    dp_kpzf_dic = {}
    
    cur.execute(sql_str)
    ret_tuple = cur.fetchall()
    if 0==len(ret_tuple):
        #print u"大盘趋势数据，空"
        #logging.info(stock_code + ',' + cur_date.strftime("%Y-%m-%d") + u"大盘趋势数据，空")
        #logging.info(sql_str)
        return
    index = 0
    for line in ret_tuple:

        dt = line[0]        
        dpzs = int(line[1])
        dp_kpzf = float(line[2])
        
        dp_qs_dic[dt.date()] = dpzs
        dp_kpzf_dic[dt.date()] = dp_kpzf
        
        index = index + 1
        
    return dp_qs_dic,dp_kpzf_dic


 
    
#两条线维持一定周期后交叉。
#用法:
#LONGCROSS(A,B,N)表示A在N周期内都小于B，本周期从下方向上穿过B时返回1，否则返回0
#例如：LONGCROSS(MA(CLOSE,5),MA(CLOSE,10),5)表示5日均线维持5周期后与10日均线交金叉    
def LONGCROSS(A,B,N):
    if A.shape[0]<N+1:
        print 'len(A) 必须大于等于 N+1'
        return
    if B.shape[0]<N+1:
        print 'len(B) 必须大于等于 N+1'
        return
    lc = np.ones(A.shape)*np.nan
    for i in range(A.shape[0]-N):
        if sum( A[-1*(N+1+i):-(1+i)]<B[-1*(N+1+i):-(1+i)] )==N and A[-1*(i+1)]>B[-1*(i+1)]:
           lc[-1*(i+1)] = True
        else:
            lc[-1*(i+1)] = False

    return lc
    
    
def Cal_MACD(inputs, short=12, long=26, mid=9):
    #print inputs['close']
    macd_diff=talib.EMA(inputs['close'],short) - talib.EMA(inputs['close'],long)
    if sum(np.isnan(macd_diff))==len(macd_diff):
        macd_dea = macd_diff
        macd_macd = macd_diff
    else:
        macd_dea=talib.EMA(macd_diff, mid)
        macd_macd=2*(macd_diff-macd_dea)
    return macd_diff,macd_dea,macd_macd

def Cal_VMACD(inputs, short=12, long=26, mid=9):
    #print inputs['close']
    macd_diff=talib.EMA(1.0*inputs['volume'],short) - talib.EMA(1.0*inputs['volume'],long)
    if sum(np.isnan(macd_diff))==len(macd_diff):
        macd_dea = macd_diff
        macd_macd = macd_diff
    else:
        macd_dea=talib.EMA(macd_diff,mid)
        macd_macd=2*(macd_diff-macd_dea)
    return macd_diff,macd_dea,macd_macd


def REF(v_data,k):    
    
    result = v_data[[0]*min(k,v_data.shape[0])+range(v_data.shape[0]-k)]
    if result.dtype in ('float16', 'float32', 'float64'):
        result[:k] = np.nan
    else:
        result[:k] = False
    
    return result

def Cal_TKQK_DOWN_ARR(HIGH,LOW):    
    
    u_qk_pos_arr = np.ones(HIGH.shape,dtype=np.int)
    d_qk_pos_arr = np.ones(HIGH.shape,dtype=np.int)
    u_qk_price_arr = np.ones(HIGH.shape,dtype=np.float)
    d_qk_price_arr = np.ones(HIGH.shape,dtype=np.float)
    for i in range(HIGH.shape[0]):        
        sub_high = HIGH[:(i+1)]
        sub_low = LOW[:(i+1)]
        qk_pos1,qk_pos2,qk_price1,qk_price2 = Cal_TKQK_DOWN(sub_high,sub_low)
        u_qk_pos_arr[i] = qk_pos1
        d_qk_pos_arr[i] = qk_pos2
        u_qk_price_arr[i] = qk_price1
        d_qk_price_arr[i] = qk_price2
    return u_qk_pos_arr,d_qk_pos_arr,u_qk_price_arr,d_qk_price_arr

def Cal_TKQK_DOWN(HIGH,LOW):
    """
    计算最近n个向下跳空缺口
    """
    REF_LOW = REF(LOW,1)
    b_is_tkqk = HIGH<REF_LOW
    index_qk_arr = np.where(b_is_tkqk==True)[0]
    qk_price1 = -1
    qk_price2 = -1
    
    qk_pos1 = 1000000
    qk_pos2 = 1000000
    # 循环美俄缺口,看是否有被回补
    for i in range(index_qk_arr.shape[0]-1,-1,-1):
        index_qk = index_qk_arr[i]
        if np.max( HIGH[index_qk:] )<REF_LOW[index_qk]:
            # 找到尚未回补的缺口
            qk_price1 = REF_LOW[index_qk]
            qk_price2 = np.max( HIGH[index_qk:] )#HIGH[index_qk]
            qk_pos1 = index_qk-1
            qk_pos2 = index_qk
            break
    return qk_pos1,qk_pos2,qk_price1,qk_price2
    
def Cal_TKQK_UP_ARR(HIGH,LOW):    
    """
    计算向上跳空缺口
    """
    u_qk_pos_arr = np.ones(HIGH.shape,dtype=np.int)
    d_qk_pos_arr = np.ones(HIGH.shape,dtype=np.int)
    u_qk_price_arr = np.ones(HIGH.shape,dtype=np.float)
    d_qk_price_arr = np.ones(HIGH.shape,dtype=np.float)
    for i in range(HIGH.shape[0]):        
        sub_high = HIGH[:(i+1)]
        sub_low = LOW[:(i+1)]
        qk_pos1,qk_pos2,qk_price1,qk_price2 = Cal_TKQK_UP(sub_high,sub_low)
        u_qk_pos_arr[i] = qk_pos1
        d_qk_pos_arr[i] = qk_pos2
        u_qk_price_arr[i] = qk_price1
        d_qk_price_arr[i] = qk_price2
    return u_qk_pos_arr,d_qk_pos_arr,u_qk_price_arr,d_qk_price_arr

def Cal_TKQK_UP(HIGH,LOW):
    """
    计算最近n个向上跳空缺口
    """
    REF_HIGH = REF(HIGH,1)
    b_is_tkqk = LOW>REF_HIGH
    index_qk_arr = np.where(b_is_tkqk==True)[0]
    qk_price1 = -1
    qk_price2 = -1
    
    qk_pos1 = 1000000
    qk_pos2 = 1000000
    # 循环美俄缺口,看是否有被回补
    for i in range(index_qk_arr.shape[0]-1,-1,-1):
        index_qk = index_qk_arr[i]
        if np.min( LOW[index_qk:] )>REF_HIGH[index_qk]:
            # 找到尚未回补的缺口
            qk_price1 = REF_HIGH[index_qk]
            qk_price2 = np.min( LOW[index_qk:] ) #LOW[index_qk]
            qk_pos1 = index_qk-1
            qk_pos2 = index_qk
            break
    return qk_pos1,qk_pos2,qk_price1,qk_price2

def BARSLAST_ARR(v_data,n=1):
    """    
    """
    pos_inf = np.inf
    s = pos_inf
    #pos_arr = np.array([],dtype=np.int)
    pos_arr = np.ones(v_data.shape,dtype=np.int) * pos_inf
    for index in range(v_data.shape[0]):
        v = v_data[index]
        if v:
            s = 0
        else:
            s += 1
        pos_arr[index] = s
        
    #print pos_arr
    n_pos_arr = copy.deepcopy(pos_arr)
    for i in range(n-1):
        for index in range(n_pos_arr.shape[0]):
            if n_pos_arr[index]==pos_inf:
                n_pos_arr[index] = pos_inf
            else:
                #print int(index - n_pos_arr[index] - 1)
                n_pos_arr[index] += pos_arr[int(index - n_pos_arr[index] - 1)] + 1
    
    n_pos_arr[n_pos_arr==np.inf] = (2 ** 16 - 1) / 2
    n_pos_arr = np.int16(n_pos_arr)
    return n_pos_arr
    
def BARSLAST(v_data,n=1):
    """
    上一次条件成立到当前的周期数。若上一次条件成立不存在，则返回无效值
    用法:
    BARSLAST(X):上一次X不为0到现在的天数
    例如：BARSLAST(CLOSE/REF(CLOSE,1)>=1.1)表示上一个涨停板到当前的周期数
    如果没有符合条件的周期，函数将返回np.inf
    """    
    index_v = np.array( range(len(v_data)) )
    
    temp_v = v_data != 0
    
    if sum(temp_v*1.0)==0:
        return np.inf
        
    if index_v[v_data != 0].shape[0]<n:
        return np.inf
    else:
        pos = len(v_data) - index_v[v_data != 0][-1*n] - 1
    return pos    


def SD_HHV(v_data, NN=10000000):
    c_len = v_data.shape[0]
    result = np.ones(c_len) * np.nan
    
    for i in range(c_len):
        # 倒数第i个
    
        NN_ = max(0,c_len-i-NN)# 从第i个往前推NN个
    
        if 0==i:
            result[-1*(i+1)] = max(v_data[NN_:])
        else:            
            result[-1*(i+1)] = max(v_data[NN_:-1*i])
    return result

def SD_LLV(v_data, NN=10000000):
    c_len = v_data.shape[0]
    result = np.ones(c_len) * np.nan
    
    for i in range(c_len):
        # 倒数第i个
        NN_ = max(0,c_len-i-NN)# 从第i个往前推NN个
        if 0==i:
            result[-1*(i+1)] = min(v_data[NN_:])
        else:            
            result[-1*(i+1)] = min(v_data[NN_:-1*i])
    return result

def SD_MAX(_v_data1, _v_data2):

    if np.isscalar(_v_data1) and np.isscalar(_v_data2):
        return max(_v_data1,_v_data2)
        
    if np.isscalar(_v_data1):
        v_data1 = np.ones(_v_data2.shape) * _v_data1
    else:
        v_data1 = _v_data1
    if np.isscalar(_v_data2):
        v_data2 = np.ones(_v_data1.shape) * _v_data2
    else:
        v_data2 = _v_data2 
        
    if v_data1.shape[0] != v_data2.shape[0]:
        print np.array([])
    
    c_len = len(v_data1)
    result = np.ones(c_len) * np.nan
    for i in range(len(v_data1)):
        result[i] = max(v_data1[i], v_data2[i])
    
    return result

def SD_MIN(_v_data1, _v_data2):
    
    if np.isscalar(_v_data1) and np.isscalar(_v_data2):
        return max(_v_data1,_v_data2)
        
    if np.isscalar(_v_data1):
        v_data1 = np.ones(_v_data2.shape) * _v_data1
    else:
        v_data1 = _v_data1
    if np.isscalar(_v_data2):
        v_data2 = np.ones(_v_data1.shape) * _v_data2
    else:
        v_data2 = _v_data2 
        
    if v_data1.shape[0] != v_data2.shape[0]:
        print np.array([])
    
    c_len = len(v_data1)
    result = np.ones(c_len) * np.nan
    for i in range(len(v_data1)):
        result[i] = min(v_data1[i], v_data2[i])
    
#    if len(v_data1)!=len(v_data2):
#        print np.array([])
#    
#    c_len = len(v_data1)
#    result = np.ones(c_len) * np.nan
#    for i in range(len(v_data1)):
#        result[i] = min(v_data1[i], v_data2[i])
    
    return result


def __SD_AVEDEV(v_data, N, k):
    if 0==k:
        c_array = v_data[-1*N:]
    else:
        c_array = v_data[-1*N-k:-1*k]
    c_len = c_array.shape[0]
    c_sum = c_array.sum()
    avg = c_sum / c_len
    
    sum_v = 0
    for i in range(c_len):
        sum_v = sum_v + abs(c_array[i] - avg)
    return sum_v/c_len

def SD_AVEDEV(v_data, N):
       
    result = np.ones(v_data.shape) * np.nan
    v_len = v_data.shape[0]
    for i in range(N-1,v_len,1):
        result[i] = __SD_AVEDEV(v_data, N, v_len-i-1)
    return result
    
def SD_SMA(v_data, N, M):
    c_array = v_data #inputs['close']
    c_len = c_array.shape[0]
    result = np.zeros(c_array.shape)
    
    istart=0
    y = np.nan
    for i in range(0,c_len,1):
        result[i]=c_array[i]
        if False==np.isnan(c_array[i]):
            istart = i
            y = c_array[i]            
            break
    result[istart]=y
    
    for i in range(istart+1,c_len,1):
        x = c_array[i]
        if np.isnan(x):
            y = np.nan
        else:            
            y = (x*M + y*(N-M)) / N
        result[i]=y    
    return result

def SD_EXPMEMA(v_data, N):
    
    if sum(np.isnan(v_data))==len(v_data):
        return np.zeros(v_data.shape) * np.nan
    else:
        return talib.EMA(v_data, N)

def Cal_KDJ(inputs,N1=9,N2=3,N3=3):
    RSV = ( inputs['close'] - talib.MIN(inputs['low'], N1) ) / (talib.MAX(inputs['high'], N1) - talib.MIN(inputs['low'], N1)) * 100
    kdj_k=SD_SMA(RSV, N2, 1)
    kdj_d=SD_SMA(kdj_k, N3, 1)
    kdj_j=3*kdj_k-2*kdj_d
    return kdj_k,kdj_d,kdj_j
    
def Cal_RSI(inputs,N1=6,N2=12,N3=24):
    """
    LC:=REF(CLOSE,1);
    RSI1:SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100;
    RSI2:SMA(MAX(CLOSE-LC,0),N2,1)/SMA(ABS(CLOSE-LC),N2,1)*100;
    RSI3:SMA(MAX(CLOSE-LC,0),N3,1)/SMA(ABS(CLOSE-LC),N3,1)*100;
    """  
    close = inputs['close']
    lc = REF(close,1)    
    rsi1=SD_SMA(np.max([close-lc,np.zeros(lc.shape)],0),N1,1) / SD_SMA(np.abs(close-lc),N1,1) * 100
    rsi2=SD_SMA(np.max([close-lc,np.zeros(lc.shape)],0),N2,1) / SD_SMA(np.abs(close-lc),N2,1) * 100
    #rsi3=SD_SMA(np.max([close-lc,np.zeros(lc.shape)],0),N3,1) / SD_SMA(np.abs(close-lc),N3,1) * 100
    
    return rsi1,rsi2

def Cal_CCI(inputs,N=14):
    #TYP := (HIGH + LOW + CLOSE)/3;
    #CCI_CCI:=(TYP-MA(TYP,14))/(0.015*AVEDEV(TYP,14));
    typ = (inputs['high'] + inputs['low'] + inputs['close'])/3
    cci = (typ - talib.SMA(typ,14)) / ( 0.015*SD_AVEDEV(typ, N) )
    
    return cci
def Cal_SKDJ(inputs):
    #LOWV:=LLV(LOW,N);
    #HIGHV:=HHV(HIGH,N);
    #RSV:=EMA((CLOSE-LOWV)/(HIGHV-LOWV)*100,M);
    #K:EMA(RSV,M);
    #D:MA(K,M);    
    N = 9
    M = 3
    lowv = talib.MIN(inputs['low'], N)
    highv = talib.MAX(inputs['high'], N)
    rsv = talib.EMA( (inputs['close']-lowv) / (highv-lowv) * 100, M )
    skdj_k = talib.EMA(rsv, M)
    skdj_d = talib.SMA(skdj_k, M)        
    return skdj_k, skdj_d

def Cal_DMI(inputs, N=14, MM=6):
    """ 尚未测试
MTR:=EXPMEMA(MAX(MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1))),ABS(REF(CLOSE,1)-LOW)),N);
HD :=HIGH-REF(HIGH,1);
LD :=REF(LOW,1)-LOW;
DMP:=EXPMEMA(IF(HD>0&&HD>LD,HD,0),N);
DMM:=EXPMEMA(IF(LD>0&&LD>HD,LD,0),N);
PDI: DMP*100/MTR;
MDI: DMM*100/MTR;
ADX: EXPMEMA(ABS(MDI-PDI)/(MDI+PDI)*100,MM);
ADXR:EXPMEMA(ADX,MM);
    """
    HIGH = inputs['high']
    LOW = inputs['low']
    CLOSE = inputs['close']
    MTR=SD_EXPMEMA(SD_MAX(SD_MAX(HIGH-LOW,abs(HIGH-REF(CLOSE,1))),abs(REF(CLOSE,1)-LOW)),N)
    
    HD =HIGH-REF(HIGH,1)
    LD =REF(LOW,1)-LOW
    
    #DMP=EXPMEMA(IF(HD>0&&HD>LD,HD,0),N);
    DMP=SD_EXPMEMA( ( (HD>0)*(HD>LD) )*HD,N )
    #DMM=EXPMEMA(IF(LD>0&&LD>HD,LD,0),N);
    DMM=SD_EXPMEMA( ( (LD>0)*(LD>HD) )*LD,N )
    PDI=DMP*100.0/MTR
    MDI=DMM*100.0/MTR
    
    ADX=SD_EXPMEMA(abs(MDI-PDI)/(MDI+PDI)*100.0,MM)
    ADXR=SD_EXPMEMA(ADX,MM)
    
    return PDI,MDI,ADX,ADXR
    
def Cal_ENE(inputs, N=10,M1=10,M2=10):
    """    
    UPPER:=(1+M1/100)*MA(CLOSE,N);
    LOWER:=(1-M2/100)*MA(CLOSE,N);
    ENE:=(UPPER+LOWER)/2;
    CROSS(C,LOWER);    
    """
    CLOSE = inputs['close']
    UPPER=(1+M1/100.0)*talib.SMA(CLOSE,N)
    LOWER=(1-M2/100.0)*talib.SMA(CLOSE,N)
    ENE=(UPPER+LOWER)/2.0
    return UPPER,ENE,LOWER
    
def Cal_BIAS(inputs,N1=6,N2=12,N3=24):
    """
    BIAS1 :(CLOSE-MA(CLOSE,N1))/MA(CLOSE,N1)*100;
    BIAS2 :(CLOSE-MA(CLOSE,N2))/MA(CLOSE,N2)*100;
    BIAS3 :(CLOSE-MA(CLOSE,N3))/MA(CLOSE,N3)*100;
    """
    CLOSE = inputs['close']
    BIAS1 = (CLOSE-talib.SMA(CLOSE,N1))/talib.SMA(CLOSE,N1)*100
    BIAS2 = (CLOSE-talib.SMA(CLOSE,N2))/talib.SMA(CLOSE,N2)*100
    BIAS3 = (CLOSE-talib.SMA(CLOSE,N3))/talib.SMA(CLOSE,N3)*100
    return BIAS1,BIAS2,BIAS3

def Cal_VR(inputs,N=26, M=6):
    """
    TH:=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N);
    TL:=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N);
    TQ:=SUM(IF(CLOSE=REF(CLOSE,1),VOL,0),N);
    VR:100*(TH*2+TQ)/(TL*2+TQ);
    MAVR:MA(VR,M);
    """
    CLOSE = inputs['close']
    CLOSE_REF_1 = REF(CLOSE,1)
    VOL = inputs['volume']    
    TH = talib.SUM( ( CLOSE>CLOSE_REF_1 ) * VOL, N)
    TL = talib.SUM( ( CLOSE<CLOSE_REF_1 ) * VOL, N)
    TQ = talib.SUM( ( CLOSE==CLOSE_REF_1 ) * VOL, N)
    VR = 100*(TH*2+TQ)/(TL*2+TQ)
    if sum(np.isnan(VR))==len(VR):
        MAVR=np.zeros(VR.shape) * np.nan
    else:
        MAVR=talib.SMA(VR, M)
    return VR,MAVR

def Cal_PSY(inputs,N=12,M=6):
    """
    PSY:COUNT(CLOSE>REF(CLOSE,1),N)/N*100;
    PSYMA:MA(PSY,M);
    """
    CLOSE = inputs['close']    
    NN = min(len(CLOSE),N)
    #PSY = sum((CLOSE>REF(CLOSE,1))[-1*NN:]) / NN * 100.0
    if NN<2:
        PSY = np.array([0.0])
    else:
        PSY = talib.SUM( 1.0*(CLOSE>REF(CLOSE,1)), NN) / NN * 100.0
    return PSY
#def Cal_OVB(inputs):
#    """
#    VA:=IF(CLOSE>REF(CLOSE,1),VOL,-VOL);
#    OBV:SUM(IF(CLOSE=REF(CLOSE,1),0,VA),0);
#    MAOBV:MA(OBV,M);
#    """
#    CLOSE = inputs['close']
#    VOL = inputs['volume']
#    VA = np.zeros(CLOSE.shape)
#    t_v2 = CLOSE>REF(CLOSE,1)
#    t_index = np.where(t_v2==True)[0]
#    VA[t_index] = VOL[t_index]
#    t_index = np.where(t_v2==False)[0]
#    VA[t_index] = -1*VOL[t_index]
#    
#    OBV = np.zeros(CLOSE.shape)
    

def Cal_ARBR(inputs,N=26):
    """
    BR:=SUM(MAX(0,HIGH-REF(CLOSE,1)),N)/SUM(MAX(0,REF(CLOSE,1)-LOW),N)*100;
    AR:=SUM(HIGH-OPEN,N)/SUM(OPEN-LOW,N)*100;
    BR〈40 OR AR<40;
    """
    OPEN = inputs['open']
    CLOSE = inputs['close']
    HIGH = inputs['high']    
    LOW = inputs['low']
    CLOSE_REF_1 = REF(CLOSE,1)
    t1 = HIGH-CLOSE_REF_1
    t1[t1<0] = 0
    t2 = CLOSE_REF_1-LOW
    t2[t2<0] = 0
    BR = talib.SUM(t1,N)/talib.SUM(t2,N)*100.0
    AR = talib.SUM(HIGH-OPEN,N) / talib.SUM(OPEN-LOW,N) * 100.0
    #ARBR = (BR<40) * (AR<40)
    return AR,BR

def Cal_MTM(inputs,N=12,M=6):
    
    CLOSE = inputs['close']
    MTM=CLOSE-REF(CLOSE,N)
    
    if sum(np.isnan(MTM))==len(MTM):
        MTMMA=np.zeros(MTM.shape) * np.nan
    else:
        MTMMA=talib.SMA(MTM,M)
    return MTM,MTMMA
    
# 计算N日的均量
def Cal_AVG_VOL(inputs, N=5,CYC=5):
   """
   计算N日平均成交量,CYC用于判断属于哪个周期
   """
   dt_list=inputs['datetime']
   VOL = inputs['volume']
   avg_vol = 0.0
   # 判断是多少周期
   if CYC==5:
       # 当前数据为日周期
       clen = min(len(VOL), N)
       avg_vol = sum(VOL[-1*clen:]) / clen / 240.0
      
   return avg_vol


# a从下方上穿b，返回1，否则返回0
def cross_arr(v_a,v_b):
    
#    if np.isscalar(v_a):
#        v_a_ = np.array([v_a,v_a])
#    else:
#        v_a_ = v_a
#    if np.isscalar(v_b):       
#        v_b_ = np.array([v_b,v_b])
#    else:
#        v_b_ = v_b
#
#    if len(v_a_)<2 or len(v_b_)<2:
#        return np.array([False])
#    else:  
#        return ( REF(v_a_,1) < REF(v_b_,1) ) & ( v_a_ > v_b_ )
        
    ref_a = v_a if np.isscalar(v_a) else REF(v_a,1)
    ref_b = v_b if np.isscalar(v_b) else REF(v_b,1)
    return (v_a>v_b) & (ref_a<ref_b)

def CROSS_ARR(v_a,v_b):
    return cross_arr(v_a,v_b)    
    
# a从下方上穿b，返回1，否则返回0
def cross(v_a,v_b):
    if np.isscalar(v_a):
        v_a_ = np.array([v_a,v_a])
    else:
        v_a_ = v_a
    if np.isscalar(v_b):       
        v_b_ = np.array([v_b,v_b])
    else:
        v_b_ = v_b

    if len(v_a_)<2 or len(v_b_)<2:
        return False
    else:    
        return v_a_[-2] < v_b_[-2] and v_a_[-1] > v_b_[-1]    
 
def CROSS(v_a,v_b):
    return cross(v_a,v_b)

# 计算平台压力
def Cal_PTYL(c_arr,h_arr,dt_list, cyc, n_kbar=500, n_kxsl=3):
    
    MA60 = talib.SMA(c_arr,cyc)
    b_dyma60_arr = c_arr>=MA60 # 是否大于60日线
    pos1 = np.inf
    
    pos_list = []
    
    for i in range(1,min(n_kbar,b_dyma60_arr.shape[0])+1,1):
        
        if b_dyma60_arr[-1*i]==True and pos1 == np.inf:
            # 第一个大于ma60的位置
            pos1 = -1*i
        elif b_dyma60_arr[-1*i]==False and pos1 != np.inf:# 
            pos2 = -1*(i-1)
            if np.abs(pos1-pos2)>n_kxsl or pos1==-1:                
                pos_list.append((pos1,pos2))
            pos1 = np.inf
    
    # 找头部
    tou_value_list = []    
    
    for (pos1,pos2) in pos_list:
#        print '----------------'
#        print datas['datetime'][pos1]
#        print datas['datetime'][pos2]
#        print 'pos1:' + str(pos1)
#        print 'pos2:' + str(pos2)
#        print '----------------'
        if pos1==-1:
            pos2 = len(c_arr)-abs(pos2)
            pos1 = len(c_arr)-1
        #print 'pos1:' + str(pos1)
        #print 'pos2:' + str(pos2)
        max_h = max(h_arr[pos2:pos1+1])
        #index = h_arr[pos2:pos1+1].index(max_h)
        index_arr = np.where(h_arr[pos2:pos1+1]==max_h)
        index = index_arr[0][0]
        t_value = ( max_h + c_arr[pos2:pos1+1][index] ) / 2.0
        dt = dt_list[pos2:pos1+1][index]
        tou_value_list.append((t_value,dt,dt_list[pos2],dt_list[pos1],abs(pos1-pos2)+1))
    
    return tou_value_list

if __name__ == '__main__':
    
    
    a=np.array([False,False,False,True,False,False,False,True,False,True,False])    
    print a
    print BARSLAST_ARR(a,1)
    print BARSLAST_ARR(a,2)
    print BARSLAST_ARR(a,3)
    print BARSLAST_ARR(a,4)
    #DMP=SD_EXPMEMA( ( (a>0)*(a>b) )*a,2 )
    #DMP=SD_EXPMEMA(a,2)
    
    #cc = talib.EMA(a, 1)
    
    
    
    
    