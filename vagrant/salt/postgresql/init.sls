postgresql-pg_hba:
  file.managed:
    - name: /etc/postgresql/9.3/main/pg_hba.conf
    - source: salt://postgresql/pg_hba.conf
    - require:
      - pkg: packages

postgresql-service:
  service:
    - running
    - name: postgresql
    - enable: True
    - reload: True
    - watch:
      - file: /etc/postgresql/9.3/main/pg_hba.conf
