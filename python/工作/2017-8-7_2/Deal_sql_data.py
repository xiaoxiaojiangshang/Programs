import MySQLdb
import xlwt
import time
from secu_dict import Secu_list
def timestamp_datetime(value):
    format = '%Y-%m-%d'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def deal_sql_data():
    cnn = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = cnn.cursor()
    list=['ltsz','zsz','jtsy_rate']
    secu_list = Secu_list()
    for secu_id in secu_list:
        for key in list:
            dict_d2d={}
            for i in range(1990,2018,1):
                sql_name="select_stock_filter_%d"%(i)
                sql_str = ("SELECT DATE(from_unixtime(`days`*86400)),%s FROM %s WHERE id =%d ORDER BY days"%(key,sql_name,secu_id[0]))
                cur239.execute(sql_str)
                for days,data in cur239.fetchall():
                    dict_d2d[days]=data
            file=xlwt.Workbook(encoding='utf-8')
            table=file.add_sheet('%s'%(key))
            list_date=[]
            for days in dict_d2d:
                list_date.append(days)
            list_date=sorted(list_date)  #the result of sorted is another ,must reagine
            cow = 0
            for i in range(len(list_date)):
                Date=list_date[i]
                table.write(cow,0,Date)
                table.write(cow,1,dict_d2d[Date])
                cow=cow+1
            file.save('C:\Users\user\Desktop\H_Data\%d_%s.xls'%(secu_id[0],key))


if __name__ == "__main__":
    deal_sql_data()
