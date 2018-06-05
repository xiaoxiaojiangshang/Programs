import MySQLdb
from Date_list import Date_list
from secu_dict import Secu_list   #get
import time

def return_year(day1,day2):
    for year in range(1990,2018,1):
        if day1>=y2m[year][0] and day1<=y2m[year][1]:
            if day2<=y2m[year][1] or year==2017:  # last year ,don't need +1 else return keyerror
                return year,True
            else:
                return year,False
        elif day1<y2m[year+1][0]:
            return year+1,True   # lastday+1
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
    for secu_id in secu_list:
        print secu_id,time.clock()-start
        for key in list_att:
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
                    write_sql(year, day_start,day_end,secu_id,key,dict_221[key_2])
                else:
                    year,flag=return_year(list_update[index],list_update[index+1])
                    if flag==True:
                        day_start=list_update[index]
                        day_end=min(list_update[index+1],y2m[year][1])#  get min,else beyond
                        write_sql(year,day_start,day_end,secu_id,key,dict_221[key_2])
                    else:
                        day_start = list_update[index]
                        day_end =y2m[year][1]
                        write_sql(year, day_start, day_end,secu_id,key,dict_221[key_2])
                        day_start =y2m[year+1][0]-1  # from first day
                        day_end = min(list_update[index+1],y2m[year+1][1])#  get min,else beyond
                        write_sql(year+1, day_start, day_end,secu_id,key,dict_221[key_2])

def write_sql(year,day_start,day_end,id_value,name,value):
    if day_start<y2m[2017][1]:     #17378=2017-7-31 end_date
        sql_name="select_stock_filter_%d"%(year)
        index1=return_index(day_start,id_value)+1
        index2=return_index(day_end,id_value)
        if type(value)=='float':
            for day in date_list[index1:index2+1]:
                sql_str=("UPDATE %s SET %s=%f WHERE id=%d and days=%d "% (sql_name,name,value,id_value,day))
                cur239.execute(sql_str)
        else:
            for day in date_list[index1:index2+1]:
                sql_str=("UPDATE %s SET %s=%s WHERE id=%d and days=%d "% (sql_name,name,value,id_value,day))
                cur239.execute(sql_str)
if __name__ == "__main__":
    start=time.clock()
    cnn = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = cnn.cursor()
    list_att = ['ltg','zgb','yg_rate','mgsy','mgjzc','jlr','jlrtb_rate','ystb_rate','jzcsy_rate','jzcfz_rate','mgwfplr','mgzbgj','mgxjllje']
    secu_list = Secu_list()
    secu_list=secu_list[8:]
    date_list, y2m = Date_list()
    deal_sql(list_att)
    cnn.close()
    cur239.close()

