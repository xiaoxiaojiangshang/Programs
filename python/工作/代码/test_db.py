# -*- coding: utf-8 -*-
import MySQLdb

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
            sql="REPLACE INTO {0}({1}) VALUES{2}".format(tablename,",".join(fieldnames), val_sql)
            # cur = connection.cursor()
            cur.execute(sql,val_arr)
        return True
    except:
        print u'%s 写数据库失败!'%tablename
        return  False

if __name__ == "__main__":

    # 一下代码为数据读取的示例
    conn = MySQLdb.connect(host='192.168.1.239', user='root', passwd='nb2008xl', db='db_fp_data_new', charset='utf8')
    cur = conn.cursor()
    last = None
    # 提取最近250个交易日的起始日期
    cur.execute("SELECT DISTINCT datetime FROM dp_day ORDER BY datetime DESC LIMIT %d,1" % 10)
    # 提取所有数据
    sql_str = "SELECT code,datetime,open_,high_,low_,close_,volum,zf FROM dp_day WHERE datetime>'%s' ORDER BY code ASC, datetime ASC" % cur.fetchone()
    # print sql_str
    cur.execute(sql_str)
    for code, dt, open_, high_, low_, close_, volume, zf in cur.fetchall():
        pass


    # 一下代码为数据写入到数据库的示例
    cl_zb_fieldnames = ['field1', 'field2']
    cl_zb_dic_list = [{'field1':1, 'field2':2}, {'field1':11, 'field2':22}]
    common_multi_insert(cur, "db_fp_data_new.aa_test", cl_zb_fieldnames, cl_zb_dic_list)

    cur.close()
    conn.close()