# 强烈推荐使用功能更全的【✨多合一动态检测与推送✨】：https://github.com/nfe-w/aio-dynamic-push

# weibo_dynamic_push

## 声明:

- 本仓库发布的`weibo_dynamic_push`项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途
- `nfe-w` 对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害
- 以任何方式查看此项目的人或直接或间接使用`weibo_dynamic_push`项目的任何脚本的使用者都应仔细阅读此声明
- `nfe-w` 保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或`weibo_dynamic_push`项目，则视为已接受此免责声明
- 本项目遵循`MIT LICENSE`协议，如果本声明与`MIT LICENSE`协议有冲突之处，以本声明为准

## 简介

定时检测指定博主的动态，如果发生变化进行推送

## Docker（推荐）

[![](https://img.shields.io/badge/DockerHub-nfew/weibo__dynamic__push-367AC7?style=flat-square&logo=Docker&logoColor=white)](https://hub.docker.com/r/nfew/weibo_dynamic_push)

```sh
# 启动容器
docker run -d -v ~/config_weibo.ini:/mnt/config_weibo.ini --name weibo_dynamic_push nfew/weibo_dynamic_push:latest
```

## 运行环境

- [Python 3](https://www.python.org/)

## 使用教程

#### 1. 填写config_weibo.ini配置信息

(1)`config`下的参数

- `uid_list`为需要扫描的博主uid列表，使用英文逗号分隔，必填
- `intervals_second`为扫描间隔秒数，不建议过于频繁，必填
- `begin_time`为扫描开始时间，非必填，不支持跨日期
- `end_time`为扫描停止时间，非必填，不支持跨日期

(2)`proxy_pool`下的参数

- `enable`是否启用ip池
- `proxy_pool_url`为ip池地址，如果启用ip池，则必填，参考 https://github.com/jhao104/proxy_pool

(3)`push_serverChan`下的参数

- `enable`是否启用serverChan推送
- `serverChan_SCKEY`如果启用该推送，则必填，参考 http://sc.ftqq.com/3.version

(4)`push_serverChan_turbo`下的参数

- `enable`是否启用serverChan_Turbo推送
- `serverChan_SendKey`如果启用该推送，则必填，参考 https://sct.ftqq.com

(5)`push_wechat`下的参数

- `enable`是否启用微信推送
- `corp_id`企业id，如果启用该推送，则必填
- `agent_id`应用id，如果启用该推送，则必填
- `corp_secret`应用Secret，如果启用该推送，则必填

(6)`push_dingtalk`下的参数

- `enable`是否启用钉钉bot推送
- `access_token`机器人access_token，如果启用该推送，则必填

#### 2.安装第三方库

`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

#### 3.启动脚本

`nohup python3 -u main.py >& weibo_dynamic_push.log &`
