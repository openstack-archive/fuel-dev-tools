packages-initial:
  pkg.latest:
    - pkgs:
      - curl

pkgrepos:
  cmd.run:
    - name: curl -sL https://deb.nodesource.com/setup | bash -
    - user: root
    - group: root
    - unless: ls /etc/apt/sources.list.d/nodesource.list
    - shell: /bin/bash
    - require:
      - pkg: packages-initial

packages:
  pkg.latest:
    - pkgs:
      - bundler
      - build-essential
      - debootstrap
      - extlinux
      - genisoimage
      - git
      - htop
      - imagemagick
      - isomd5sum
      - kpartx
      - libmysqlclient-dev
      - libvirt-bin
      - make
      - nginx
      - nodejs
      - postgresql
      - postgresql-server-dev-9.3
      - python-dev
      - python-ipaddr
      - python-paramiko
      - python-pip
      - python-nose
      - python-software-properties
      - python-virtualenv
      - python-yaml
      - rsync
      - ruby2.0
      - ruby-dev
      - rubygems-integration
      - screen
      - silversearcher-ag
      - software-properties-common
      - tmux
      - unzip
      - vim
      - vim-nox
      - virtualenvwrapper
      - yum
      - yum-utils
    - require:
      - cmd: pkgrepos

py26-fake-interpreter:
  file.symlink:
    - name: /usr/bin/python2.6
    - target: /usr/bin/python2.7

gitconfig:
  file.managed:
    - name: {{ pillar['HOME'] }}/.gitconfig
    - source: salt://packages/gitconfig
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}

/etc/tmux.conf:
  file.managed:
    - source: salt://packages/tmux.conf
    - require:
      - pkg: packages
