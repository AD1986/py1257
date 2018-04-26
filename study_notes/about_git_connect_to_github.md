#How to use GIT connect to github
  

>Author:AD1986
>Date:20180426
  

##0x01 Main reference
  

[廖雪峰的bolg关于GIT的笔记](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

## 0x02 Solved the problem of "Updates were rejected"
  
在学习廖雪峰的bolg关于GIT的笔记相关内容，实践时会发现因为GIT版本不同导致shell命令差异，执行"git push -u github master"时出现错误。
  
详述如下：
  
1. git init //初始化仓库
2. git add "file.name" //添加文件到本地仓库
3. git commit -m "first commit" //添加文件描述信息
4. git remote add github + 远程仓库地址 //链接远程仓库，创建主分支
5. git push -u github master //把本地仓库的文件推送到远程仓库
  
之后，发现出错了。
  
经实践确认，正确的步骤如下：
  
1. git init //初始化仓库
2. git add "file.name" //添加文件到本地仓库
3. git commit -m "first commit" //添加文件描述信息
4. git remote add github + 远程仓库地址 //链接远程仓库，创建主分支
5. git pull github master --allow-unrelated-histories  // 把本地仓库的变化连接到远程仓库主分支
6. git push -u github master //把本地仓库的文件推送到远程仓库