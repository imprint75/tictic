from contextlib import contextmanager as _contextmanager
from fabric.api import env, run, prefix
from fabric.context_managers import cd
from fabric.operations import sudo

env.directory = '/srv/tictic/'
env.activate = 'source /srv/tictic_env/bin/activate'


def vagrant():
    env.hosts = ['192.168.33.103']
    env.user = 'vagrant'
    env.password = 'vagrant'


def testing():
    with cd('/srv/'):
        run('ls')


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def run_tests():
    with virtualenv():
        run('./manage.py test')


def build():
    apt_update()
    add_apt_repo()
    apt_update()
    install_nginx()
    install_uwsgi()
    install_python()
    install_redis()
    install_git()
    link_confs('tictic', 'tictic')
    create_env('tictic_env')
    install_pip_reqs('tictic_env', 'tictic')
    restart()


def create_env(venv='test_env'):
    with cd('/srv/'):
        sudo('python3 -m venv {}'.format(venv))


def link_confs(dir_name='test', file_name='test'):
    sudo('rm /etc/nginx/sites-available/default')
    n1 = 'ln -s /srv/{0}/{0}/confs/{1} /etc/nginx/sites-available/default'
    sudo(n1.format(dir_name, file_name))
    u1 = 'ln -s /srv/{0}/{0}/confs/{1}.ini /etc/uwsgi/apps-available/{1}.ini'
    sudo(u1.format(dir_name, file_name))
    u2 = 'ln -s /etc/uwsgi/apps-available/{0}.ini ' \
         '/etc/uwsgi/apps-enabled/{0}.ini'
    sudo(u2.format(file_name))


def install_pip_reqs(venv='test_env', proj_dir='test'):
    command = '/srv/{}/bin/pip3 install --upgrade -r ' \
              '/srv/{}/requirements.txt'
    sudo(command.format(venv, proj_dir))


def restart():
    sudo('service nginx restart')
    sudo('service uwsgi restart')


### apt-get stuff ###


def add_apt_repo():
    sudo('apt-get install python3-software-properties')


def apt_update():
    sudo('apt-get update')


### ssh key stuff ###


### installs ###


def install_nginx():
    sudo('apt-get install nginx-full')


def install_redis():
    sudo('apt-get install redis-server')


def install_uwsgi():
    sudo('apt-get install uwsgi uwsgi-plugin-python3')


def install_python():
    sudo('apt-get install python3-setuptools')
    sudo('apt-get install python3.4-venv')
    sudo('apt-get install python3-dev')
    sudo('apt-get install build-essential')


def install_python_audio():
    # needed to pip install pyaudio
    sudo('apt-get install libjack-jackd2-dev portaudio19-dev')


def install_git():
    run('sudo apt-get install git')


def install_emacs24():
    apt_update()
    sudo('apt-get install emacs24 emacs24-el emacs24-common-non-dfsg')


def install_node():
    sudo('add-apt-repository ppa:chris-lea/node.js')
    sudo('apt-get update')
    sudo('apt-get install python g++ make nodejs')
