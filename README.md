参考rabbitmq的脚本
https://github.com/iambocai/falcon-monit-scripts/tree/master/rabbitmq

open-falcon activeMQ监控脚本
================================

系统需求
--------------------------------
操作系统：Linux
Python >= 2.6
python-simplejson

主要逻辑
--------------------------------
从activeMQ-server的api接口(http://IP:8161/admin/xml/queues.jsp)读取相关数据，然后推送到falco-agent


汇报字段
--------------------------------
| key |  tag | type | note |
|-----|------|------|------|
|activemq.size|queuename(Queue名字)|GAUGE| |
|activemq.enqueuecount|queuename(Queue名字)|GAUGE| |
|activemq.dequeuecount|queuename(Queue名字)|GAUGE| |
|activemq.consumercount|queuename(Queue名字)|GAUGE| |


使用方法
--------------------------------
1. 根据实际部署情况，修改16行的activeMQ-server管理端口和登录用户名密码
2. 将脚本加入crontab即可
*/1 * * * * cd /path/to/activemq-mon &&python activemq.py


授权类型：MIT
