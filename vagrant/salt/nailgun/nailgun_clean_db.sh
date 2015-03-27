#!/bin/bash

sudo su postgres -c "psql -c \"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = 'nailgun';\""
sudo su postgres -c "psql -c \"DROP DATABASE nailgun;\""
sudo su postgres -c "psql -c \"CREATE DATABASE nailgun WITH OWNER nailgun;\""

. /etc/bash_completion.d/virtualenvwrapper

workon fuel

cd /sources/fuel-web/nailgun

./manage.py syncdb
./manage.py loaddefault # It loads all basic fixtures listed in settings.yaml
./manage.py loaddata nailgun/fixtures/sample_environment.json  # Loads fake nodes
