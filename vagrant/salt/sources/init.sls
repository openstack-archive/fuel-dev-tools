sources-directory:
  file.directory:
    - name: /vagrant/sources
    - makedirs: true
    - require:
      - pkg: packages

fuel-astute-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-astute
    - target: /vagrant/sources/fuel-astute
    - unless: ls /vagrant/sources/fuel-astute
    - require:
      - file: sources-directory

fuel-dev-tools:
  git.latest:
    - name: https://github.com/stackforge/fuel-dev-tools
    - target: /vagrant/sources/fuel-dev-tools
    - unless: ls /vagrant/sources/fuel-dev-tools
    - require:
      - file: sources-directory

fuel-devops-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-devops
    - target: /vagrant/sources/fuel-devops
    - unless: ls /vagrant/sources/fuel-devops
    - require:
      - file: sources-directory

fuel-docs-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-docs
    - target: /vagrant/sources/fuel-docs
    - unless: ls /vagrant/sources/fuel-docs
    - require:
      - file: sources-directory

fuel-library-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-library
    - target: /vagrant/sources/fuel-library
    - unless: ls /vagrant/sources/fuel-library
    - require:
      - file: sources-directory

fuel-main-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-main
    - target: /vagrant/sources/fuel-main
    - unless: ls /vagrant/sources/fuel-main
    - require:
      - file: sources-directory

fuel-plugins-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-plugins
    - target: /vagrant/sources/fuel-plugins
    - unless: ls /vagrant/sources/fuel-plugins
    - require:
      - file: sources-directory

fuel-ostf-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-ostf
    - target: /vagrant/sources/fuel-ostf
    - unless: ls /vagrant/sources/fuel-ostf
    - require:
      - file: sources-directory

fuel-specs-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-specs
    - target: /vagrant/sources/fuel-specs
    - unless: ls /vagrant/sources/fuel-specs
    - require:
      - file: sources-directory

fuel-web-source:
  git.latest:
    - name: https://github.com/stackforge/fuel-web
    - target: /vagrant/sources/fuel-web
    - unless: ls /vagrant/sources/fuel-web
    - require:
      - file: sources-directory

python-fuelclient:
  git.latest:
    - name: https://github.com/stackforge/python-fuelclient
    - target: /vagrant/sources/python-fuelclient
    - unless: ls /vagrant/sources/python-fuelclient
    - require:
      - file: sources-directory

rsync-sources:
  cmd.run:
    - name: rsync -az /vagrant/sources/ /sources
    - creates: /sources/fuel-web  # creates more but I think Salt doesn't support this
    - require:
      - git: fuel-astute-source
      - git: fuel-docs-source
      - git: fuel-dev-tools
      - git: fuel-devops-source
      - git: fuel-library-source
      - git: fuel-main-source
      - git: fuel-ostf-source
      - git: fuel-plugins-source
      - git: fuel-specs-source
      - git: fuel-web-source
      - git: python-fuelclient
