#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import yaml
import sys
from datetime import datetime
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

now_ip = '';

def GetNowIp():
    get_ip_method = os.popen('curl -s http://ddns.oray.com/checkip')
    get_ip_responses = get_ip_method.readlines()[0]
    get_ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
    get_ip_value = get_ip_pattern.findall(get_ip_responses)[0]
    #get_ip_value = os.popen('curl -s icanhazip.com').readlines()[0]
    return get_ip_value

def AliAccessKey(id,Secret,region):
    try:
        client = AcsClient(id, Secret, region)
        return client
    except Exception as e:
        print("验证aliyun key失败")
        print(e)
        sys.exit(-1)

def read_yaml(filename):
    try:
        yaml_file = open(filename,"rb")
        yaml_data = yaml.safe_load(yaml_file)
        yaml_file.close()
        return yaml_data
    except Exception as e:
        print("读取配置文件错误")
        print(e)
        sys.exit(-1)

def write_to_file():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #current_script_path = sys.argv[0]
    #print current_script_path
    # 绝对路径获取
    current_script_path = os.path.abspath(sys.argv[0])
    current_script_path = os.path.dirname(current_script_path)
    log_file = current_script_path + '/' + 'aliyun_ddns.log'
    #print log_file
    write = open(log_file, 'a')
    write.write(time_now + ' ' + str(rc_value)  + ' ' + str(rc_record_id)+ '\n')
    write.close()
    return

def GetDNSRecord(yaml_data,client,DomainName):
    try:
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))

        for RecordId in json_data['DomainRecords']['Record']:
            if yaml_data['UserData']['RR'] == RecordId['RR']:
                return RecordId

    except Exception as e:
        print("获取Record失败")
        print(e)
        sys.exit(-1)

def UpdateDomainRecord(client,yaml_data,Record):
    try:
        
        if 'Auto_Lines' == yaml_data['UserData']['UpdateDomain']:
            args = len(sys.argv)
            if args > 1 : 
                DomainValue = sys.argv[1]
            else :
                DomainValue = now_ip
        else :
            DomainValue = yaml_data['UserData']['UpdateDomain']

        if Record['Value'] == DomainValue :
            print('新旧IP地址一致,无需更新.')
            sys.exit(-1)    

        request = UpdateDomainRecordRequest()   
        request.set_accept_format('json')
        request.set_Value(DomainValue)
        request.set_Type(yaml_data['UserData']['DomainType'])
        request.set_RR(yaml_data['UserData']['RR'])
        request.set_RecordId(Record['RecordId'])
        response = client.do_action_with_exception(request)

        #如果是泛解析则追加@的解析
        if '*' == yaml_data['UserData']['RR']:
            request = UpdateDomainRecordRequest()   
            request.set_accept_format('json')
            request.set_Value(DomainValue)
            request.set_Type(yaml_data['UserData']['DomainType'])
            request.set_RR('@')
            request.set_RecordId(Record['RecordId'])
            response = client.do_action_with_exception(request)

        print("更新域名解析成功")
        print("域名:" + yaml_data['UserData']['DomainName'] + " 主机:" + yaml_data['UserData']['RR'] + " 记录类型:" +  yaml_data['UserData']['DomainType'] + " 记录值:" +  DomainValue)
    except Exception as e:
        print("更新域名解析失败")
        print(e)


def main():
    yaml_data = read_yaml('./config.yaml')
    global now_ip
    now_ip = GetNowIp()
    client = AliAccessKey(yaml_data['AliyunData']['AccessKey_ID'],yaml_data['AliyunData']['Access_Key_Secret'],yaml_data['AliyunData']['region_id'])
    Record = GetDNSRecord(yaml_data,client,yaml_data['UserData']['DomainName'])
    UpdateDomainRecord(client,yaml_data,Record)

if __name__ == "__main__" :
    main()