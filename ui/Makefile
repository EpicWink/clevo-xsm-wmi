start:
	python ./src/starter.py

install:
	mkdir -p /usr/share/tuxedo/wmi-ui
	cp -r ./src/* /usr/share/tuxedo/wmi-ui
	cp ./wmi-ui /usr/bin/wmi-ui
	cp ./LICENSE.txt /usr/bin/LICENSE.txt
	cp ./README.md /usr/bin/README.md
	chmod +x /usr/bin/wmi-ui

installdependencies:
	apt-get install python3-pip python3-tk
	pip3 install cefpython3
