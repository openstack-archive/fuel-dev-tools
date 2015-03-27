fuel-virtualenv-dir:
  file.directory:
    - name: {{ pillar['HOME'] }}/.virtualenvs
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}
    - makedirs: True

fuel-virtualenv:
  virtualenv.managed:
    - name: {{ pillar['HOME'] }}/.virtualenvs/fuel
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}
    - require:
      - file: fuel-virtualenv-dir

fuel-virtualenv-requirements:
  cmd.script:
    - name: salt://virtualenv/virtualenv-requirements.sh
    - shell: /bin/bash
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}
    - cwd: {{ pillar['HOME'] }}
    #- creates: {{ pillar['HOME'] }}/.virtualenvs/fuel
    - require:
      - virtualenv: fuel-virtualenv

fuel-virtualenv-postactivate-script:
  file.managed:
    - name: {{ pillar['HOME'] }}/.virtualenvs/fuel/bin/postactivate
    - source: salt://virtualenv/postactivate
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}
    - mode: 744
    - require:
      - virtualenv: fuel-virtualenv
