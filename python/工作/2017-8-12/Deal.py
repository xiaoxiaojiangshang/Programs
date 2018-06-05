
import xlrd
import xlwt
import time
import sys
# from secu_dict import Secu_list

def timestamp_datetime(value):
    format = '%Y-%m-%d'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def compare(excel1,excel2):
    data1=xlrd.open_workbook(excel1)   #open file
    sh1 = data1.sheets()[0]
    nrows = sh1.nrows
    dict1_d2d={}
    for i in range(nrows):
        row_data=sh1.row_values(i)
        dict1_d2d[row_data[0]]=row_data[1]   # only two col

    data2 = xlrd.open_workbook(excel2)  # open file
    sh2 = data2.sheets()[0]
    nrows = sh2.nrows
    dict2_d2d = {}
    for i in range(1,nrows):
        row_data = sh2.row_values(i)
        dict2_d2d[row_data[0]] = row_data[1]  # only two col
    return dict1_d2d,dict2_d2d
def write2excel(dict1_d2d,dict2_d2d,K):
    list_date = []
    for days in dict1_d2d:
        list_date.append(days)
    list_date = sorted(list_date)  # the result of sorted is another ,must reagine
    cow=1
    for i in range(len(list_date)):
        Date = list_date[i]
        if K == 0:
            if i==0:
                table.write(0,0,'DATE')
                table.write(0,1,'%s'%(excel1_name[K]))
                table.write(0,2, '%s'%(excel2_name[K]))
                table.write(0,3,'Diff')
            Date_temp=(Date-33331+7762)*86400
            Date_temp=timestamp_datetime(Date_temp)
            table.write(cow, 0, Date_temp)
            table.write(cow, 1, dict1_d2d[Date])
            a=(dict1_d2d[Date])
            if Date in dict2_d2d:
                table.write(cow,2,dict2_d2d[Date])
                b=dict2_d2d[Date]
                if a is not None:
                    c="%.4f%%"%((a-b)/a*100)
                    table.write(cow,3,c)
            cow = cow + 1
        else:
            if i==0:
                table.write(0,K*3+1,'%s'%(excel1_name[K]))
                table.write(0,K*3+2, '%s'%(excel2_name[K]))
                table.write(0,K*3+3,'Diff')
            table.write(cow, K*3+1, dict1_d2d[Date])
            a =dict1_d2d[Date]
            if Date in dict2_d2d:
                table.write(cow, K*3+2, dict2_d2d[Date])
                b =dict2_d2d[Date]
                if a:
                    if isinstance(a,unicode):
                        # print a
                        pass
                    else:
                        c = "%.4f%%"%((a-b)/a*100)
                        table.write(cow, K*3+3,c)
            cow = cow + 1
if __name__ == "__main__":
    excel1_name=['ltsz','zsz','jtsy_rate']
    excel2_name=['ltsz_DC','zsz_DC','jtsy_rate_DC']
    # secu_list=Secu_list()
    secu_list =[]
    for i in sys.argv[1]:
        if i!=',':
            secu_list.append(int(i[0]))
    for secu_id in secu_list:
        file = xlwt.Workbook(encoding='utf-8')
        # table = file.add_sheet('%s'%(secu_id),cell_overwrite_ok=True)
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        for i in range(len(excel1_name)):
            name1='%d_%s.xls'%(secu_id,excel1_name[i])
            name2='%d_%s.xls'%(secu_id,excel2_name[i])
            dict1_d2d,dict2_d2d=compare(name1,name2)
            write2excel(dict1_d2d,dict2_d2d,i)
        file.save('C:\Users\user\Desktop\Date\%s.xls' % (secu_id))