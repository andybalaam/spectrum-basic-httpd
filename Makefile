
all: build

build:
	docker build -t spectrum-basic-httpd .

run: build
	- docker kill spectrum-basic-httpd
	- docker rm spectrum-basic-httpd
	docker run -p 80:80 --name=spectrum-basic-httpd -it spectrum-basic-httpd

run-interactive: build
	- docker kill spectrum-basic-httpd
	- docker rm spectrum-basic-httpd
	docker run -p 80:80 --name=spectrum-basic-httpd -it spectrum-basic-httpd /bin/bash
