import xlrd
import xlwt
import time

def timestamp_datetime(value):
    format = '%Y-%m-%d'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def compare(excel1,excel2,K):
    data1=xlrd.open_workbook(excel1)   #open file
    sh1 = data1.sheets()[0]
    nrows = sh1.nrows
    dict1_d2d={}
    for i in range(nrows):
        row_data=sh1.row_values(i)
        temp = row_data[0]
        dict1_d2d[row_data[0]]=row_data[1]   # only two col

    data2 = xlrd.open_workbook(excel2)  # open file
    sh2 = data2.sheets()[0]
    nrows = sh2.nrows
    dict2_d2d = {}
    for i in range(1,nrows):
        row_data = sh2.row_values(i)
        temp2=row_data[0]
        dict2_d2d[row_data[0]] = row_data[1]  # only two col

    key='%s Pk %s'%(excel1_name[K],excel2_name[K])
    file = xlwt.Workbook(encoding='utf-8')
    table = file.add_sheet('%s'% (key))
    list_date = []
    for days in dict1_d2d:
        list_date.append(days)
    list_date = sorted(list_date)  # the result of sorted is another ,must reagine
    cow = 0
    for i in range(len(list_date)):
        Date = list_date[i]
        Date_temp=(Date-33331+7762)*86400
        Date_temp=timestamp_datetime(Date_temp)
        table.write(cow, 0, Date_temp)
        table.write(cow, 1, dict1_d2d[Date])
        a=(dict1_d2d[Date])
        if Date in dict2_d2d:
            table.write(cow,2,dict2_d2d[Date])
            b=dict2_d2d[Date]
            if a is not None:
                table.write(cow,3,(a-b)/a)
        cow = cow + 1
    file.save('%s.xls' % (key))

if __name__ == "__main__":
    excel1_name=['ltsz','zsz','jtsy_rate']
    excel2_name=['ltsz_DC','zsz_DC','jtsy_rate_DC']
    # excel1_name = [ 'jtsy_rate']
    # excel2_name = [ 'jtsy_rate_DC']
    for i in range(len(excel1_name)):
        name1='%s.xls'%(excel1_name[i])
        name2='%s.xls'%(excel2_name[i])
        compare(name1,name2,i)
