# Start Program

# Linux_CentOS 8 installing
## Robo3T install
- [Robo3T安裝參考網站](https://www.centlinux.com/2020/09/install-robo-3t-mongodb-gui-on-centos-8.html  )
- 最後執行robo3t時如果出現`robo3t: error while loading shared libraries: libcurl-gnutls.so.4: cannot open shared object file: No such file or directory`可參考此[連結](https://www.youtube.com/watch?v=_bae1v0o_JA&ab_channel=gotbletu)進行修復
- robo3t path usr/local/bin

## Mongodb server install(Use version 3.4.x)
- [Mongodb server (version3.4) 安裝參考網站](https://www.mongodb.com/docs/v3.4/tutorial/install-mongodb-enterprise-on-red-hat/)
- [Mongodb server administrator user setting](https://www.digitalocean.com/community/tutorials/how-to-secure-mongodb-on-centos-8#step-1-adding-an-administrative-user
)
- Mongodb server 開放使用IP連線
Terminal輸入`sudo nano /etc/mongod.conf`
![](https://i.imgur.com/v8s0PfU.png)
在127.0.0.1後加入,IP
更改後重啟mongo `sudo service mongod restart`

## Vscode Install
- [Vscode 安裝參考連結](https://code.visualstudio.com/docs/setup/linux)
- python library version
![](https://i.imgur.com/153salr.png)
![](https://i.imgur.com/Sje1voh.png)
![](https://i.imgur.com/gE5k3QC.png)
![](https://i.imgur.com/0eCpFXq.png)
![](https://i.imgur.com/mWsDZaJ.png)


## MongoDB datasource for WISE-PaaS Dashboard
- use terminal download programs
    `git clone https://github.com/eric248550/mongodb-grafana.git`
- use terminal install npm
    `sudo npm install`
    `sudo npm install -g forever`
- move to folder 
    `cd mongodb-grafana/server`
- run code
    `forever start mongodb-proxy.js`
- port listen on mongodb-grafana/server/config/default.json
- code [參考連結](https://github.com/eric248550/mongodb-grafana)
# Linux_CentOS 8 Run Program
## Auto start
### Controller 248, 289
- Python program path:
  - `/home/apiuser/Runcode/test/run_file.py`
- Service path:
  - `/etc/systemd/system/run.service`
- Edit service: 
    - `cd /etc/systemd/system `
    - `sudo nano run.service`
- Start service:
     - `sudo systemctl start run.service`
- Check service status:
     - `sudo systemctl status run.service`
- Data 
    - DB: AP, Client
    - Collection:Controller4
### Map sdk
- Python program path:
  - `/home/apiuser/Runcode/test/call_file_map.py`
- Service path:
  - `/etc/systemd/system/sdk.service`
- Edit service: 
    - `cd /etc/systemd/system `
    - `sudo nano sdk.service`
- Start service:
     - `sudo systemctl start sdk.service`
- Check service status:
     - `sudo systemctl status sdk.service`
- Data 
    - DB: AP
    - Collection:Controller4

## Manually start 
### MongoDB plugin for Grafana
- JS program path
  -  `mongodb-grafana/server`
- Start api at background
  - `forever start mongodb-proxy.js`
- 備註:server listens on `http://localhost:port` port 會根據`mongodb-grafana/server/config/default.json`
    ![](https://i.imgur.com/G3INcEW.png)
