nailgun-log-directory:
  file.directory:
    - name: /var/log/nailgun
    - makedirs: True
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}

remote-log-directory:
  file.directory:
    - name: /var/log/remote
    - makedirs: True
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}

nailgun-user:
  postgres_user.present:
    - name: nailgun
    - createdb: True
    - createroles: True
    - superuser: True
    - password: nailgun
    - require:
      - pkg: packages

nailgun-db:
  postgres_database.present:
    - name: nailgun
    - db_user: nailgun
    - db_password: nailgun
    - require:
      - pkg: packages
      - postgres_user: nailgun-user

/usr/bin/nailgun_clean_db.sh:
  file.managed:
    - source: salt://nailgun/nailgun_clean_db.sh
    - mode: 0777

create-database:
  cmd.run:
    - name: /usr/bin/nailgun_clean_db.sh
    - user: vagrant
    - require:
      - file: /usr/bin/nailgun_clean_db.sh

raemon-source:
  git.latest:
    - name: https://github.com/nulayer/raemon.git
    - rev: b78eaae57c8e836b8018386dd96527b8d9971acc
    - target: /home/vagrant/raemon
    - user: vagrant
    - group: vagrant
    - unless: ls /home/vagrant/raemon

rvm-keys:
  cmd.run:
    - name: gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3

get-rvm-io:
  cmd.script:
    - name: salt://nailgun/get-rvm-io.sh stable
    - source: salt://nailgun/get-rvm-io.sh
    - shell: /bin/bash
    - unless: ls /usr/local/rvm
    - require:
      - cmd: rvm-keys

packages-ruby-2.1:
  cmd.run:
    - name: source /etc/profile.d/rvm.sh && rvm install 2.1
    - unless: ls /usr/local/rvm/rubies/ruby-2.1.5/bin/ruby
    - require:
      - cmd: get-rvm-io

raemon-gem:
  cmd.run:
    - name: source /etc/profile.d/rvm.sh && rvm user gemsets && rvm gemset create astute && rvm use 2.1@astute && gem build raemon.gemspec && gem install raemon-0.3.0.gem && gem install bundler
    - user: vagrant
    - group: vagrant
    - cwd: /home/vagrant/raemon
    - unless: /home/vagrant/raemon/raemon-0.3.0.gem
    - require:
      - cmd: packages-ruby-2.1
      - git: raemon-source

python-fuel-command:
  cmd.run:
    - name: python setup.py develop
    - cwd: /sources/python-fuelclient

python-fuel-command-config-dir:
  file.directory:
    - name: /etc/fuel/client
    - makedirs: True

python-fuel-command-config:
  file.managed:
    - name: /etc/fuel/client/config.yaml
    - source: salt://nailgun/client-config.yaml
    - require:
      - file: python-fuel-command-config-dir
