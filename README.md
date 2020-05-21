# 论坛网址

http://123.57.144.109/

默认用户：密码123  密码：123

# 项目描述

–实现了话题浏览与分类、话题发布，评论回复，用户个人信息设置，基于Celery消息队列私信、@提醒、密码找回等功能

–数据存储使用 MySQL，ORM 使用 SQLAlchemy

–实现对 CSRF、XSS、SQL 注入攻击的防御

–使用 Jinja2 模板继承技术减少重复开发，代码易于维护

–使用 Nginx 做反向代理，压缩静态资源，提高访问速度

–使用 Redis 数据库保存和共享多进程下的 Session 和 token，保证数据传输可靠性和高速度

–通过 Gevent 模式同时配合 Gunicorn 实现多进程负载均衡，并使用 Supervisor 进行进程守护管理

–使用 Shell 脚本进行一键部署

# 项目展示

用户登录注册

![img](https://github.com/YajueSP1919/flask_web/blob/master/gifs/s1.gif)

用户通过邮箱重置密码

![img](https://github.com/YajueSP1919/flask_web/blob/master/gifs/s2.gif)

用户发贴和发表评论

![img](https://github.com/YajueSP1919/flask_web/blob/master/gifs/s3.gif)

站内信

![img](https://github.com/YajueSP1919/flask_web/blob/master/gifs/s4.gif)

用户个人主页

![img](https://github.com/YajueSP1919/flask_web/blob/master/gifs/s5.gif)




