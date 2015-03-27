#!/bin/bash

cd /home/vagrant
git clone git://github.com/n1k0/casperjs.git
cd casperjs
git checkout tags/1.0.0-RC4
sudo ln -sf `pwd`/bin/casperjs /usr/local/bin/casperjs
