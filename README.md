Meerkat
================
A Pypi Server implements

build
---------------------------------------
```shell
sudo docker run --rm -v /home/benjamin/git/meerkat:/home/matrix  -v $(which docker):$(which docker) -v /var/run/docker.sock:/var/run/docker.sock docker.neg/matrix:0.0.2 /usr/local/bin/matrix.sh

```

deploy
-------------
```shell
sudo docker run --name meerkat -p 3141:8080 -dt meerkat:0.0.1 
```