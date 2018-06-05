
import wmi
import os
import sys
import platform
import time
import socket


def sys_version():
    c = wmi.WMI()
    # 获取操作系统版本
    for sys in c.Win32_OperatingSystem():
        print "Version:%s" % sys.Caption.encode("UTF8"), "Vernum:%s" % sys.BuildNumber
        print  sys.OSArchitecture.encode("UTF8")  # 系统是32位还是64位的
        print sys.NumberOfProcesses  # 当前系统运行的进程总数


def cpu_mem():
    c = wmi.WMI()
    # CPU类型和内存
    for processor in c.Win32_Processor():
        # print "Processor ID: %s" % processor.DeviceID
        print "Process Name: %s" % processor.Name.strip()
    for Memory in c.Win32_PhysicalMemory():
        print "Memory Capacity: %.fMB" % (int(Memory.Capacity) / 1048576)


def cpu_use():
    # 5s取一次CPU的使用率
    c = wmi.WMI()
    while True:
        for cpu in c.Win32_Processor():
            timestamp = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
            print '%s | Utilization: %s: %d %%' % (timestamp, cpu.DeviceID, cpu.LoadPercentage)
            time.sleep(5)


def disk():
    c = wmi.WMI()
    # 获取硬盘分区
    for physical_disk in c.Win32_DiskDrive():
        for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                print physical_disk.Caption.encode("UTF8"), partition.Caption.encode("UTF8"), logical_disk.Caption

                # 获取硬盘使用百分情况
    for disk in c.Win32_LogicalDisk(DriveType=3):
        print disk.Caption, "%0.2f%% free" % (100.0 * long(disk.FreeSpace) / long(disk.Size))


def network():
    c = wmi.WMI()
    # 获取MAC和IP地址
    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
        print "MAC: %s" % interface.MACAddress
    for ip_address in interface.IPAddress:
        print "ip_add: %s" % ip_address
    print

    # 获取自启动程序的位置
    for s in c.Win32_StartupCommand():
        print "[%s] %s <%s>" % (s.Location.encode("UTF8"), s.Caption.encode("UTF8"), s.Command.encode("UTF8"))


        # 获取当前运行的进程
    for process in c.Win32_Process():
        print process.ProcessId, process.Name


def main():
    sys_version()
    # cpu_mem()
    # disk()
    # network()
    # cpu_use()


if __name__ == '__main__':
    main()
    print platform.system()
    print platform.release()
    print platform.version()
    print platform.platform()
    print platform.machine()
import socket
hostname = socket.gethostname()
print hostname
import requests


def checkip(ip):
    URL = 'http://ip.taobao.com/service/getIpInfo.php'
    try:
        r = requests.get(URL, params=ip, timeout=3)
    except requests.RequestException as e:
        print(e)
    else:
        json_data = r.json()
        if json_data[u'code'] == 0:
            print '所在国家： ' + json_data[u'data'][u'country'].encode('utf-8')
            print '所在地区： ' + json_data[u'data'][u'area'].encode('utf-8')
            print '所在省份： ' + json_data[u'data'][u'region'].encode('utf-8')
            print '所在城市： ' + json_data[u'data'][u'city'].encode('utf-8')
            print '所属运营商：' + json_data[u'data'][u'isp'].encode('utf-8')
        else:
            print '查询失败,请稍后再试！'


ip = {'ip': '202.102.193.68'}
checkip(ip)


judge a process


def CheckProcExistByPN(process_name):
    try:
        WMI = win32com.client.GetObject('winmgmts:')
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    except Exception, e:
        print process_name + "error : ", e;
    if len(processCodeCov) > 0:
        print process_name + " exist";
        return 1
    else:
        print process_name + " is not exist";
        return 0


if __name__ == '__main__':
    CheckProcExistByPN('notepad.exe')

author: orangleliu date: 2014-11-12
python2.7.x ip_scaner.py

'''''
不同平台，实现对所在内网端的ip扫描

有时候需要知道所在局域网的有效ip，但是又不想找特定的工具来扫描。
使用方法 python ip_scaner.py 192.168.1.1
(会扫描192.168.1.1-255的ip)
'''

import platform
import sys
import os
import time
import thread


def get_os():
    '''''
    get os 类型
    '''
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()

    flag = False
    for line in list(output):
        if not line:
            continue
        if str(line).upper().find("TTL") >= 0:
            flag = True
            break
    if flag:
        print "ip: %s is ok ***" % ip_str


def find_ip(ip_prefix):
    '''''
    给出当前的127.0.0 ，然后扫描整个段所有地址
    '''
    for i in range(1, 256):
        ip = '%s.%s' % (ip_prefix, i)
        thread.start_new_thread(ping_ip, (ip,))
        time.sleep(0.3)


if __name__ == "__main__":
    print "start time %s" % time.ctime()
    commandargs = sys.argv[1:]
    args = "".join(commandargs)

    ip_prefix = '.'.join(args.split('.')[:-1])
    find_ip(ip_prefix)
    print "end time %s" % time.ctime()