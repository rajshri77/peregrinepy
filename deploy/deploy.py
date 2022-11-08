"""
py_mina deployfile
"""


from py_mina import *
from py_mina.subtasks import (
    git_clone, 
    create_shared_paths, 
    link_shared_paths, 
    rollback_release, 
    force_unlock,
)


# Settings - global


set('verbose', True)
set('keep_releases', 5)
#set('sudo_on_chown', True)
#set('sudo_on_chmod', True)
#set('sudo_on_cleanup_releases', True)
#set('ask_unlock_if_locked', True)


# Settings - remote server connection


set('user', 'root')
set('hosts', ['localhost'])


# Settings - application


set('deploy_to', '/var/www/example_application')
set('repository', 'https://github.com/py-mina-deploy/dummy-web-for-deployment')
set('branch', 'master')


# Settings - shared [PUBLIC] files/dirs (application configs, assets, storage, etc.)


set('shared_dirs', [])
set('shared_files', [])


# Settings - explicit owner of [PUBLIC] shared files/dirs


#set('owner_user', 'www-data')
#set('owner_group', 'www-data')


# Settings - protected shared files/dirs (db configs, certificates, keys, etc.)
#          * [PROTECTED] owner config settings are required to be set


#set('protected_shared_dirs', [])
#set('protected_shared_files', [])


# Settings - owner of [PROTECTED] shared files/dirs

#set('protected_owner_user', 'root')
#set('protected_owner_group', 'root')


# Tasks


@task
def restart():
    """
    Restarts application on remote server
    """
    
    with cd(fetch('current_path')):
        run('touch restart.txt')


@deploy_task(on_success=restart)
def deploy():
    """
    Runs deploy process on remote server
    """

    git_clone()
    link_shared_paths()


@setup_task
def setup():
    """
    Runs setup process on remote server
    """

    create_shared_paths()


@task
def rollback():
    """
    Rollbacks to previous release
    """

    rollback_release()


@task
def unlock():
    """
    Forces lockfile removal when previous deploy failed
    """

    force_unlock()
