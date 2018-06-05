# -*- coding: utf-8 -*-
import MySQLdb
from Date_list import Date_list
from secu_dict import Secu_list   #get
import time
# import sys
# sys.path.append("../profile")

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
        cur239.execute("UPDATE %s,temp SET %s.%s = temp.%s WHERE %s.id = temp.id and %s.days=temp.days"%(tablename, tablename,att,att, tablename, tablename))

def beyond_year(day1,day2,id,att):
    if day2-day1>=365:
        print "it beyond one year,day1=%d,day2=%d,diff=%d,id=%d,att=%s"%(day1,day2,day2-day1,id,att)

def return_index(day):
    for index,day_temp in enumerate(date_list):
        if day_temp<day:
            continue
        elif day_temp==day:
            return index
        else:
            return index-1
# @sd_profile('a.prof')
def deal_sql(list_att):
    dict_all_zgb={}
    for key in list_att:
        print "key=%s"%(key),time.clock()-start
        sql_name = "hs_finance"
        cur239.execute("SELECT id,update_day,%s  FROM %s WHERE %s IS NOT NULL  ORDER BY id ASC,update_day ASC,tid DESC,data_type DESC" % (key, sql_name, key))
        dict_list_all=[]    #list is composed of dict
        dict_221={}    #(id+update):value
        dict_121={}   #id:update_list
        for id, update_day, value in cur239.fetchall():
            if (id, update_day) not in dict_221:
                dict_221[(id, update_day)] = value
                if id in dict_121:
                    dict_121[id].append(update_day)
                else:
                    dict_121[id] = [update_day]
        for secu_id in secu_list:
            if secu_id in dict_121:            #有的股票某个属性全都为空
                list_update =dict_121[secu_id]
                list_update=sorted(list_update)
                for index,up_day in enumerate(list_update):
                    if index==len(list_update)-1:
                        day_start=up_day
                        year = 2017  # last year
                        day_end=y2m[year][1]
                        Add_list(dict_list_all, day_start,day_end,secu_id,key,dict_221[(secu_id,up_day)],dict_all_zgb)
                    else:
                        day_start=min(list_update[index],y2m[2017][1]-1)
                        day_end=min(list_update[index+1],y2m[2017][1])#  get min,else beyond
                        # beyond_year(day_start,day_end,secu_id,key)
                        Add_list(dict_list_all,day_start,day_end,secu_id,key,dict_221[(secu_id,up_day)],dict_all_zgb)
        update(cur239,key,dict_list_all)

def Add_list(dict_list_all,day_start,day_end,id_value,name,value,dict_all_zgb):
    if day_start<y2m[2017][1]:    #17378=2017-7-31 end_date
        index1=return_index(day_start)+1
        index2=return_index(day_end)
        if name[0] != 'm'or (id_value,date_list[index2]) not in dict_all_zgb:  # repsent mg and zgb is NULL
            for days in date_list[index1:index2 + 1]:
                one_dict={'days':days,'id':id_value,name:value}
                dict_list_all+=[one_dict]
                if name=='zgb':
                    dict_all_zgb[(id_value,days)]=value
        else:
            for days in date_list[index1:index2 + 1]:
                if (id_value,days) not in dict_all_zgb:   #start is NULL ,filter
                    one_dict = {'days': days, 'id': id_value, name: value}
                    dict_list_all += [one_dict]
                    # print "it is littel:",id_value,days
                else:
                    start_zgb=dict_all_zgb[(id_value,days)]
                    end_zgb = dict_all_zgb[(id_value,date_list[index2])]
                    if start_zgb==end_zgb:     #same ,don't need update
                            one_dict = {'days': days, 'id': id_value, name: value}
                            dict_list_all += [one_dict]
                    else:
                        value_temp=value
                        index1=date_list.index(days)
                        for days in date_list[index1:index2 + 1]:
                            days_zgb=dict_all_zgb[(id_value,days)]
                                # if days>13879 and days<14244 and name=='mgwfplr':
                                #     print days,value_temp,start_zgb,days_zgb
                            if start_zgb!=days_zgb and days_zgb is not None:
                                value_temp=value*days_zgb/start_zgb
                                start_zgb=days_zgb
                            one_dict = {'days': days, 'id': id_value, name: value_temp}
                            dict_list_all += [one_dict]
                        break
if __name__ == "__main__":
    start = time.clock()
    cnn = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = cnn.cursor()
    list_att = ['zgb','ltg', 'yg_rate', 'mgsy', 'mgjzc', 'jlr', 'jlrtb_rate', 'ystb_rate', 'jzcsy_rate', 'jzcfz_rate', 'mgwfplr', 'mgzbgj', 'mgxjllje']
    for year in range(1990,2018,1):     # Set NULL about spent 30 sec
        one_row_val_sql =",".join(["%s=NULL"] * len(list_att))
        expression=one_row_val_sql%('ltg','zgb','yg_rate','mgsy','mgjzc','jlr','jlrtb_rate','ystb_rate','jzcsy_rate','jzcfz_rate','mgwfplr','mgzbgj','mgxjllje')
        tablename = "select_stock_filter_%d"%year
        sql_str="UPDATE %s SET %s "%(tablename,expression)
        cur239.execute(sql_str)
    secu_list = Secu_list()
    # secu_list=secu_list[:50]
    date_list, y2m = Date_list()
    deal_sql(list_att)
    cnn.close()
    cur239.close()
    print time.clock()-start
