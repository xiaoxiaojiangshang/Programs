import numpy as np
import matplotlib.pyplot as plt
import MySQLdb


def sql_plot(id_min,id_max,id_type):
    for i in range(id_min,id_max):
        for j in range(id_type):
            sql_str = ("SELECT avg FROM algorithm_realtime WHERE zl_id =%d AND TYPE =%d" % (i, j))
            cur239.execute(sql_str)
            list = []
            for avg in cur239.fetchall():
                list.append(avg)
            if len(list) == 0:
                continue
            del list[0]
            x = np.arange(0, len(list), 1)
            y = list
            plt.figure()
            label = "zl_id=%d and type=%d" % (i, j)
            plt.legend(loc='best')
            plt.plot(x, y, c='r')
            plt.ylabel("avg")
            plt.title(label)
            plt.grid()
            plt.savefig("%s" % (label))
            # plt.show()
def sql_plot_plus():
    sql_str = ("SELECT zl_id,MAX(gen) FROM cl_jz GROUP BY zl_id")
    cur239.execute(sql_str)
    dict2 = {}
    for zl_id, max_gen in cur239.fetchall():
        dict2[zl_id] = max_gen
    dict3 = {}
    for key in dict2:
        sql_str = ("SELECT zl_id,cl_id,gen FROM cl_jz WHERE zl_id=%d and gen=%d" % (key, dict2[key]))
        cur239.execute(sql_str)
        for zl_id, cl_id, max_gen in cur239.fetchall():
            key = (zl_id, cl_id)
            if key in dict3:
                continue
            else:
                dict3[key] = max_gen
    for key in dict3:
        sql_str = ("SELECT from_unixtime(days*86400),jz FROM cl_jz WHERE zl_id=%d and cl_id=%d and gen=%d" % (
        key[0], key[1], dict3[key]))
        cur239.execute(sql_str)
        x = []
        y = []
        for days, jz in cur239.fetchall():
            x.append(days)
            y.append(jz)
        label = "zl_id=%d and cl_id=%d and gen=%d" % (key[0], key[1], dict3[key])
        plt.figure()
        plt.title(label)
        plt.legend(loc='best')
        plt.plot(x, y, c='r')
        plt.ylabel("JZ")
        plt.xlabel("Date")
        plt.title(label)
        plt.grid()
        plt.savefig("%s.jpg" % (label))
        # plt.show()
    cur239.close()
    cnn.close()
if __name__ == "__main__":
    cnn= MySQLdb.connect(host='192.168.1.210', user='dev', passwd='sd61131707', db='afa_cps', charset='utf8')
    cur239 = cnn.cursor()
    sql_plot(6,24,2)
    sql_plot_plus()
    cur239.close()
    cnn.close()



