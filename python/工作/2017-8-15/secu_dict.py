import MySQLdb

def Secu_list():
    cnn = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = cnn.cursor()
    secu_list_inno=[]
    sql_name="hs_finance"
    sql_str = ("SELECT id FROM %s  GROUP by id "%(sql_name))
    cur239.execute(sql_str)
    for id in cur239.fetchall():
        secu_list_inno.append(id[0])
    secu_list = []
    for i in range(1990, 2018, 1):
        sql_name = "select_stock_filter_%d" % (i)
        sql_str = ("SELECT id FROM %s GROUP by id " % (sql_name))
        cur239.execute(sql_str)
        for id in cur239.fetchall():
            if id[0] not in secu_list:
                secu_list.append(id[0])
    secu_list= [val for val in secu_list if val in secu_list_inno]  #Intersection
    secu_list.sort()
    return secu_list

if __name__ == "__main__":
    Secu_list()