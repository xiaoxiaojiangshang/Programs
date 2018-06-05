# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#读取'SecuCode', 'TradingDay', 'TurnoverRate', 'ClosePrice', 'ChangePCT', 'TotalMV
import MySQLdb
from  datetime import datetime
import time

def common_multi_insert(cur, tablename, fieldnames, dic_list_al):
    try:
        index_slice_list = range(0, len(dic_list_al), 10000) #gip=10000
        if index_slice_list[-1] < len(dic_list_al) - 1: index_slice_list += [len(dic_list_al)]# 保存最后一位
        for i in range(len(index_slice_list)-1):
            dic_list = dic_list_al[index_slice_list[i]:index_slice_list[i+1]]  #dic_list save 10000个数据
            val_arr=[]
            for dic in dic_list:
                for field in fieldnames:
                    val_arr.append(dic[field])
            one_row_val_sql="("+",".join(["%s"]*len(fieldnames))+")"
            val_sql=",".join([one_row_val_sql]*len(dic_list))
            sql = "replace Into {0}({1})  VALUES{2}".format(tablename, ",".join(fieldnames),val_sql)
            # cur = connection.cursor()
            cur.execute(sql,val_arr)
        return True
    except Exception as ex:
        print ex
        print u'%s 写数据库失败!'%tablename
        return  False
def datetime2days(dt):
    if datetime == type(dt):
        timeArray = time.strptime("%s" % dt.date(), "%Y-%m-%d")  # %H:%M:%S
    else:
        timeArray = time.strptime("%s" % dt, "%Y-%m-%d")
    days = int((time.mktime(timeArray) + 8 * 60 * 60) / 86400)
    return days

def load_zqdm():
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()
    sql_str = "SELECT Innercode,SecuCode FROM secumain WHERE SecuCategory=1"
    cur.execute(sql_str)

    Innercode2SecuCode = {}
    for Innercode,SecuCode in cur.fetchall():
        Innercode2SecuCode[Innercode] = SecuCode
    cur.close()
    conn.close()

    return Innercode2SecuCode

def update_ltsz(Innercode2SecuCode):
    conn239 = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = conn239.cursor()
    sql_str=" Drop table if exists temp"
    cur239.execute(sql_str)
    sql_str = "CREATE TABLE temp(days INT NOT NULL, id INT NOT NULL, ltsz FLOAT NULL,sy_rate FLOAT NULL ,zsz FLOAT NULL PRIMARY KEY ( days,id )); "
    cur239.execute(sql_str)
    cur239.execute("ALTER TABLE `temp` ENGINE = MYISAM ")


    # 往临时表写数据
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()
    sql_str = "SELECT InnerCode,TradingDay,TotalMV,PE,NegotiableMV FROM lc_dindicesforvaluation"
    cur.execute(sql_str)

    data_list = []
    year_list = []
    invalid_InnerCode_set = set()
    for InnerCode, TradingDay, TotalMV in cur.fetchall():
        year_list += [TradingDay.year]
        if InnerCode not in Innercode2SecuCode:
            #print InnerCode
            invalid_InnerCode_set.add(InnerCode)
            continue
        stock_id = int(Innercode2SecuCode[InnerCode])
        data_list += [{'days': datetime2days(TradingDay), 'id': stock_id, 'ltsz':int(TotalMV)}]

    print invalid_InnerCode_set
    common_multi_insert(cur239, "temp", ['days', 'id', 'ltsz'], data_list)


    for year in set(year_list):
        tablename = "select_stock_filter_%d"%year
        sql_str = "update %s,temp set %s.ltsz = temp.ltsz where %s.id = temp.id and %s.days=temp.days"%(tablename, tablename, tablename, tablename)
        cur239.execute(sql_str)
    cur239.close()
    conn239.close()


if __name__ == "__main__":

    Innercode2SecuCode = load_zqdm()

    update_ltsz(Innercode2SecuCode)
