# -*- coding: utf-8 -*-
import MySQLdb
import numpy as np
from datetime import datetime

def get_id_2_name():   ## id:name
    stock2NameDic = {}
    conn = MySQLdb.connect(host='192.168.1.200', user='root', passwd='nb2008xl', db='db_stock', charset='utf8')
    cur = conn.cursor()

    # cur.execute('SELECT id,name FROM web_stock.sector')
    # ret_tuple = cur.fetchall()
    # for line in ret_tuple:
    #     block = int(line[0])
    #     blockID2nameDic[block] = line[1]
    sql_str = 'SELECT id,name FROM web_stock.stock'
    cur.execute(sql_str)
    ret_tuple = cur.fetchall()
    for line in ret_tuple:
        stock2NameDic[(str(line[0])).zfill(6)] = line[1]
    cur.close()
    conn.close()
    return stock2NameDic

def init_one_stock_data(stock_code, max_num=250):
    all_datas = {}
    conn = MySQLdb.connect(host='192.168.1.250', user='root', passwd='nb2008xl', db='db_fp_data_new', charset='utf8')
    cur = conn.cursor()
    last = None

    # cur.execute("SELECT DISTINCT datetime FROM gg_day WHERE code='%s' ORDER BY datetime DESC LIMIT %d,1"%(stock_code,max_num))
    sql_str = "SELECT code,datetime,pt_price FROM gg_pt WHERE code='%s' ORDER BY datetime DESC LIMIT 0,%d" % ( stock_code, max_num)
    cur.execute(sql_str)
    pt_price_dic = {}
    pt_price_dic2 = {}
    for code, dt, ptyl in cur.fetchall():
        pt_price_dic[(code, dt)] = ptyl
        pt_price_dic2[code] = (np.hstack((np.array([dt]), pt_price_dic2.get(code, (np.array([]), np.array([])))[0])),
                               np.hstack((np.array(ptyl), pt_price_dic2.get(code, (np.array([]), np.array([])))[1])))

    # 提取最近250个交易日的起始日期
    # 提取所有数据
    sql_str = "SELECT code,datetime,open_,high_,low_,close_,volum,zf,liangbi,hsl,ltsz FROM gg_day WHERE code='%s' ORDER BY datetime DESC LIMIT 0,%d" % (
    stock_code, max_num)
    cur.execute(sql_str)
    for code, dt, open_, high_, low_, close_, volume, zf, lb, hsl, ltsz in cur.fetchall():
        if code != last:
            if last:
                all_datas[last] = {'datetime': datas['datetime'], 'open': np.array(datas['open']),
                                   'high': np.array(datas['high']), 'low': np.array(datas['low']),
                                   'close': np.array(datas['close']), 'volume': np.array(datas['volume']),
                                   'zf': np.array(datas['zf']), 'lb': np.array(datas['lb']),
                                   'hsl': np.array(datas['hsl']), 'ltsz': np.array(datas['ltsz']),
                                   'ptyl': np.array(datas['ptyl'])}
            datas = {'datetime': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'zf': [], 'lb': [],
                     'hsl': [], 'ltsz': [], 'ptyl': []}
            last = code
        datas['datetime'] = np.hstack((np.array([dt]), datas['datetime']))
        datas['open'] = np.hstack((np.array([open_]), datas['open']))
        datas['high'] = np.hstack((np.array([high_]), datas['high']))
        datas['low'] = np.hstack((np.array([low_]), datas['low']))
        datas['close'] = np.hstack((np.array([close_]), datas['close']))
        datas['volume'] = np.hstack((np.array([volume]), datas['volume']))
        datas['zf'] = np.hstack((np.array([zf]), datas['zf']))
        datas['lb'] = np.hstack((np.array([lb]), datas['lb']))
        datas['hsl'] = np.hstack((np.array([hsl]), datas['hsl']))
        datas['ltsz'] = np.hstack((np.array([ltsz]), datas['ltsz']))

        if pt_price_dic.has_key((code, dt)):
            ptyl = pt_price_dic[(code, dt)]
        else:
            dt_arr = pt_price_dic2.get(code, (np.array([]), np.array([])))[0]
            ptyl_arr = pt_price_dic2.get(code, (np.array([]), np.array([])))[1]
            index_where_arr = np.where(dt_arr <= dt)[0]
            if index_where_arr.shape[0] > 0:
                ptyl = ptyl_arr[index_where_arr[-1]]
            else:
                ptyl = -1

        datas['ptyl'] = np.hstack((np.array([ptyl]), datas['ptyl']))

    if last:
        all_datas[last] = {'datetime': datas['datetime'], 'open': np.array(datas['open']),
                           'high': np.array(datas['high']), 'low': np.array(datas['low']),
                           'close': np.array(datas['close']), 'volume': np.array(datas['volume']),
                           'zf': np.array(datas['zf']), 'lb': np.array(datas['lb']), 'hsl': np.array(datas['hsl']),
                           'ltsz': np.array(datas['ltsz']), 'ptyl': np.array(datas['ptyl'])}
    cur.close()
    conn.close()
    return all_datas


def init_dp_data_mn(tablename,start_date, end_date = datetime(3000,12,31,0,0,0).date()):
    """
    非日线级别的大盘数据提取
    """
    all_datas = {}
    conn = MySQLdb.connect(host = '192.168.1.250', user = 'root', passwd = 'nb2008xl', db = 'db_fp_data_new', charset = 'utf8')
    cur = conn.cursor()
    last = None
    # # 提取最近250个交易日的起始日期
    # cur.execute("SELECT DISTINCT datetime FROM %s ORDER BY datetime DESC LIMIT %d,1"%(tablename,max_num))
    # 提取所有数据 cur.fetchone()
    sql_str = "SELECT code,datetime,open_,high_,low_,close_,volum FROM %s WHERE datetime>'%s' AND datetime<'%s' ORDER BY code ASC, datetime ASC"%(tablename,start_date,end_date)
    #print sql_str
    cur.execute(sql_str)
    for (code,dt,open_,high_,low_,close_,volume) in cur.fetchall():
        if code!=last:
            if last:
                all_datas[last] = {'datetime':datas['datetime'], 'open':np.array(datas['open']), 'high':np.array(datas['high']), 'low':np.array(datas['low']), 'close':np.array(datas['close']), 'volume':np.array(datas['volume'])}
            datas = {'datetime':[], 'open':[], 'high':[], 'low':[], 'close':[], 'volume':[]}
            last = code
        datas['datetime'].append(dt)
        datas['open'].append(open_)
        datas['high'].append(high_)
        datas['low'].append(low_)
        datas['close'].append(close_)
        datas['volume'].append(volume)
        # datas['zf'].append(zf)

    if last:
        all_datas[last] = {'datetime':datas['datetime'], 'open':np.array(datas['open']), 'high':np.array(datas['high']), 'low':np.array(datas['low']), 'close':np.array(datas['close']), 'volume':np.array(datas['volume'])}
    cur.close()
    conn.close()
    return all_datas