gulp:
  cmd.run:
    - name: npm install -g gulp
    - unless: npm ls -g gulp

phantomjs:
  cmd.run:
    - name: npm install -g phantomjs
    - unless: npm ls -g phantomjs

casperjs:
  cmd.script:
    - name: salt://npm/casperjs.sh
    - cwd: {{ pillar['HOME'] }}
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}
    - creates: {{ pillar['HOME'] }}/casperjs

fuel-web-npm-install:
  cmd.run:
    - name: npm install
    - cwd: /sources/fuel-web/nailgun
    - require:
      #- git: fuel-web-source
      - cmd: gulp

fuel-web-gulp:
  cmd.run:
    - name: gulp
    - cwd: /sources/fuel-web/nailgun
    - require:
      - cmd: fuel-web-npm-install

fuel-web-owner:
  file.directory:
    - name: /sources/fuel-web
    - group: {{ pillar['GROUP'] }}
    - user: {{ pillar['USER'] }}
    - recurse:
      - user
      - group
    - require:
      - cmd: fuel-web-gulp-bower
