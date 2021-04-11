<h1 align="center">
  <br>Aliddns<br>
</h1>

<h5 align="center">阿里DDNS 的刷新脚本,可用于动态ip环境下的定时任务或手动指定刷新.</h5>



## 准备
### 1.准备环境
```
pip3 install pyyaml 

// 安装阿里云支持库
//   如果您使用Python 2.x，执行以下命令
//pip install aliyun-python-sdk-core
//   如果您使用Python 3.x，执行以下命令
pip install aliyun-python-sdk-core-v3
   
pip install aliyun-python-sdk-alidns
```

### 2.配置文件
```
# 阿里云更新域名解析文档
# https://help.aliyun.com/document_detail/29776.html
# https://help.aliyun.com/document_detail/29774.html


# 阿里云信息，从阿里云获取填写即可
AliyunData:
  # 阿里云的AccessKey_ID , Access_Key_Secret , region_id
  # 获取方法，参考文档: https://help.aliyun.com/knowledge_detail/38738.html
  AccessKey_ID: 'AccessKey'
  Access_Key_Secret: 'Secret'
  region_id: "cn-hangzhou"

# DNS解析信息
UserData:
  # 需要修改的域名
  DomainName: '需要修改的域名'
  # 解析的主机
  RR: '需要修改的主机'
  # 解析的记录
  DomainType: '需要修改的记录类型'
  # 解析更新的值，如果填写 Auto_Lines ,则从命令行获取,如果命令行为空则去当前设备的外网ip进行更新
  UpdateDomain: 'Auto_Lines'
  #UpdateDomain: '127.0.0.1'
```
