##### How to create test environment
[ubuntu](https://hub.docker.com/_/ubuntu)

- Pull and create ubuntu
```
# Pull Ubuntu images
docker pull ubuntu:18.04
# Create Ubuntu container
docker run -it --name ubuntu-test -p 2222:22 ubuntu:18.04
```
- Change root password
```
root@cc6b5eaa2cd4:/# passwd
Enter new UNIX password:123456
Retype new UNIX password:123456
```
- Update apt-get, install vim and openssh-server
```
root@cc6b5eaa2cd4:~# apt-get update \
    && apt-get install -y vim \
    && apt-get install -y openssh-server
```
- Enable root login
```
root@cc6b5eaa2cd4:~# vim /etc/ssh/sshd_config

#PermitRootLogin prohibit-password
->
PermitRootLogin yes
```
- Check and start sshserver
```
## check openssh-server status
root@cc6b5eaa2cd4:~# ps -e | grep ssh
## start sshserver
root@cc6b5eaa2cd4:~# /etc/init.d/ssh start
```
- Check sftp result
```
root@cc6b5eaa2cd4:~# cd ~/
root@cc6b5eaa2cd4:~# ls -a
.  ..  .bash_history  .bashrc  .cache  .profile  .selected_editor  .viminfo
```

##### How to test this component
- Fill in Ubuntu information to test/sftp/test_sftp_utils.py
```
CONFIG = {
    'hostname': 'localhost',
    'port': 2222,
    'username': 'root',
    'password': '123456'
}
```
