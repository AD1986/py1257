>Author:AD1986
>  
>Date:20180502

  
# Using Django for the first time
  
## 架构选择
  
Windows 10
  
Python 3.6.5
  
Pip 10.0.1
  
Django 2.0.5
  
MySQL 8.0.11
  
## 部署步骤
  
默认已完成Windows 10安装。
  
从[Python官网](https://www.python.org/)下载安装包，完成安装。之后在CMD黑屏终端输入以下指令进行状态检查：
  
	python
  
之后，更新pip至最新版本，并完成Django的安装。在system32目录下的CMD黑屏终端输入以下指令:
  
	python -m pip install --upgrade pip
	pip --version
	pip install Django
  
验证Django的安装结果，在 system32 目录下的CMD黑屏终端输入以下指令:
  
	python
	import django
	django.get_version()
  
最后，安装MySQL。从[MySQL官网](https://dev.mysql.com/)下载安装程序，选择Windows (x86, 32-bit) MSI Installer，安装过程选择 Server only，最终完成安装。另外，mysql的启停可以使用windows服务进行管理，不再赘述。
  
安装完成后，需要配置环境变量，将安装好的bin目录，添加到环境变量的path中，并使用CMD黑屏终端进行验证：
  
	mysql -u root -p
  
最后，完成Demo数据库的创建：
  
	create database first_time;
  
检查Demo数据库创建的结果：
	show databases;
  

## 对于Django框架连接MySQL的必要配置
  
必须安装mysqlclient，以及mysqlclient的依赖包protobuf
  
	pip install protobuf
	pip install mysqlclient
  

## 创建项目
  
创建一个工程目录，并使用CMD黑屏终端进入该目录。使用Django指令，创建具体项目目录first\_time
  
	D:
	cd D:\django_study  
	django-admin startproject first_time
  
命令执行成功后，在 django\_study 目录中自动生产了名为 first\_time 的文件夹。此时，可以使用 tree命令 查看具体的结果，指令如下：
  
	tree . /F
  
通过树状目录，可以看出在项目目录 first\_time 下，生成了 manage.py 和 first_time 二级目录，二级目录下包含四个文件，分别是： settings.py urls.py wsgi.py \--init--.py
  
* manage.py，这是一个命令行工具，基本不去修改，我们可以通过此工具使用多种方式对Django项目进行交互；
* settings.py，项目配置文件；
* urls.py，项目的URL声明；
* wsgi.py，项目与WSGI兼容的WEB服务器入口；
* \--init--.py，这是一个空文件，它告诉python此目录可以被视为一个python包；
  
## Demo搭建
  
### 设计数据库表结构
  
Demo中规划了两张表，分别是班级表和学生表。
  
	班级表结构   
	表名：grades； 
	字段1：班级名称，gname；
	字段2：成立时间，gdate；
	字段3：女生人数，ggirlnum；
	字段4：男生人数，gboynum；
	字段5：是否删除，isdelete；
  
	学生表结构   
	表名：students；
	字段1：学生姓名，sname；
	字段2：性别，sgender；
	字段3：年龄，sage；
	字段4：简介，scontend；
	字段5：所属班级，sgrade；
	字段6：是否删除，isdelete；
	  
### 修改django所使用的默认数据库
  
django使用的默认数据库为sqlite3， 在二级目录下的setting.py中能找到默认配置：
  
	DATABASES = {
    	'default': {
    	    'ENGINE': 'django.db.backends.sqlite3',
    	    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    	}
	}
  
修改之后的配置如下：
  
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'HOST': 'localhost',
	        'PORT': '3306',
	        'NAME': 'first_time',
	        'USER': 'root',
	        'PASSWORD': 'mysql',
	    }
	}
  
### 创建应用
在一级目录 first\_time 中执行以下指令：
  
	python manage.py startapp myApp
  
该指令正常执行后，将在一级目录 first\_time中生成 myApp目录。二级目录myApp中包含了一个名为 migrations 的文件夹与六个文件。
