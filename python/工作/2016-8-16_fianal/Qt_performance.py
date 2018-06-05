# -*- coding: utf-8 -*-
#读取'SecuCode', 'TradingDay', 'TurnoverRate', 'ClosePrice', 'ChangePCT', 'TotalMV
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
    except Exception as ex:
        print ex
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

def cal_quarter(dt):
    start_year = 1990  # 从 1990 年开始
    if dt.month <= 3:
        # 第一季度
        the_quarter = 1
    elif dt.month <= 6:
        # 第二季度
        the_quarter = 2
    elif dt.month <= 9:
        # 第三季度
        the_quarter = 3
    else:
        # 第四季度
        the_quarter = 4
    quanter_counter = 4 * (dt.year - start_year) + the_quarter
    return quanter_counter

def load_zqdm():
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()

    sql_str = "SELECT Innercode,CompanyCode,SecuCode FROM secumain WHERE SecuCategory=1"
    cur.execute(sql_str)

    Innercode2SecuCode = {}
    CompanyCode2SecuCode = {}
    for Innercode,CompanyCode,SecuCode in cur.fetchall():
        if not SecuCode.isdigit(): continue
        Innercode2SecuCode[Innercode] = SecuCode
        CompanyCode2SecuCode[CompanyCode] = SecuCode

    cur.close()
    conn.close()

    return Innercode2SecuCode, CompanyCode2SecuCode

def load_ct_systemconst():
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()

    sql_str = "SELECT LB,DM,MS FROM ct_systemconst WHERE LB=1158"
    cur.execute(sql_str)

    LB2DM = {}
    for LB, DM, MS in cur.fetchall():
        t_list = LB2DM.get(LB, [])
        t_list += [(DM, MS.encode('utf8'))]
        LB2DM[LB] = t_list

    cur.close()
    conn.close()
    return LB2DM

def update_ltsz(Innercode2SecuCode):
    conn239 = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = conn239.cursor()
    sql_str=" Drop table if exists temp"
    cur239.execute(sql_str)
    sql_str = "CREATE TABLE temp(days INT NOT NULL, id INT NOT NULL, ltsz FLOAT NULL, jtsy_rate FLOAT NULL ,zsz FLOAT NULL, gx_rate FLOAT NULL,PRIMARY KEY ( days,id )); "
    cur239.execute(sql_str)
    cur239.execute("ALTER TABLE `temp` ENGINE = MYISAM ")


    # 往临时表写数据
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()
    sql_str = "SELECT InnerCode,TradingDay,NegotiableMV,PE,TotalMV,DividendRatio FROM lc_dindicesforvaluation ORDER BY TradingDay DESC"
    cur.execute(sql_str)

    data_list = []
    year_set = set()
    invalid_InnerCode_set = set()
    for InnerCode, TradingDay, NegotiableMV,PE,TotalMV,DividendRatio in cur.fetchall():
        #if not TotalMV:continue
        if TradingDay.year not in year_set: year_set.add(TradingDay.year)
        if InnerCode not in Innercode2SecuCode:
            #print InnerCode
            invalid_InnerCode_set.add(InnerCode)
            continue
        stock_id = int(Innercode2SecuCode[InnerCode])
        data_list += [{'days': datetime2days(TradingDay), 'id': stock_id, 'ltsz':NegotiableMV, 'jtsy_rate':PE, 'zsz':TotalMV, 'gx_rate':DividendRatio}]

    print invalid_InnerCode_set
    common_multi_insert(cur239, "temp", ['days', 'id', 'ltsz', 'jtsy_rate', 'zsz', 'gx_rate'], data_list)


    for year in year_set:
        print year
        tablename = "select_stock_filter_%d"%year
        sql_str = "UPDATE %s,temp SET %s.ltsz = temp.ltsz,%s.jtsy_rate=temp.jtsy_rate,%s.zsz=temp.zsz,%s.gx_rate=temp.gx_rate WHERE %s.id = temp.id and %s.days=temp.days"%(tablename, tablename, tablename, tablename, tablename, tablename, tablename)
        cur239.execute(sql_str)
    cur.close()
    conn.close()
    cur239.close()
    conn239.close()

# 业绩预告
def update_from_LC_PerformanceForecast(Innercode2SecuCode, LB2DM):
    """
    业绩预告
    :param Innercode2SecuCode: 
    :param LB2DM: 
    :return: 
    """
    conn239 = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = conn239.cursor()
    sql_str = " Drop table if exists temp_LC_PerformanceForecast"
    cur239.execute(sql_str)
    sql_str = "CREATE TABLE temp_LC_PerformanceForecast(tid TINYINT(5) NOT NULL, id MEDIUMINT(6) NOT NULL, " \
              "update_day SMALLINT(5) NULL,data_type INT NOT NULL, yg_rate FLOAT NULL, " \
              "yg_type VARCHAR(16) NULL,PRIMARY KEY ( tid,id,update_day,data_type )); "
    # yg_rate_floor FLOAT NULL, yg_rate_ceil FLOAT NULL,
    cur239.execute(sql_str)
    cur239.execute("ALTER TABLE `temp_LC_PerformanceForecast` ENGINE = MYISAM ")

    # 往临时表写数据
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()
    sql_str = "SELECT CompanyCode,InfoPublDate,EndDate,ForcastType,(EGrowRateFloorC+EGrowthRateCeilC)/2.0 AS yg_rate,ForecastObject FROM lc_performanceforecast ORDER BY InfoPublDate DESC"
    cur.execute(sql_str)

    data_list = []
    year_set = set()
    invalid_InnerCode_set = set()
    dm2ms = dict(LB2DM[1158])
    for CompanyCode,InfoPublDate,EndDate,ForcastType,yg_rate,ForecastObject in cur.fetchall():
        # if not TotalMV:continue
        if InfoPublDate.year not in year_set: year_set.add(InfoPublDate.year)
        if CompanyCode not in Innercode2SecuCode:
            # print InnerCode
            #invalid_InnerCode_set.add(InnerCode)
            continue

        tid = cal_quarter(EndDate)
        stock_id = int(Innercode2SecuCode[CompanyCode])
        data_type = 3
        data_list += [
            {'tid':tid, 'id': stock_id, 'update_day': datetime2days(InfoPublDate), 'data_type':data_type, 'yg_rate': yg_rate, 'yg_type': dm2ms[ForcastType]}]

    print invalid_InnerCode_set
    field_list = ['tid', 'id', 'update_day', 'data_type', 'yg_rate', 'yg_type']
    common_multi_insert(cur239, "temp_LC_PerformanceForecast", field_list, data_list)

    tablename = "hs_finance"
    temp_tablename = "temp_LC_PerformanceForecast"
    sql_str = "REPLACE INTO {0}({1}) SELECT {1} FROM {2}".format(tablename, ",".join(field_list), temp_tablename)
    print sql_str
    cur239.execute(sql_str)

    cur.close()
    conn.close()
    cur239.close()
    conn239.close()

# 从业绩快报中整数据
def update_from_LC_PerformanceLetters(CompanyCode2SecuCode, LB2DM):
    conn239 = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = conn239.cursor()
    sql_str = " Drop table if exists temp_lc_performanceletters"
    cur239.execute(sql_str)
    sql_str = "CREATE TABLE temp_lc_performanceletters(tid TINYINT(3) NOT NULL, id MEDIUMINT(6) NOT NULL, " \
              "update_day INT NOT NULL,data_type INT NOT NULL, jlr FLOAT NULL, ystb_rate FLOAT NULL, jlrtb_rate FLOAT NULL, jzcsy_rate FLOAT NULL, " \
              "mgjzc FLOAT NULL, mgsy FLOAT NULL, mgxjllje FLOAT NULL,PRIMARY KEY ( tid,id,update_day,data_type )); "

    print sql_str
    cur239.execute(sql_str)
    cur239.execute("ALTER TABLE `temp_lc_performanceletters` ENGINE = MYISAM ")

    # 往临时表写数据
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()

    # 通过CompanyCode 和 EndDate 确定发布日期
    pub_date_dic = {}
    sql_str = "SELECT CompanyCode,InfoPublDate,EndDate FROM lc_performanceletters WHERE Mark=2 AND PeriodMark=3"
    cur.execute(sql_str)
    for CompanyCode, InfoPublDate, EndDate in cur.fetchall():
        pub_date_dic[(CompanyCode, EndDate)] = InfoPublDate

    sql_str = "SELECT CompanyCode,EndDate,InfoPublDate,Mark,PeriodMark,ROE,NPParentCompanyOwnersYOY,OperatingRevenueYOY,NPParentCompanyOwners,NetAssetPS,BasicEPS,NetOperateCashFlowPS FROM" \
              " lc_performanceletters WHERE Mark=2 AND PeriodMark=3 ORDER BY EndDate DESC"
    cur.execute(sql_str)

    data_list = []
    year_set = set()
    invalid_pub_date_set = set()
    field_list = ['tid', 'id', 'update_day', 'data_type', 'jlr', 'ystb_rate', 'jlrtb_rate', 'jzcsy_rate', 'mgjzc', 'mgsy', 'mgxjllje']
    tuple_list = []
    for CompanyCode,EndDate,InfoPublDate,Mark,PeriodMark,ROE,NPParentCompanyOwnersYOY,OperatingRevenueYOY,NPParentCompanyOwners,NetAssetPS,BasicEPS,NetOperateCashFlowPS in cur.fetchall():
        # if not TotalMV:continue
        if InfoPublDate.year not in year_set: year_set.add(InfoPublDate.year)
        if CompanyCode not in Innercode2SecuCode:
            # print InnerCode
            # invalid_InnerCode_set.add(InnerCode)
            continue
        stock_id = int(Innercode2SecuCode[CompanyCode])
        tid = cal_quarter(EndDate)
        if (CompanyCode, EndDate) not in pub_date_dic:
            invalid_pub_date_set.add((CompanyCode, EndDate))
            continue

        update_day = datetime2days(InfoPublDate)#(pub_date_dic[(CompanyCode, EndDate)])
        data_type = 2 # 快报
        jlr = NPParentCompanyOwners  # 净利润
        ystb_rate = OperatingRevenueYOY  # 营收同比增
        jlrtb_rate = NPParentCompanyOwnersYOY  # 净利润同比增
        jzcsy_rate = ROE  # 净资产收益率
        #jzcfz_rate = DebtAssetsRatio  # 净资产负债率
        mgjzc = NetAssetPS  # 每股净资产
        mgsy = BasicEPS  # 每股收益
        # mgwfplr = UndividedProfit  # 每股未分配利润
        # mgzbgj = CapitalSurplusFundPS  # 每股资本公积
        mgxjllje = NetOperateCashFlowPS  # 每股经营活动产生的现金流量净额

        data_list += [
            {'tid': tid, 'id': stock_id, 'update_day': update_day, 'data_type': data_type, 'jlr': jlr, 'ystb_rate': ystb_rate, "jlrtb_rate": jlrtb_rate,
             'jzcsy_rate': jzcsy_rate, 'mgjzc': mgjzc, 'mgsy': mgsy, 'mgxjllje': mgxjllje}]

    print invalid_pub_date_set

    common_multi_insert(cur239, "temp_lc_performanceletters", field_list, data_list)

    tablename = "hs_finance"
    temp_tablename = "temp_lc_performanceletters"
    # update_field_list = field_list[2:]
    # t_str_list = []
    # for field in update_field_list:
    #     t_str_list += ["{0}.{2}={1}.{2}".format(tablename, temp_tablename, field)]
    # sql_str = "UPDATE {0},{1} SET {2} WHERE {0}.tid={1}.tid AND {0}.id={1}.id".format(tablename, temp_tablename,
    #                                                                                   ",".join(t_str_list))
    sql_str = "REPLACE INTO {0}({1}) SELECT {1} FROM {2}".format(tablename,",".join(field_list), temp_tablename)
    print sql_str
    cur239.execute(sql_str)

    cur.close()
    conn.close()
    cur239.close()
    conn239.close()

# 业绩报告
def update_from_lc_maindatanew(Innercode2SecuCode, LB2DM):

    conn239 = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = conn239.cursor()
    sql_str = " Drop table if exists temp_lc_maindatanew"
    cur239.execute(sql_str)
    sql_str = "CREATE TABLE temp_lc_maindatanew(tid TINYINT(3) NOT NULL, id MEDIUMINT(6) NOT NULL, bb_day SMALLINT(5) NULL, jlr FLOAT NULL, ystb_rate FLOAT NULL, jlrtb_rate FLOAT NULL, jzcsy_rate FLOAT NULL,jzcfz_rate FLOAT NULL, mgjzc FLOAT NULL, mgsy FLOAT NULL, mgwfplr FLOAT NULL, mgzbgj FLOAT NULL,mgxjllje FLOAT NULL,PRIMARY KEY ( tid,id )); "
    # yg_rate_floor FLOAT NULL, yg_rate_ceil FLOAT NULL,
    cur239.execute(sql_str)
    cur239.execute("ALTER TABLE `temp_lc_maindatanew` ENGINE = MYISAM ")

    # 往临时表写数据
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()

    # 通过CompanyCode 和 EndDate 确定发布日期
    pub_date_dic = {}
    sql_str = "SELECT CompanyCode,InfoPublDate,EndDate FROM lc_maindatanew"
    cur.execute(sql_str)
    for CompanyCode,InfoPublDate,EndDate in cur.fetchall():
        pub_date_dic[(CompanyCode, EndDate)] = InfoPublDate

    sql_str = "SELECT CompanyCode,EndDate,ROE,NetProfitGrowRate,OperatingRevenueGrowRate,NetProfit,DebtAssetsRatio,NetAssetPS,EPS,UndividedProfit,CapitalSurplusFundPS,OperCashFlowPS" \
              " FROM lc_mainindexnew ORDER BY EndDate DESC"
    cur.execute(sql_str)

    data_list = []
    year_set = set()
    invalid_pub_date_set = set()
    for CompanyCode,EndDate,ROE,NetProfitGrowRate,OperatingRevenueGrowRate,NetProfit,DebtAssetsRatio,NetAssetPS,EPS,UndividedProfit,CapitalSurplusFundPS,OperCashFlowPS in cur.fetchall():
        # if not TotalMV:continue
        if InfoPublDate.year not in year_set: year_set.add(InfoPublDate.year)
        if CompanyCode not in Innercode2SecuCode:
            # print InnerCode
            # invalid_InnerCode_set.add(InnerCode)
            continue
        stock_id = int(Innercode2SecuCode[CompanyCode])
        tid = cal_quarter(EndDate)
        if (CompanyCode, EndDate) not in pub_date_dic:
            invalid_pub_date_set.add((CompanyCode, EndDate))
            continue
        bb_day = datetime2days(pub_date_dic[(CompanyCode, EndDate)])
        jlr = NetProfit# 净利润
        ystb_rate = OperatingRevenueGrowRate # 营收同比增
        jlrtb_rate = NetProfitGrowRate # 净利润同比增
        jzcsy_rate = ROE # 净资产收益率
        jzcfz_rate = DebtAssetsRatio # 净资产负债率
        mgjzc  = NetAssetPS# 每股净资产
        mgsy = EPS # 每股收益
        mgwfplr = UndividedProfit# 每股未分配利润
        mgzbgj = CapitalSurplusFundPS # 每股资本公积
        mgxjllje = OperCashFlowPS # 每股经营活动产生的现金流量净额
        data_list += [
            {'tid': tid, 'id': stock_id, 'bb_day': bb_day, 'jlr': jlr, 'ystb_rate':ystb_rate, "jlrtb_rate":jlrtb_rate,
             'jzcsy_rate':jzcsy_rate, 'jzcfz_rate':jzcfz_rate, 'mgjzc':mgjzc, 'mgsy':mgsy, 'mgwfplr':mgwfplr,
             'mgzbgj':mgzbgj, 'mgxjllje':mgxjllje}]

    print invalid_pub_date_set
    field_list = ['tid','id','bb_day','jlr','ystb_rate','jlrtb_rate','jzcsy_rate','jzcfz_rate','mgjzc','mgsy','mgwfplr','mgzbgj','mgxjllje']
    common_multi_insert(cur239, "temp_lc_maindatanew", field_list, data_list)

    tablename = "hs_finance"
    temp_tablename = "temp_lc_maindatanew"
    update_field_list = field_list[2:]
    t_str_list = []
    for field in update_field_list:
        t_str_list += ["{0}.{2}={1}.{2}".format(tablename, temp_tablename, field)]
    sql_str = "UPDATE {0},{1} SET {2} WHERE {0}.tid={1}.tid AND {0}.id={1}.id".format(tablename, temp_tablename, ",".join(t_str_list))
    print sql_str
    cur239.execute(sql_str)

    cur.close()
    conn.close()
    cur239.close()
    conn239.close()

def update_from_lc_mainindexnew(Innercode2SecuCode, LB2DM):

    conn239 = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = conn239.cursor()
    sql_str = " Drop table if exists temp_lc_mainindexnew"
    cur239.execute(sql_str)
    sql_str = "CREATE TABLE temp_lc_mainindexnew(tid TINYINT(3) NOT NULL, id MEDIUMINT(6) NOT NULL, update_day SMALLINT(5) NULL, data_type TINYINT(3) NOT NULL," \
              "jlr FLOAT NULL,yysr FLOAT NULL, ystb_rate FLOAT NULL, jlrtb_rate FLOAT NULL, jzcsy_rate FLOAT NULL,jzcfz_rate FLOAT NULL, mgjzc FLOAT NULL, mgsy FLOAT NULL, " \
              "mgwfplr FLOAT NULL, mgzbgj FLOAT NULL,mgxjllje FLOAT NULL,PRIMARY KEY ( tid,id,update_day,data_type )); "
    # yg_rate_floor FLOAT NULL, yg_rate_ceil FLOAT NULL,
    cur239.execute(sql_str)
    cur239.execute("ALTER TABLE `temp_lc_mainindexnew` ENGINE = MYISAM ")

    # 往临时表写数据
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()

    # 通过CompanyCode 和 EndDate 确定发布日期
    pub_date_dic = {}
    sql_str = "SELECT CompanyCode,InfoPublDate,EndDate,OperatingReenue FROM lc_maindatanew"
    cur.execute(sql_str)
    for CompanyCode,InfoPublDate,EndDate,OperatingReenue in cur.fetchall():
        pub_date_dic[(CompanyCode, EndDate)] = (InfoPublDate, OperatingReenue)

    sql_str = "SELECT CompanyCode,EndDate,ROE,NetProfitGrowRate,OperatingRevenueGrowRate,NetProfit,DebtAssetsRatio,NetAssetPS,EPS,UndividedProfit,CapitalSurplusFundPS,OperCashFlowPS" \
              " FROM lc_mainindexnew ORDER BY EndDate DESC"
    cur.execute(sql_str)

    data_list = []
    year_set = set()
    invalid_pub_date_set = set()
    for CompanyCode,EndDate,ROE,NetProfitGrowRate,OperatingRevenueGrowRate,NetProfit,DebtAssetsRatio,NetAssetPS,EPS,UndividedProfit,CapitalSurplusFundPS,OperCashFlowPS in cur.fetchall():
        # if not TotalMV:continue
        if InfoPublDate.year not in year_set: year_set.add(InfoPublDate.year)
        if CompanyCode not in Innercode2SecuCode:
            # print InnerCode
            # invalid_InnerCode_set.add(InnerCode)
            continue
        stock_id = int(Innercode2SecuCode[CompanyCode])
        tid = cal_quarter(EndDate)
        if (CompanyCode, EndDate) not in pub_date_dic:
            invalid_pub_date_set.add((CompanyCode, EndDate))
            continue
        update_day = datetime2days(pub_date_dic[(CompanyCode, EndDate)][0])
        data_type = 1
        yysr = pub_date_dic[(CompanyCode, EndDate)][1] # 营业收入
        jlr = NetProfit# 净利润
        ystb_rate = OperatingRevenueGrowRate # 营收同比增
        jlrtb_rate = NetProfitGrowRate # 净利润同比增
        jzcsy_rate = ROE # 净资产收益率
        jzcfz_rate = DebtAssetsRatio # 净资产负债率
        mgjzc  = NetAssetPS# 每股净资产
        mgsy = EPS # 每股收益
        mgwfplr = UndividedProfit# 每股未分配利润
        mgzbgj = CapitalSurplusFundPS # 每股资本公积
        mgxjllje = OperCashFlowPS # 每股经营活动产生的现金流量净额
        data_list += [
            {'tid': tid, 'id': stock_id, 'update_day': update_day, 'data_type':data_type,'jlr': jlr, 'yysr':yysr,'ystb_rate':ystb_rate, "jlrtb_rate":jlrtb_rate,
             'jzcsy_rate':jzcsy_rate, 'jzcfz_rate':jzcfz_rate, 'mgjzc':mgjzc, 'mgsy':mgsy, 'mgwfplr':mgwfplr,
             'mgzbgj':mgzbgj, 'mgxjllje':mgxjllje}]

    print invalid_pub_date_set
    field_list = ['tid','id','update_day','data_type','jlr','yysr','ystb_rate','jlrtb_rate','jzcsy_rate','jzcfz_rate','mgjzc','mgsy','mgwfplr','mgzbgj','mgxjllje']
    common_multi_insert(cur239, "temp_lc_mainindexnew", field_list, data_list)

    tablename = "hs_finance"
    temp_tablename = "temp_lc_mainindexnew"
    update_field_list = field_list[2:]
    t_str_list = []
    # for field in update_field_list:
    #     t_str_list += ["{0}.{2}={1}.{2}".format(tablename, temp_tablename, field)]
    # sql_str = "UPDATE {0},{1} SET {2} WHERE {0}.tid={1}.tid AND {0}.id={1}.id".format(tablename, temp_tablename, ",".join(t_str_list))
    sql_str = "REPLACE INTO {0}({1}) SELECT {1} FROM {2}".format(tablename, ",".join(field_list), temp_tablename)
    print sql_str
    cur239.execute(sql_str)

    cur.close()
    conn.close()
    cur239.close()
    conn239.close()

def update_from_lc_sharestru(CompanyCode2SecuCode, LB2DM):
    conn239 = MySQLdb.connect(host='192.168.1.239', user='jgp', passwd='123456', db='com_stock', charset='utf8')
    cur239 = conn239.cursor()
    sql_str = " Drop table if exists temp_lc_sharestru"
    cur239.execute(sql_str)
    sql_str = "CREATE TABLE temp_lc_sharestru(tid TINYINT(5) NOT NULL, id MEDIUMINT(6) NOT NULL, update_day SMALLINT(5) NULL, data_type TINYINT(3) NOT NULL," \
              "zgb FLOAT NULL,ltg FLOAT NULL,PRIMARY KEY ( tid,id,update_day,data_type )); "
    # yg_rate_floor FLOAT NULL, yg_rate_ceil FLOAT NULL,
    cur239.execute(sql_str)
    cur239.execute("ALTER TABLE `temp_lc_sharestru` ENGINE = MYISAM ")

    # 往临时表写数据
    conn = MySQLdb.connect(host='192.168.1.212', user='dev', passwd='sd61131707', db='jydb1', charset='utf8')
    cur = conn.cursor()


    sql_str = "SELECT CompanyCode,InfoPublDate,EndDate,AFloats,Ashares FROM lc_sharestru ORDER BY EndDate DESC"
    cur.execute(sql_str)

    data_list = []
    invalid_pub_date_set = set()
    for CompanyCode,InfoPublDate,EndDate,AFloats,Ashares in cur.fetchall():
        # if not TotalMV:continue
        if not InfoPublDate:
            invalid_pub_date_set.add(EndDate)
            continue
        if CompanyCode not in Innercode2SecuCode:
            # print InnerCode
            # invalid_InnerCode_set.add(InnerCode)
            continue
        stock_id = int(Innercode2SecuCode[CompanyCode])
        tid = cal_quarter(EndDate)

        update_day = datetime2days(InfoPublDate)
        data_type = 4
        ltg = AFloats # 流通股
        zgb = Ashares # 总股本
        data_list += [
            {'tid': tid, 'id': stock_id, 'update_day': update_day, 'data_type':data_type,'ltg': ltg, 'zgb':zgb}]

    print invalid_pub_date_set
    field_list = ['tid','id','update_day','data_type','ltg','zgb']
    common_multi_insert(cur239, "temp_lc_sharestru", field_list, data_list)

    tablename = "hs_finance"
    temp_tablename = "temp_lc_sharestru"
    update_field_list = field_list[2:]
    t_str_list = []
    # for field in update_field_list:
    #     t_str_list += ["{0}.{2}={1}.{2}".format(tablename, temp_tablename, field)]
    # sql_str = "UPDATE {0},{1} SET {2} WHERE {0}.tid={1}.tid AND {0}.id={1}.id".format(tablename, temp_tablename, ",".join(t_str_list))
    sql_str = "REPLACE INTO {0}({1}) SELECT {1} FROM {2}".format(tablename, ",".join(field_list), temp_tablename)
    print sql_str
    cur239.execute(sql_str)

    cur.close()
    conn.close()
    cur239.close()
    conn239.close()

if __name__ == "__main__":

    Innercode2SecuCode, CompanyCode2SecuCode = load_zqdm()

    #update_ltsz(Innercode2SecuCode)

    LB2DM = load_ct_systemconst()

    # 业绩预告
    # update_from_LC_PerformanceForecast(CompanyCode2SecuCode, LB2DM)

    # 从业绩快报 表更新每股指标和非每股指标
    # update_from_LC_PerformanceLetters(CompanyCode2SecuCode, LB2DM)

    # 业绩报告
    #update_from_lc_mainindexnew(CompanyCode2SecuCode, LB2DM)

    # 股权结构变动
    update_from_lc_sharestru(CompanyCode2SecuCode, LB2DM)


