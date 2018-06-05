#-*- coding: utf-8 -*-
import wmi
import time
import win32com
import requests
import socket
import os

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

if __name__ == '__main__':
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    cpu_mem()
    # cpu_use()
    disk()
    CheckProcExistByPN('chrome.exe')
    ip = {'ip': '116.226.42.176'}
    checkip(ip)
