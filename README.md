# Simple Syslog Server

![python version](https://img.shields.io/badge/Python-3.12-blue)

A very simple fast syslog server with a web interface.

## Linux Setup Instructions

### Install Packages:

```
git clone https://github.com/voun7/Simple_Syslog_Server.git
```

```commandline
cd Simple_Syslog_Server
```

```commandline
python3 -m venv venv
```

```commandline
source venv/bin/activate
```

```commandline
pip install -r requirements.txt
```

### Setup a Systemd Service:

Add the contents of `Simple_Syslog_Server.service` into the editor

```commandline
nano /etc/systemd/system/Simple_Syslog_Server.service
```

Run the following commands to finish setup

```commandline
systemctl daemon-reload
```

```commandline
systemctl start Simple_Syslog_Server
```

```commandline
systemctl status Simple_Syslog_Server
```

```commandline
systemctl enable Simple_Syslog_Server
```


## Usage

Send logs to server using ip address of server on port `1514`.


Access logs on server using link below.
```
http://server_ip_address:9000
```
