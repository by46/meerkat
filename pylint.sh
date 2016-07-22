#! /bin/sh

if [ ! -d "venv" ]; then
	virtualenv venv
fi
chmod +x ./venv/bin/activate

./venv/bin/activate
pip install --trusted-host scmesos06 -i http://scmesos06:3141/simple -r requirements.txt --cache-dir=/tmp/$JOB_NAME

pylint -f parseable meerkat | tee pylint.out