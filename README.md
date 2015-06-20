Requires docker. Can be reproduced on a normal RHEL/Centos
6.5 x86_64 host with ssh access, but including this for completeness.

setup_env.sh          Builds two docker images: galera-repro and galera-repro-fab

start_containers.sh   Starts containers and runs the fabric scripts which reproduce the bug

The fabric script can probably be simplified but it is still reasonably small.

Sample run, WSREP_SST: lines appearing in mysqld-bin.index file on one host:

    [10.2.0.193] Executing task 'setup'
    [10.2.0.193] Saving password = secret
    [10.2.0.193] put: <file obj> -> /root/.my.cnf
    [10.2.0.193] run: cp "$(echo /etc/my.cnf)"{,.bak}
    [10.2.0.193] put: <file obj> -> /etc/my.cnf
    [10.2.0.193] sudo: pgrep mysqld
    [10.2.0.193] sudo: pgrep mysqld
    [10.2.0.193] put: <file obj> -> /var/lib/mysql/reset_password.sql
    [10.2.0.193] sudo: service mysql bootstrap --init-file=/var/lib/mysql/reset_password.sql
    [10.2.0.193] out: Bootstrapping the cluster.. Starting MySQL.. SUCCESS! 
    [10.2.0.193] out: 
    
    [10.2.0.193] sudo: rm /var/lib/mysql/reset_password.sql
    [10.2.0.193] Executing task 'create_databases'
    [10.2.0.193] sudo: mysql -N --batch -e "create database if not exists db1"
    [10.2.0.193] sudo: mysql -N --batch -e "grant all on db1.* to user@'%' identified by 'foo'"
    [10.2.0.193] sudo: mysql -N --batch -e "create database if not exists db2"
    [10.2.0.193] sudo: mysql -N --batch -e "grant all on db2.* to user@'%' identified by 'foo'"
    [10.2.0.193] sudo: mysql -N --batch -e "create database if not exists db3"
    [10.2.0.193] sudo: mysql -N --batch -e "grant all on db3.* to user@'%' identified by 'foo'"
    [10.2.0.193] sudo: mysql -N --batch -e "flush privileges"
    [10.2.0.194] Executing task 'create_databases'
    [10.2.0.195] Executing task 'create_databases'
    [10.2.0.193] sudo: mysql -N --batch -e "DROP DATABASE IF EXISTS test"
    [10.2.0.194] Executing task 'setup'
    [10.2.0.194] Saving password = secret
    [10.2.0.194] put: <file obj> -> /root/.my.cnf
    [10.2.0.194] run: cp "$(echo /etc/my.cnf)"{,.bak}
    [10.2.0.194] put: <file obj> -> /etc/my.cnf
    [10.2.0.194] sudo: service mysql restart || service mysql restart --wsrep-provider-options='pc.npvo=true'
    [10.2.0.194] out:  ERROR! MySQL server PID file could not be found!
    [10.2.0.194] out: Starting MySQL...SST in progress, setting sleep higher. SUCCESS! 
    [10.2.0.194] out: 
    
    [10.2.0.195] Executing task 'setup'
    [10.2.0.195] Saving password = secret
    [10.2.0.195] put: <file obj> -> /root/.my.cnf
    [10.2.0.195] run: cp "$(echo /etc/my.cnf)"{,.bak}
    [10.2.0.195] put: <file obj> -> /etc/my.cnf
    [10.2.0.195] sudo: service mysql restart || service mysql restart --wsrep-provider-options='pc.npvo=true'
    [10.2.0.195] out:  ERROR! MySQL server PID file could not be found!
    [10.2.0.195] out: Starting MySQL...SST in progress, setting sleep higher. SUCCESS! 
    [10.2.0.195] out: 
    
    
    Done.
    Disconnecting from 10.2.0.195... done.
    Disconnecting from 10.2.0.193... done.
    Disconnecting from 10.2.0.194... done.
    [10.2.0.193] Executing task 'check'
    [10.2.0.193] sudo: cat /var/lib/mysql/mysqld-bin.index
    [10.2.0.193] out: ./mysqld-bin.000001
    [10.2.0.193] out: ./mysqld-bin.000002
    [10.2.0.193] out: ./mysqld-bin.000003
    [10.2.0.193] out: WSREP_SST: [INFO] PrWSREP_SST: [INFO] Preparing binlog files for transfer: (20150302 22:17:15.835)
    [10.2.0.193] out: mysqld-bin.000005
    [10.2.0.193] out: 
    
    [10.2.0.194] Executing task 'check'
    [10.2.0.194] sudo: cat /var/lib/mysql/mysqld-bin.index
    [10.2.0.194] out: ./mysqld-bin.000004
    [10.2.0.194] out: ./mysqld-bin.000005
    [10.2.0.194] out: ./mysqld-bin.000006
    [10.2.0.194] out: 
    
    [10.2.0.195] Executing task 'check'
    [10.2.0.195] sudo: cat /var/lib/mysql/mysqld-bin.index
    [10.2.0.195] out: ./mysqld-bin.000005
    [10.2.0.195] out: ./mysqld-bin.000006
    [10.2.0.195] out: ./mysqld-bin.000007
    [10.2.0.195] out: 
    
    
    Done.
    Disconnecting from 10.2.0.195... done.
    Disconnecting from 10.2.0.193... done.
    Disconnecting from 10.2.0.194... done.
    a0361134e6f169be9e063bf648f6601345c3842925de95f20a3ca158d60f4db2
    92e268913a448d00e99ea422da2fe67ed1700e5cc06800f31544d347ace942d0
    9bbb0bf82faaf43c489e5f4d9a7e7fef86945535ab9ae86ebae61aa174477d83
