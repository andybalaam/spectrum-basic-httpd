
all: build

build:
	docker build -t spectrum-basic-httpd .

run: build kill
	docker run -p 80:80 --name=spectrum-basic-httpd -it spectrum-basic-httpd

run-interactive: build kill
	docker run -p 80:80 --name=spectrum-basic-httpd -it spectrum-basic-httpd /bin/bash

execbash:
	docker exec -it spectrum-basic-httpd /bin/bash

kill:
	- docker kill spectrum-basic-httpd
	- docker rm spectrum-basic-httpd

