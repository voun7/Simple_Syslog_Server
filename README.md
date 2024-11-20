# Syslog Server

![python version](https://img.shields.io/badge/Python-3.12-blue)

Simple syslog server with web interface.

## Linux Setup Instructions

### Install Packages:

```
git clone https://github.com/voun7/Syslog_Server.git
```

```commandline
cd Syslog_Server
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

Add the contents of `Syslog_Server.service` into the editor

```commandline
nano /etc/systemd/system/Syslog_Server.service
```

Run the following commands to finish setup

```commandline
systemctl daemon-reload
```

```commandline
systemctl start Syslog_Server
```

```commandline
systemctl status Syslog_Server
```

```commandline
systemctl enable Syslog_Server
```
