#!/bin/bash

. /etc/bash_completion.d/virtualenvwrapper

workon fuel

pip install /sources/fuel-web/shotgun  # this fuel project is listed in setup.py requirements
pip install -r /sources/fuel-web/nailgun/requirements.txt
pip install -r /sources/fuel-web/nailgun/test-requirements.txt

pip install tox
pip install ipython
pip install pudb
