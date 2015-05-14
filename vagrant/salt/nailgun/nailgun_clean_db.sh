#!/bin/bash
#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

sudo su postgres -c "psql -c \"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = 'nailgun';\""
sudo su postgres -c "psql -c \"DROP DATABASE nailgun;\""
sudo su postgres -c "psql -c \"CREATE DATABASE nailgun WITH OWNER nailgun;\""

. /etc/bash_completion.d/virtualenvwrapper

workon fuel

cd /sources/fuel-web/nailgun

./manage.py syncdb
./manage.py loaddefault # It loads all basic fixtures listed in settings.yaml
./manage.py loadfakedeploymenttasks  # Loads fake deployment tasks
./manage.py loaddata nailgun/fixtures/sample_environment.json  # Loads fake nodes
