vagrant-virtualenv-path:
  file.append:
    - name: /home/vagrant/.bashrc
    - text: export WORKON_HOME=/home/vagrant/.virtualenvs
    - require:
      - pkg: packages

vagrant-virtualenv-bash-source:
  file.append:
    - name: /home/vagrant/.bashrc
    - text: . /etc/bash_completion.d/virtualenvwrapper
    - require:
      - pkg: packages
      - file: vagrant-virtualenv-path

/home/vagrant/.bash_profile:
  file.managed:
    - source: salt://user/vagrant-bash-profile
    - user: vagrant
    - group: vagrant
