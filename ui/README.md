# About
The WMI-UI is a User Interface for Controlling the [clevo-xsm-wmi](https://bitbucket.org/tuxedocomputers/clevo-xsm-wmi) over the sysfs interface.

# Requirements
* Python 3
* pip3
* python3-tk
* [CEF Python](https://github.com/cztomczak/cefpython) Version 57.0
* [clevo-xsm-wmi](https://bitbucket.org/tuxedocomputers/clevo-xsm-wmi)

# Installation

For only install the wmi-ui run 
```shell
sudo make install
```

For the install the wmi-ui under ubuntu with the dependencies (pip3, python3-tk, cefpython3) run
```shell
sudo make installdependencies
sudo make install
```

After this step, can you start the application over the terminal with 
```shell
sudo wmi-ui
```

# Start

1. Make sure the clevo-xsm-wmi kernel module is running
2. Start the application with starter.py or over wmi-ui

```shell
sudo python3 ./src/starter.py
```

```shell
sudo wmi-ui
```
