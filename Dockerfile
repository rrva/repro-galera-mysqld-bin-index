FROM centos:6
RUN yum install -y upstart openssh-server
RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN sed -ri 's/session    required     pam_loginuid.so/#session    required     pam_loginuid.so/g' /etc/pam.d/sshd
RUN mkdir -p /root/.ssh && chown root.root /root && chmod 700 /root/.ssh
RUN echo 'root:docker' | chpasswd
ADD MariaDB.repo /etc/yum.repos.d/
RUN yum install -y MariaDB-Galera-server sudo which
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
