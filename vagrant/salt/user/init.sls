vagrant-virtualenv-path:
  file.append:
    - name: {{ pillar['HOME'] }}/.bashrc
    - text: export WORKON_HOME={{ pillar['HOME'] }}/.virtualenvs
    - require:
      - pkg: packages

vagrant-virtualenv-bash-source:
  file.append:
    - name: {{ pillar['HOME'] }}/.bashrc
    - text: . /etc/bash_completion.d/virtualenvwrapper
    - require:
      - pkg: packages
      - file: vagrant-virtualenv-path

vagrant-bash-profile:
  file.managed:
    - name: {{ pillar['HOME'] }}/.bash_profile
    - source: salt://user/vagrant-bash-profile
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}
