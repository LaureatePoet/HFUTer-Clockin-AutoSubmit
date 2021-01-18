# HFUTer-Clockin-AutoSubmit（适用于HFUTer的自动打卡）
- [HFUTer-Clockin-AutoSubmit](#HFUTer-Clockin-AutoSubmit（适用于HFUTer的自动打卡）)
  - [简介](#简介)
  - [使用方法](#使用方法)
    - [本地](#本地)
    - [服务器](#服务器)
    - [Github Actions](#Github-Actions)
  - [其他](#其他)
    - [批量处理](#批量处理)
    - [项目来源](#项目来源)
    - [声明](#声明)

## 简介
因我校每日健康打卡由今日校园迁移至校内系统，原[自动打卡](https://gitee.com/Finch1/FuckDailyCP)项目已不支持，本着**交流学习**的目的分享此项目。
## 使用方法
* 学号: 即为自己的学号
* 密码: 学校新系统对应的密码
* 地址: 你想填写的地址，理论上任何文本都可以，譬如：**查令十字路84号**
### 本地
CMD/Terminal 切换到项目文件夹，输入并执行:
```
python3 HFUTclockin.py 学号 密码 地址
```
本地执行在不设置定时任务的情况下，只能每天手动执行。
关于定时任务，对于**Windows**用户，可以简单编写`ps1`（powershell）脚本，脚本内容即为`python HFUTclockin.py 学号 密码 地址`，并设置*定时任务*（具体Google）执行该脚本；对于Linux/Mac OS用户可参考服务器食用方法。

### 服务器
服务器可以通过使用`cron`来设置定时任务。

在Linux中可以使用`crontab -e`设置定时任务让程序每天自动打卡
```
30 17,18 * * * python3 HFUTclockin.py 学号 密码 定位地址
```
### Github Actions
Fork本项目，点击`Settings`，增加`ACCOUNT`、`PASSWORD`、`ADDRESS` 3个Secrets，分别对应你的账号、密码、定位地址。
设置完之后 **Star** 该仓库，这样就设置好了。

>一定要**Star**自己的这个仓库，否则不执行！

>一定要**Star**自己的这个仓库，否则不执行！

>一定要**Star**自己的这个仓库，否则不执行！

> *Github Actions*的配置文件在`.github/workflows/HFUT-Auto-Clockin.yml`，默认设置的打开时间是每天14/15时0/30分（UTC+8）。
如果需要个性化配置（执行时间，执行条件等等），需编辑对应配置文件`.yml`

## 其他
### 批量处理
参考[项目来源](#项目来源)中的[Campus-daily-crack](https://github.com/moddemod/Campus-daily-crack)，只需要编辑好`info.txt`，即可实现；或者采用本项目`批量打卡`文件夹，编辑好`info.txt`，运行`clockins.py`即可。

### 项目来源
* [Campus-daily-crack](https://github.com/moddemod/Campus-daily-crack)

* [FuckDailyCP](https://gitee.com/Finch1/FuckDailyCP)

### 声明
此项目仅用来学习交流使用，如作他用所承受的法律责任一概与作者无关（下载使用即代表你同意上述观点），请同学们在下载/使用后24小时内删除。