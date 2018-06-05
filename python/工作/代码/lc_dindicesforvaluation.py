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
    except:
        print u'%s 写数据库失败!'%tablename
        return  False
def write_sql(cur,dic_list_al):
    for dic in dic_list_al:
        for id,days,turn_rate,close,chg,zsz in dic:
            if year != days.year:
                year = days.year
                tablename='select_stock_filter_%d'%(year)
            cur.execute("update tablename set turnrate=(select turnrate from tablename where id=dic[id] AND days=dic[days]),close=(select close from tablename where id=dic[id] AND days=dic[days]),"
                        "chg=(select chg from tablename where id=dic[id] AND days=dic[days]),zsz=(select zsz from tablename where id=dic[id] AND days=dic[days])")

def datetime2days(dt):
    if datetime == type(dt):
        timeArray = time.strptime("%s" % dt.date(), "%Y-%m-%d")  # %H:%M:%S
    else:
        timeArray = time.strptime("%s" % dt, "%Y-%m-%d")
    days = int((time.mktime(timeArray) + 8 * 60 * 60) / 86400)
    return days

if __name__ == "__main__":


    # 一下代码为数据读取的示例
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()
    last = None
    cl_zb_fieldnames = ['SecuCode', 'TradingDay', 'TurnoverRate', 'ClosePrice', 'ChangePCT', 'TotalMV']
    cur.execute("SELECT %s FROM qt_performance LEFT JOIN secumain ON qt_performance.InnerCode = secumain.InnerCode ORDER BY TradingDay DESC"%(",".join(cl_zb_fieldnames)) )
    maper_dic = {'SecuCode':'id','TradingDay':'days','TurnoverRate':'turnover_rate','ClosePrice':'close','ChangePCT':'chg','TotalMV':'zsz'}
    cl_zb_dic_list = []
    for line in cur.fetchall():
        line_dict ={}
        for iline in range(len(line)):
            if cl_zb_fieldnames[iline]=='TradingDay':
                value=datetime2days(line[iline])
            else:
                value=line[iline]
            name = cl_zb_fieldnames[iline]
            line_dict[maper_dic[name]] = value
        cl_zb_dic_list.append(line_dict)
    # 一下代码为数据写入到数据库的示例
    new_cl_zb_fieldnames = []
    for name in cl_zb_fieldnames:
        new_cl_zb_fieldnames += [maper_dic[name]]
    conn = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur = conn.cursor()
    year=1000
    tablename=''
    write_sql(cur,cl_zb_dic_list)
    # common_multi_insert(cur, "select_stock_filter_2017", new_cl_zb_fieldnames, cl_zb_dic_list)
    cur.close()
    conn.close()