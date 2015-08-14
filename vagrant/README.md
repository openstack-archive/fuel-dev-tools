============================
Fuel development Vagrant box
============================

This is a definition of a Vagrant box tailored for development of Mirantis Fuel.
Configuration is done using [SaltStack](http://saltstack.com/).

Usage
-----

Clone and `cd` into this repo then run
```
vagrant up
```
to start the Vagrant box (with the Virtualbox provider) or
```
vagrant up --provider=libvirt
```
to start with the `libvirt` provider.

Then run
```
vagrant ssh
sudo su
salt-call state.highstate --local
```
to SSH into the machine and initially set up the environment. Then on the virtual machine as user `vagrant` you can do
```
workon fuel
```
to activate the Python virtualenv. To start the server type
```
/sources/fuel-web/nailgun/manage.py run --fake-tasks
```
and point your browser to [http://localhost:8200](http://localhost:8200) -- username/password for the test env is `admin`/`admin`.

Sometimes it might be necessary to repopulate the DB with fixtures, to do this just type (`dropdb` might be needed before):
```
./manage.py syncdb
./manage.py loaddefault # It loads all basic fixtures listed in settings.yaml
./manage.py loaddata nailgun/fixtures/sample_environment.json  # Loads fake nodes
```

As a shortut, a script `nailgun_clean_db.sh` is provided to reinitialize the database using the above commands.

To run tests:
```
cd /sources/fuel-web
./run_tests.sh
```

The `sources` directory is mounted under `/sources` on the Vagrant machine using Rsync for better performance
(otherwise tests run incredibly slow). If you want Vagrant to automatically rsync your local directory to the virtualmachine run
```
vagrant rsync-auto
```

Note that this is a one-way sync, i.e. from your local machine to the virtual machine, not the other way around.

There is also the `/vagrant/sources` folder where `sources` are mounted too, but using the standard VirtualBox
Synchronized Folders which is extremely slow.

For more information see http://docs.mirantis.com/fuel-dev/develop/nailgun/development/env.html and
http://docs.mirantis.com/fuel-dev/develop/env.html

tmux
----
[tmux](http://tmux.sourceforge.net/) is installed by default. Each tmux window's output is logged
to a separate file for easier inspection of history. The file's name can be fetched in current
active window from the `TMUX_LOG_FILE` variable (see `/home/vagrant/.bash_profile`).

Astute
----
To run Ruby tests for `fuel-astute`:

```
cd /sources/fuel-astute
rvm gemset use astute
./run_tests.sh
```

TODO
----
* eliminate the need for running `rsync-auto` and instead install the `rsync` service inside the Vagrant box
  that synchronizes `/vagrant/sources` into `/sources`
* add link (and Jenkins job?) to pre-generated Vagrant box
