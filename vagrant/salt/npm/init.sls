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
    - cwd: /home/vagrant
    - user: vagrant
    - creates: /home/vagrant/casperjs

fuel-web-npm-install:
  cmd.run:
    - name: npm install
    - cwd: /sources/fuel-web/nailgun
    - require:
      #- git: fuel-web-source
      - cmd: gulp

fuel-web-gulp-bower:
  cmd.run:
    - name: gulp bower
    - cwd: /sources/fuel-web/nailgun
    - require:
      - cmd: fuel-web-npm-install

fuel-web-owner:
  file.directory:
    - name: /sources/fuel-web
    - user: vagrant
    - group: vagrant
    - recurse:
      - user
      - group
    - require:
      - cmd: fuel-web-gulp-bower
