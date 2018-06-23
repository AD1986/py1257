# openldap and python3

## 0x00 架构
  
virtualbox 5.1.3
  
ubuntu 14.04.5
  
openldap 2.4.31
  
python 3.4.3
  
## 0x01 需求说明
  
1、搭建 openldap，提供目录服务；
  
2、openldap 的数据源来自于数据仓库导出的文本文件，使用 python 进行预处理，最终实现目录服务的同步，权限的有效期管理。
  
## 0x02 部署 ubuntu
  
导入一个纯净版 ubuntu 镜像。
  
在 virtualbox 中设置网卡参数。连接方式为桥接网卡，混杂模式为全部允许，刷新MAC地址。
  
之后启动虚拟机，修改本地电脑防火墙设置，互PING测试。虚拟机PING百度测试。
    
获取最新的软件包，升级已安装的所有软件包。
  
	sudo apt-get update
	sudo apt-get upgrade
  
安装 openssh-server。
  
	sudo apt-get install openssh-server
  
配置时间同步。
  
	sudo crontab -l
	sudo crontab -e
	*/10 * * * * /usr/sbin/ntpdate ntp1.aliyun.com >/dev/null 2>&1
	sudo crontab -l
  
制作镜像备份。
  
## 0x03 部署 openldap
  
执行命令：
  
	sudo apt-get install slapd ldap-utils
  
过程中需要设置管理密码：
  
	Please enter the password for the admin entry in your LDAP directory. 
	Administrator password:
	ldap
  
配置 ldap server，执行命令：
  
	sudo dpkg-reconfigure slapd
  
	Q1：If you enable this option, no initial configuration or database will be created for you. 
	Omit OpenLDAP server configuration?
	如果启用此选项，则不会为您创建初始配置或数据库。
	省略OpenLDAP服务器配置？
	A1：NO
  
	Q2：The DNS domain name is used to construct the base DN of the LDAP directory. For example, 'foo.example.org' will create the directory with 'dc=foo, dc=example, dc=org' as base DN.
	DNS域名用于构建LDAP目录的基本DN。 例如，'foo.example.org'将创建以'dc = foo，dc = example，dc = org'作为基准DN的目录。
	A2：tcrcb.com
  
	Q3：Please enter the name of the organization to use in the base DN of your LDAP directory.
	A3：tcrcb
  
	Q4：Please enter the password for the admin entry in your LDAP directory. 
	A4：ldap
  
	A5：ldap
  
	Q6：The HDB backend is recommended. HDB and BDB use similar storage formats, but HDB adds support for subtree renames. Both support the same configuration options.
	In either case, you should review the resulting database configuration for your needs. See /usr/share/doc/slapd/README.DB_CONFIG.gz for more details.  
	建议使用HDB后端。 HDB和BDB使用类似的存储格式，但HDB增加了对子树重命名的支持。 两者都支持相同的配置选项。
	无论哪种情况，您都应该查看所需的数据库配置。 有关更多详细信息，请参阅/usr/share/doc/slapd/README.DB_CONFIG.gz。
	A6：HDB
  
	Q7： Do you want the database to be removed when slapd is purged? 
	您是否希望在清除slapd时删除数据库？
	A7：NO
  
	Q8：There are still files in /var/lib/ldap which will probably break the configuration process. If you enable this option, the maintainer scripts will move the old database files out of the way before creating a new database.  
	在 /var/lib/ldap 存在文件可能会破坏配置过程。 如果启用此选项，则维护者脚本将在创建新数据库之前将旧数据库文件移开。
	A8：yes
  
	Q9：The obsolete LDAPv2 protocol is disabled by default in slapd. Programs and users should upgrade to LDAPv3.  If you have old programs which can't use LDAPv3, you should select this option and 'allow bind_v2' will be added to your slapd.conf file.
	默认情况下，废弃的LDAPv2协议在slapd中被禁用。 程序和用户应该升级到LDAPv3。 如果您的旧程序无法使用LDAPv3，则应选择此选项，'allow bind_v2'将添加到您的slapd.conf文件中。
	A9：NO
  
## 0x04 验证 openldap
  
执行命令：
  
	ldapsearch -x -LLL -b dc=tcrcb,dc=com
	netstat -an | grep 389
  
新建 add.ldif 文件：
  
	dn: ou=D027,dc=tcrcb,dc=com
	objectClass: top
	objectClass: organizationalUnit
	ou: D027
	physicalDeliveryOfficeName: 科技信息部
	
	dn: cn=0935,ou=D027,dc=tcrcb,dc=com
	objectClass: top
	objectClass: person
	objectClass: organizationalPerson
	cn: 0935
	sn: 杨超
	description: 610321876543214321
	title: 技术科员
	st: J032
	l: 1
  
进行添加操作，之后查询结果：
  
	ldapadd -x -D "cn=admin,dc=tcrcb,dc=com" -w ldap -f add.ldif
	ldapsearch -x -b "dc=tcrcb,dc=com"
  
新建 del.ldif 文件：
  
	cn=0935,ou=D027,dc=tcrcb,dc=com
	ou=D027,dc=tcrcb,dc=com
  
进行删除操作，之后查询结果：
  
	ldapdelete -x -D "cn=admin,dc=tcrcb,dc=com" -w ldap -f del.ldif
	ldapsearch -x -b "dc=tcrcb,dc=com"
  
## 0x05 编译安装 python3
  
官网下载 python3.6.5，格式为 Gzipped source tarball。
  
	ubuntu@localhost:~$ ls
	Python-3.6.5.tgz
	ubuntu@localhost:~$ sudo tar -xvf Python-3.6.5.tgz
	ubuntu@localhost:~$ sudo chown -R root:root Python-3.6.5/
	ubuntu@localhost:~$ sudo chown -R root:root Python-3.6.5/
	ubuntu@localhost:~$ cd Python-3.6.5/
	ubuntu@localhost:~/Python-3.6.5$  sudo more README
  
	On Unix, Linux, BSD, macOS, and Cygwin::

    ./configure
    make
    make test
    sudo make install

	ubuntu@localhost:~/Python-3.6.5$  sudo ./configure
  
报错处理：
  
	checking build system type... x86_64-pc-linux-gnu
	checking host system type... x86_64-pc-linux-gnu
	checking for python3.6... no
	checking for python3... python3
	checking for --enable-universalsdk... no
	checking for --with-universal-archs... no
	checking MACHDEP... linux
	checking for --without-gcc... no
	checking for --with-icc... no
	checking for gcc... no
	checking for cc... no
	checking for cl.exe... no
	configure: error: in `/opt/Python-3.6.5':
	configure: error: no acceptable C compiler found in $PATH
	See `config.log' for more details

	ubuntu@localhost:~/Python-3.6.5$ sudo apt-get install make gcc

	ubuntu@localhost:~/Python-3.6.5$  sudo ./configure
	ubuntu@localhost:~/Python-3.6.5$  sudo make
	ubuntu@localhost:~/Python-3.6.5$  sudo make install

	ubuntu@localhost:~/Python-3.6.5$  sudo apt-get install zlib*

	ubuntu@localhost:~/Python-3.6.5$ sudo make install

	The directory '/home/ubuntu/.cache/pip/http' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
	The directory '/home/ubuntu/.cache/pip' or its parent directory is not owned by the current user and caching wheels has been disabled. check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.

	sudo pip install requests 会报错
	sudo -H pip install requests 这样就好了
  
## 0x06 写代码并完成需求，具体见 README.vsd
  
最终完成的代码文件列表：
  
	主函数
	ldap_main.py
	功能函数
	file_util.py
	file_merge.py
	file_dos2unix.py
	file_del_duplicate_line.py
	file_copy.py
	file_comparison_add_dup_line.py
	file_comparison_add_diff_line.py

	以及“对文件最后一行”的处理函数
	file_last_line.py
  
另外需要说明的是，时间仓促，边学边写，所以代码质量不高。
  
>Author:AD1986
>  
>Date:20180623