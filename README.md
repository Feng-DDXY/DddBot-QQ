# DddBot-QQ

基于 Python、NapCat 和 OneBot 11 的《洛克王国：世界》QQ 群机器人

## 目前功能：

* 定时在指定 QQ 群中 @小呱呱，查询远行商人信息（单纯不想走远行商人接口）
* 支持多个 QQ 群
* 群聊命令：`/ping`、`/状态`、`/帮助`（其实毫无作用）
*

## 技术栈

* Python 3.12
* Flask + Waitress
* NapCat / OneBot 11
* Docker
* Ubuntu Linux

##

使用：

1. 部署 NapCat 并登录 QQ。

2. 配置 OneBot HTTP Server 和 HTTP Client

3.

4. 需要的依赖：

   `python3 -m pip install flask waitress`

5. 其中，将 `config.example.json` 复制为 `config.json`，填写自己的群号（可以多个）、QQ 号及 Access Token（NapCat后台的）。

6. 启动回复程序：

   `python3 reply_bot.py`

7. 在测试群发送 `/ping`，检查是否收到回复。

 当前 `reply_bot.py` 监听的 Docker 网桥 IP 为 `172.18.0.1`，不同服务器的 Docker 网桥地址可能不同，需要根据实际环境调整。

我自己这边的NapCat HTTP Client 的事件地址为 `http://172.18.0.1:8080/event`

定时查询：通过 Linux cron 执行 `send_merchant.py`。

##

## 项目状态

v0.1.0 — 纯自己测试玩的版本，如果需要的话可以联系我，我直接把机器人拉进去

