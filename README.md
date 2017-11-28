Prometheus stress tool
======================

Prom stress tool as a target for prom, which allows to
send messages to prom with tunable message speed and
message size.

Installation
------------

There are few ways to install and run stress tool: manually, via docker,
via installation script and via OpenStack. Let's describe all these ways.

### Manual installation

If you need just to run script, you need to install it with python:

```console
sudo python ./setup.py install
```

and then use tool cli:

```console
prom-stress-tool -h
```

### Docker container

If you want to run stress tool inside docker container, you need to build it:

```console
docker build . -t stress
```

set required env vars and then run it in target mode:

```console
docker run -p $PORT:$PORT \
           --name target \
           -e PORT=$PORT \
           -e COUNT=$COUNT \
           -e SPEED=$SPEED \
           -d stress
```

or run it in read mode:

```console
docker run --name reader -e READ=$READ \
                         -e PROMETHEUS=$PROMETHEUS \
                         -e JOB_NAME=$JOB_NAME \
                         -e INSTANCE=~\"^.+${PORT}$\" \
                         -e READ_PERIOD=$READ_PERIOD -d stress;
```

### Installation script

Installation script allows to deploy docker and run stress tools on it from
scratch. You need just download installation script:

```console
wget -qO- https://raw.githubusercontent.com/prazumovsky/prom-stress-tool/master/common-script > common-script.sh
chmod +x common-script.sh
```

and run it under root (don't forget to set all required env vars):

```console
sudo bash common-script.sh
```

### OpenStack installation

Also project has heat template inside, so you can just copy heat template to
OpenStack Heat and run it with required parameters.
