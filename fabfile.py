import time

from fabric.api import (env, execute, hide, run, settings, sudo, task,
                        runs_once, with_settings)
from fabric.contrib.files import upload_template
from fabric.utils import puts, abort

__all__ = ['setup', 'check']

WSREP_SYNCED = '4'


def mysql(query):
    return sudo('mysql -N --batch -e "%s"' % query)


def other_mysql_nodes():
    return [e for e in env.all_hosts
            if e != env.host_string]


def mysql_variable(variable_sql):
    with hide('running', 'output'):
        ret = mysql(variable_sql)
    status = ret.split("\t")
    if len(status) == 2:
        return status[1]
    return None


def mysql_global_variable(variable_name):
    return mysql_variable("show global variables like '%s'" % variable_name)


def mysql_status(variable_name):
    return mysql_variable("show status like '%s'" % variable_name)


def wait_until_node_synced():
    for x in range(0, 10):
        ret = mysql_status('wsrep_local_state')
        if ret == WSREP_SYNCED:
            break
        puts("waiting max 20s until wsrep_local_state == 4")
        puts("wsrep_local_state: [%s]" % ret)
        time.sleep(2.0)


def is_running():
    with settings(warn_only=True):
        with hide("warnings"):
            running = sudo("pgrep mysqld")
    return running.succeeded


def require_mysql_not_running():
    if is_running():
        abort('cannot continue, mysqld is running. stop it and try again')


def enable_bootstrap_in_running_node():
    mysql("SET GLOBAL wsrep_provider_options='pc.bootstrap=1'")


def bootstrap_cluster():
    if not env.get('first_db_node_started'):
        if is_running():
            enable_bootstrap_in_running_node()
        else:
            start_bootstrap_node(env.mysql_root_password,
                                 env.mysql_user_password)

        env['first_db_node_started'] = env.host_string
    else:
        sudo("service mysql restart || "
             "service mysql restart --wsrep-provider-options='pc.npvo=true'")
        wait_until_node_synced()


def start_bootstrap_node(mysql_root_password, user_password):
    require_mysql_not_running()
    upload_template('template/mysql_reset_password.sql',
                    '/var/lib/mysql/reset_password.sql',
                    context={'password': mysql_root_password})
    sudo('service mysql bootstrap ' +
         '--init-file=/var/lib/mysql/reset_password.sql')
    sudo("rm /var/lib/mysql/reset_password.sql")
    execute(create_databases)
    mysql("DROP DATABASE IF EXISTS test")


def create_mysqld_config():
    my_cnf_ctx = {}
    if len(env.all_hosts) > 1:
        nodelist = ",".join(other_mysql_nodes())
    else:
        nodelist = ""
    my_cnf_ctx['other_nodes'] = nodelist
    upload_template('template/my.cnf', '/etc/my.cnf',
                    context=my_cnf_ctx, mode=0644)


def save_root_password(password):
    user_cnf_ctx = {}
    puts("Saving password = %s" % password)
    user_cnf_ctx['password'] = password
    upload_template('template/user.my.cnf', '/root/.my.cnf',
                    context=user_cnf_ctx, mode=0600)


def configure_passwords():
    env['mysql_root_password'] = 'secret'
    env['mysql_user_password'] = 'foo'

    save_root_password(env.mysql_root_password)


def configure():
    configure_passwords()
    create_mysqld_config()


@task
def check():
    sudo('cat /var/lib/mysql/mysqld-bin.index')


@task
def setup():
    """Set up MySQL cluster."""
    env['mysql_databases'] = ['db1', 'db2', 'db3']
    configure()
    bootstrap_cluster()


@task
@with_settings(warn_only=True)
@runs_once
def create_databases():
    for name in env.mysql_databases:
        mysql('create database if not exists %s' % name)
        mysql(("grant all on %s.* to user@'%%' " +
              "identified by '%s'") %
              (name, env.mysql_user_password))
    mysql('flush privileges')
