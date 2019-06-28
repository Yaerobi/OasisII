#!/bin/sh

echo "start compile processing"

echo "installing venv"
python3.7 -m venv venv 

. ./venv/bin/activate

echo "installing requirements"
pip install -r requirements.txt

echo "cythonization"
python setup.py build_ext -i

echo "pyinstaller"
cd OasisII && pyinstaller -r ImageConverter.*.so  -F controller.py


