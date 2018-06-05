import MySQLdb

def Date_list():
    cnn = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = cnn.cursor()
    Date_list=[]
    y2m={}
    for i in range(1990,2018,1):
        sql_name="select_stock_filter_%d"%(i)
        sql_str = ("SELECT days FROM %s GROUP by days "%(sql_name))
        cur239.execute(sql_str)
        for day in cur239.fetchall():
            Date_list.append(day[0])   # return is a touple,first is need
        sql_str = ("SELECT min(days),max(days) FROM %s " % (sql_name))
        cur239.execute(sql_str)
        for min_day,max_day in cur239.fetchall():
            y2m[i]=(min_day,max_day)
    return Date_list,y2m
if __name__ == "__main__":
    Date_list()