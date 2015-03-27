fuel-virtualenv-dir:
  file.directory:
    - name: /home/vagrant/.virtualenvs
    - user: vagrant
    - group: vagrant
    - makedirs: True

fuel-virtualenv:
  virtualenv.managed:
    - name: /home/vagrant/.virtualenvs/fuel
    - user: vagrant
    - group: vagrant
    - require:
      - file: fuel-virtualenv-dir

fuel-virtualenv-requirements:
  cmd.script:
    - name: salt://virtualenv/virtualenv-requirements.sh
    - shell: /bin/bash
    - user: vagrant
    - group: vagrant
    - cwd: /home/vagrant
    #- creates: /home/vagrant/.virtualenvs/fuel
    - require:
      - virtualenv: fuel-virtualenv

/var/log/nailgun:
  file.directory:
    - makedirs: True
    - user: vagrant
    - group: vagrant

/var/log/remote:
  file.directory:
    - makedirs: True
    - user: vagrant
    - group: vagrant

/home/vagrant/.virtualenvs/fuel/bin/postactivate:
  file.managed:
    - source: salt://virtualenv/postactivate
    - user: vagrant
    - group: vagrant
    - mode: 744
    - require:
      - virtualenv: fuel-virtualenv
