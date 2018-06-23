>Author:AD1986
>  
>Date:20180502
  
# Using Django for the first time
  
## 0x01 架构选择
  
Windows 10
  
Python 3.6.5
  
Pip 10.0.1
  
Django 2.0.5
  
MySQL 5.7.22
  
## 0x02 部署步骤
  
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
  
最后，安装MySQL并完成Demo数据库的创建。
  
从[MySQL官网](https://dev.mysql.com/)下载安装程序，选择Windows (x86, 32-bit) MSI Installer，安装过程选择 Server only，最终完成安装。另外，mysql的启停可以使用windows服务进行管理，不再赘述。
  
安装完成后，需要配置环境变量，将安装好的bin目录，添加到环境变量的path中，并使用CMD黑屏终端进行验证：
  
	mysql -u root -p
  
完成Demo数据库的创建：
  
	create database first_db CHARACTER SET utf8;
  
检查Demo数据库创建的结果：
  
	show databases;
	+--------------------+
	| Database           |
	+--------------------+
	| first_db           |
	| information_schema |
	| mysql              |
	| performance_schema |
	| sys                |
	+--------------------+
  
## 0x03 对于Django框架连接MySQL的必要配置
  
Django 推荐的方案是使用 mysqlclient，安装事项见[官网说明](https://pypi.org/project/mysqlclient/)，请留心 mysqlclient 的相关依赖文件。
  
在安装完成后，需要修改 Django 的具体项目配置文件，此方面内容将在"Demo搭建"数据库配置部分进行详细说明。
  
## 0x04 创建项目
  
创建一个工程目录，并使用CMD黑屏终端进入该目录。使用Django指令，创建具体项目目录first\_demo
  
	D:
	cd D:\django_study
	django-admin startproject first_demo
  
命令执行成功后，在 django\_study 目录中自动生产了名为 first\_demo 的文件夹。此时，可以使用 tree命令 查看具体的结果，指令如下：
  
	tree . /F
  
通过树状目录，可以看出在项目目录 first\_demo 下，生成了 manage.py 和 first\_demo 二级目录，二级目录下包含四个文件，分别是： settings.py urls.py wsgi.py \_\_init__.py
  
* manage.py，这是一个命令行工具，基本不去修改，我们可以通过此工具使用多种方式对Django项目进行交互；
* settings.py，项目配置文件；
* urls.py，项目的URL声明；
* wsgi.py，项目与WSGI兼容的WEB服务器入口；
* \_\_init__.py，这是一个空文件，它告诉python此目录可以被视为一个python包；
  
## 0x05 Demo搭建
  
### 1 设计数据库表结构
  
Demo中规划了两张表，分别是班级表和学生表。
  
	班级表结构   
	表名：grade； 
	字段1：班级名称，g_name；
	字段2：成立时间，g_date；
	字段3：女生人数，g_girl_num；
	字段4：男生人数，g_boy_num；
	字段5：是否删除，is_delete；
  
	学生表结构   
	表名：student；
	字段1：学生姓名，s_name；
	字段2：性别，s_gender；
	字段3：年龄，s_age；
	字段4：简介，s_contend；
	字段5：所属班级，s_grade；
	字段6：是否删除，is_delete；
	  
### 2 修改django所使用的默认数据库
  
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
	        'NAME': 'first_db',
	        'USER': 'root',
	        'PASSWORD': 'mysql',
	        'HOST': '127.0.0.1',
	        'PORT': '3306',
	    }
	}
  
### 3 创建应用，并将此应用配置至项目中（即激活应用）
在一级目录 first\_demo 中执行以下指令：
  
	python manage.py startapp myApp
  
该指令正常执行后，将在一级目录 first\_demo中生成 myApp目录。二级目录 myApp 中包含了一个名为 migrations 的文件夹与六个文件。
  
* \_\_init__.py，同样的，这是一个空文件，它告诉python此目录可以被视为一个python包；
* admin.py，站点配置文件；
* models.py，模型配置文件，数据库的每一张表都对应一个模型（即数据库中有多少张表，就应有在此文件中定义多少个模型）；
* views.py，视图配置文件；

  
打开二级目录 first\_demo 中的 settings.py 文件，将 myApp 应用加入到 INSTALLED\_APPS 的配置中。
  
	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
		# 以下为配置修改的内容
	    'myApp',
	]
  
### 4 模型的定义与简单使用
  
#### 4.1 定义模型
  
修改二级目录 myApp 中的 models.py 文件，新建“班级表”与“学生表”对应的模型：
  
	# 以下两个模型类均没有定义主键。在随后使用模型初始化数据库的过程中，每张表都会默认生成一个名为 id 的主键，且其值会随着表内条目的增加而自动递增。
	class Grade(models.Model):
	    g_name = models.CharField(max_length=20)
	    g_date = models.DateTimeField()
	    g_girl_num = models.IntegerField()
	    g_boy_num = models.IntegerField()
	    is_delete = models.BooleanField(default=False)
	
	class Student(models.Model):
	    s_name = models.CharField(max_length=20)
	    s_gender = models.BooleanField(default=True)
	    s_age = models.IntegerField()
	    s_contend = models.CharField(max_length=40)
	    # 关联外键
	    s_grade = models.ForeignKey("Grade", on_delete=models.CASCADE)
	    is_delete = models.BooleanField(default=False)
  
#### 4.2 初始化数据表
  
使用模型初始化数据库中的数据表（生成数据表）。具体分为两步，分别是：生成迁移文件；执行迁移。
  
##### 生成迁移文件
  
使用CMD黑屏终端，进入一级目录，执行以下指令：
  
	python manage.py makemigrations
  
执行成功后，CMD黑屏终端会有如下反馈：
  
	Migrations for 'myApp':
	  myApp\migrations\0001_initial.py
	    - Create model Grade
	    - Create model Student
  
完成后，此时检查 first\_db 数据库，会发现此数据库中没有任何数据表。
  
	use first_db;
	show tables;
  
但在二级目录 myApp 下的 migrations 目录中出现了 0001\_initial.py 文件，此文件即为迁移文件。
  
##### 执行迁移
  
使用CMD黑屏终端，进入一级目录，执行以下指令：
  
	python manage.py migrate
  
完成后，此时检查 first\_db 数据库，会发现此数据库中已经生成了数据表，并已完成数据表中的字段定义。
  
	use first_db;
	show tables;
	desc myapp_grade;
	desc myapp_student;
  
### 4.3 利用 Python Shell 与数据库交互
  
#### 前期准备
首先，由于将使用到 model.datatime() 函数，该函数会检查时区。默认配置将产生时区异常警告，因此需要修改 二级目录 first\_demo 中的 settings.py 文件，具体修改参数为“TIME\_ZONE”和“USE\_TZ”。
  
	TIME_ZONE = 'Asia/Shanghai'
	USE_TZ = False
  
之后，进入 Python Shell，执行指令：
  
	python manage.py shell
  
最后，在 Python Shell 模式下引入包：
  
	from myApp.models import Grade,Student
	from django.utils import timezone
	from datetime import *
  
#### 查询方法说明

在 Python Shell 模式下， Django 可以通过模型查询 myapp\_grade 表中数据，具体方法如下：
  
	Grade.objects.all()
  
#### 增删改查
  
首先，通过模型向 myapp\_grade 表中添加一条数据：
  
	grade1 = Grade()
	grade1.g_name = "python04"
	grade1.g_date = datetime(2017,7,17,0,0,0)
	grade1.g_girl_num = 3
	grade1.g_boy_num = 70
  
检查数据库，发现 myapp\_grade 数据表中没有数据。
  
	select * from myapp_grade;
  
之后，在 Python Shell 中执行指令：
  
	grade1.save()
  
再次查询 myapp\_grade 数据表，可以确认数据已添加到该表中。同时，在 Python Shell 中执行指令：
  
	Grade.objects.all()
  
确认查询结果能正常返回。
  
另外，可以通过重写类重写 Grade 类，将返回值格式化：
  
	class Grade(models.Model):
    g_name = models.CharField(max_length=20)
    g_date = models.DateTimeField()
    g_girl_num = models.IntegerField()
    g_boy_num = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    def __str__(self):
        return "班级名称：%s\t女生人数：%d\t男生人数：%d"%(self.g_name,self.g_girl_num,self.g_boy_num)
	
	# 在 Python Shell 中执行“Grade.objects.all()”的返回值
	<QuerySet [<Grade: 班级名称：python04   女生人数：3     男生人数：70>, <Grade: 班级名称：python05   女生人数：31     男生人数：55>]>
  
也可以通过以下指令查找已知主键的数据库条目：
  
	Grade.objects.get(pk=2)
  
可以通过模型修改数据：
  
	grade1.g_girl_num = 3
	grade1.save()
  
还可以删除具体的条目：
  
	grade2.delete()
	# 此指令会将数据库中的指定条目删除
  
#### 外键的使用
  
在 Python Shell 中实例化一名学生：
  
	grade1=Grade.objects.get(pk=1)
	stu1=Student()
	stu1.s_name="张三"
	stu1.s_age=22
	stu1.s_contend="我叫张三"
	stu1.s_grade=grade1
	stu1.save()
  
在 Python Shell 中实例化另一名学生，另外，查询出属于某一特定班级的所有学生：
  
	grade1=Grade.objects.get(pk=1)
	stu2=Student()
	stu2.s_name="李四"
	stu2.s_gender= False
	stu2.s_age=22
	stu2.s_contend="我叫李四，我是女生"
	stu2.s_grade=grade1
	stu2.save()
	grade1.student_set.all()
	# 此处的 grade1 为外键
  
另外，可以通过下列语句一次性写入数据库：
  
	stu4 = grade1.student_set.create(s_name=u"赵六",s_age=21,s_contend=u"我叫赵六")
  
## 0x06 Admin站点管理
  
### 前期准备
  
在 Python Shell 中，创建管理员用户：
  
	python manage.py createsuperuser
  
依次输入用户名、邮箱、密码。
  
之后，检查二级目录下的 setting.py 配置文件，确认配置项 INSTALLED_APPS 中存在"django.contrib.admin"。
  
启动web服务器，"ip"默认为本机地址，端口号默认为"8000"：
  
	python manage.py runserver <ip:port>
  
事实上，此web服务器是纯python构建的轻量级web服务器，仅适用于开发测试阶段。另外，停止服务需要使用 "crtl + c"。
  
访问以下 url，最终进入管理后台：
  
	http://127.0.0.1:8000/admin
  
### 利用后台维护数据库
  
首先，需要将"班级表"和"学生表"添加到admin用户后台可视化页面中，需要配置二级目录 myApp 目录下 admin.py, 配置完成后刷新web界面即可。
  
	from .models import Grade,Student
	admin.site.register(Grade)
	admin.site.register(Student)
  
重写"班级表"的展示页面，需要进一步配置二级目录 myApp 目录下 admin.py。
  
	class GradeAdmin(admin.ModelAdmin):
	    # 列表页面属性
	    list_display = ['pk', 'g_name', 'g_date', 'g_girl_num', 'g_boy_num', 'is_delete']
	    list_filter = ['g_name']  # 过滤器
	    search_fields = ['g_name']  # 搜索栏
	    list_per_page = 5
	    # 明细页面属性，单击add按钮后出现的页面
	    # fields = ['g_girl_num', 'g_boy_num', 'g_name', 'g_date', 'is_delete']  # 修改了页面的显示顺序
	    fieldsets = [
	        ('num', {"fields": ['g_girl_num', 'g_boy_num']}),
	        ('base', {"fields": ['g_name', 'g_date', 'is_delete']}),
	    ]  # 分组显示
	    # 注意 fields与fieldsets同一时间只能使用一种
	
	admin.site.register(Grade, GradeAdmin)
	# 这里添加了 GradeAdmin
  
之后，重写学生页。
  
	class StudentAdmin(admin.ModelAdmin):
	    list_display = ['pk', 's_name', 's_gender', 's_age', 's_contend', 's_grade', 'is_delete']
	    list_filter = ['s_gender']
	    search_fields = ['s_name']
	    list_per_page = 10
	    fields = ['s_name', 's_grade', 's_age', 's_gender', 's_contend', 'is_delete']
	
	admin.site.register(Student, StudentAdmin)
  
最后，重写二级目录 myApp 目录下 models.py 中的班级类和学生类。
  
	class Grade(models.Model):
	    g_name = models.CharField(max_length=20)
	    g_date = models.DateTimeField()
	    g_girl_num = models.IntegerField()
	    g_boy_num = models.IntegerField()
	    is_delete = models.BooleanField(default=False)
	    def __str__(self):
	        return self.g_name
	
	class Student(models.Model):
	    s_name = models.CharField(max_length=20)
	    s_gender = models.BooleanField(default=True)
	    s_age = models.IntegerField()
	    s_contend = models.CharField(max_length=40)
	    # 关联外键
	    s_grade = models.ForeignKey("Grade", on_delete=models.CASCADE)
	    is_delete = models.BooleanField(default=False)
	    def __str__(self):
	        return self.s_name
  
在创建班级时，实现可以直接添加学生。实现此功能需要继承 TabularInline，并进行关联。
  
	class GradeInit(admin.TabularInline):
	    model = Student
	    extra = 3
	    # 在新建班级的同时，新增3个学生
	
	class GradeAdmin(admin.ModelAdmin):
	    # 进行关联
	    inlines = [GradeInit]
	
	    # 列表页面属性
	    list_display = ['pk', 'g_name', 'g_date', 'g_girl_num', 'g_boy_num', 'is_delete']
	    list_filter = ['g_name']  # 过滤器
	    search_fields = ['g_name']  # 搜索栏
	    list_per_page = 5
	
	    # 明细页面属性，单击add按钮后出现的页面
	    # fields = ['g_girl_num', 'g_boy_num', 'g_name', 'g_date', 'is_delete']  # 修改了页面的显示顺序
	    fieldsets = [
	        ('num', {"fields": ['g_girl_num', 'g_boy_num']}),
	        ('base', {"fields": ['g_name', 'g_date', 'is_delete']}),
	    ]  # 分组显示
	    # 注意 fields与fieldsets同一时间只能使用一种
  
重写布尔值返回值。实现此需求，首先需要新建函数 bool\_s\_gender()，之后需要将此函数传入 list\_display，最后可以用 short\_description 方法修改字段在页面上的显示。
  
	class StudentAdmin(admin.ModelAdmin):
	    # 新建函数 bool_s_gender()
	    def bool_s_gender(self):
	        if self.s_gender:
	            return "Male"
	        else:
	            return "Female"

		bool_s_gender.short_description = "性别"

	    # 传入函数 bool_s_gender
	    list_display = ['pk', 's_name', bool_s_gender, 's_age', 's_contend', 's_grade', 'is_delete']
	    list_filter = ['s_grade']
	    search_fields = ['s_name']
	    list_per_page = 10
	    fields = ['s_name', 's_grade', 's_age', 's_gender', 's_contend', 'is_delete']
  
### 使用装饰器进行页面注册
  
未成功，以下代码出错
  
	@admin.register(Student)
	class StudentAdmin(admin.ModelAdmin):
	    # 新建函数 bool_s_gender()
	    def bool_s_gender(self):
	        if self.s_gender:
	            return "Male"
	        else:
	            return "Female"
	
	    bool_s_gender.short_description = "性别"
	
	    # 传入函数 bool_s_gender
	    list_display = ['pk', 's_name', bool_s_gender, 's_age', 's_contend', 's_grade', 'is_delete']
	    list_filter = ['s_grade']
	    search_fields = ['s_name']
	    list_per_page = 10
	    fields = ['s_name', 's_grade', 's_age', 's_gender', 's_contend', 'is_delete']
	
	# admin.site.register(Student, StudentAdmin)