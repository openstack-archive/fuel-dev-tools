#!/bin/bash

. /etc/bash_completion.d/virtualenvwrapper

mkvirtualenv fuel
workon fuel

pip install /sources/fuel-web/shotgun  # this fuel project is listed in setup.py requirements
pip install -r /sources/fuel-web/nailgun/test-requirements.txt

pip install ipython pudb

pip install tox
