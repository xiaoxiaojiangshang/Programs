# -*- coding: utf-8 -*-
import MySQLdb
from Date_list import Date_list
from secu_dict import Secu_list   #get
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
            cur.execute(sql,val_arr)
        return True
    except Exception as ex:
        print ex
        print u'%s 写数据库失败!'%tablename
        return  False

def update(cur,att,dict):
    sql_str=" Drop table if exists temp"
    cur.execute(sql_str)
    sql_str = "CREATE TABLE temp(days INT NOT NULL, id INT NOT NULL, %s FLOAT NULL,PRIMARY KEY ( days,id )) "%(att)
    cur.execute(sql_str)
    cur.execute("ALTER TABLE `temp` ENGINE = MYISAM ")
    common_multi_insert(cur239, "temp", ['days', 'id', att], dict)
    for year in range(1990,2018,1):
        tablename = "select_stock_filter_%d"%year
        sql_str = "UPDATE %s,temp SET %s.%s = temp.%s WHERE %s.id = temp.id and %s.days=temp.days"%(tablename, tablename,att,att, tablename, tablename)
        cur239.execute(sql_str)


def beyond_year(day1,day2,id,att):
    if day2-day1>=365:
        print "it beyond one year,day1=%d,day2=%d,diff=%d,id=%d,att=%s"%(day1,day2,day2-day1,id,att)

def return_index(day,id):
    if day in date_list:
        return date_list.index(day)
    else:
        try:
            for day_temp in date_list:
                index_temp=date_list.index(day_temp)
                if date_list[index_temp]<day and date_list[index_temp+1]>day:
                    return index_temp
        except:
            print day,id

def deal_sql(list_att):
    for key in list_att:
        print key,time.clock()-start
        dict_list_all=[]
        for secu_id in secu_list:
            dict_221={}
            list_update=[]
            sql_name="hs_finance"
            sql_str = ("SELECT id,update_day,%s  FROM %s WHERE id =%d and %s IS NOT NULL ORDER BY id ASC,update_day ASC,tid DESC,data_type DESC"%(key,sql_name,secu_id,key))
            cur239.execute(sql_str)
            for id,update_day,value in cur239.fetchall():
                if (id,update_day) not in dict_221:
                    dict_221[(id,update_day)]=value
                    list_update.append(update_day)
            for key_2 in dict_221:
                index=list_update.index(key_2[1])
                if index==len(list_update)-1:
                    day_start=key_2[1]
                    year = 2017  # last year
                    day_end=y2m[year][1]
                    Add_list(dict_list_all, day_start,day_end,secu_id,key,dict_221[key_2])
                else:
                    day_start=min(list_update[index],y2m[2017][1]-1)
                    day_end=min(list_update[index+1],y2m[2017][1])#  get min,else beyond
                    # beyond_year(day_start,day_end,secu_id,key)
                    Add_list(dict_list_all,day_start,day_end,secu_id,key,dict_221[key_2])
        update(cur239,key,dict_list_all)

def Add_list(dict_list_all,day_start,day_end,id_value,name,value):
    if day_start<y2m[2017][1]:     #17378=2017-7-31 end_date
        index1=return_index(day_start,id_value)+1
        index2=return_index(day_end,id_value)
        for days in date_list[index1:index2 + 1]:
            one_dict={'days':days,'id':id_value,name:value}
            dict_list_all+=[one_dict]
            # if day_start>=13626 and day_end<=14043:

if __name__ == "__main__":
    start=time.clock()
    cnn = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = cnn.cursor()
    list_att = ['ystb_rate','jzcsy_rate','jzcfz_rate','mgwfplr','mgzbgj','mgxjllje']
    secu_list = Secu_list()
    date_list, y2m = Date_list()
    deal_sql(list_att)
    cnn.close()
    cur239.close()

