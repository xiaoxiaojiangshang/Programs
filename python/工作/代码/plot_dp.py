
import matplotlib.pyplot as plt
import MySQLdb

def set_bench(date_start,date_end):
    cnn = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='db_fp_data_new', charset='utf8')
    cur239 = cnn.cursor()
    sql_str = ("SELECT datetime,zf FROM `dp_day` WHERE code =000300 AND datetime<='%s' AND datetime>='%s' ORDER BY datetime"%(date_end,date_start))
    cur239.execute(sql_str)
    x_b=[]
    y_b=[]
    z=1
    for datetime,zf in cur239.fetchall():
        x_b.append(datetime)
        z=z*(1+zf/100)
        y_b.append(z)
    label="300_ZF"
    plt.plot(x_b, y_b, c='b',label=label)
    plt.legend(loc='best')
    cur239.close()
    cnn.close()
    return x_b
def sql_plot_plus():
    sql_str = ("SELECT zl_id,MAX(gen) FROM cl_jz GROUP BY zl_id")
    cur210.execute(sql_str)
    dict2 = {}
    for zl_id, max_gen in cur210.fetchall():
        dict2[zl_id] = max_gen
    dict3 = {}
    for key in dict2:
        sql_str = ("SELECT zl_id,cl_id,gen FROM cl_jz WHERE zl_id=%d and gen=%d" % (key, dict2[key]))
        cur210.execute(sql_str)
        for zl_id, cl_id, max_gen in cur210.fetchall():
            key = (zl_id, cl_id)
            if key in dict3:
                continue
            else:
                dict3[key] = max_gen
    for key in dict3:
        sql_str = ("SELECT from_unixtime(days*86400-60*60 *8),jz FROM cl_jz WHERE zl_id=%d and cl_id=%d and gen=%d" % ( key[0], key[1], dict3[key]))
        cur210.execute(sql_str)
        x = []
        y = []
        for days, jz in cur210.fetchall():
            x.append(days)
            y.append(jz)
        plt.figure()
        date_min=x[0]
        date_max=x[-1]
        x_b=set_bench(date_min,date_max)
        for i in range(len(x_b)):
            if x_b[i] in x:
                continue
            else:
                x.insert(i,x_b[i])
                y.insert(i,y[i-1])
        plt.plot(x, y, c='r',label='Strategy')
        label = "zl_id=%d and cl_id=%d and gen=%d" % (key[0], key[1], dict3[key])
        plt.title(label)
        plt.legend(loc='best')
        plt.ylabel("JZ")
        plt.xlabel("Date")
        plt.grid()
        plt.savefig("%s.jpg" % (label))
        plt.show()
if __name__ == "__main__":
    cnn210= MySQLdb.connect(host='192.168.1.210', user='dev', passwd='sd61131707', db='afa_cps', charset='utf8')
    cur210 = cnn210.cursor()
    sql_plot_plus()
    cur210.close()
    cnn210.close()