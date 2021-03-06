# coding:utf-8
__author__ = 'nacker'

from . import admin
from flask import render_template, request, jsonify, url_for, session
from app.models import *

# 请求处理之前的 装饰器
@admin.before_request
def checklogin():
    # 获取当前的请求路径
    path = request.path
    # 要求登录才能请求的路径
    urllist = [
        url_for('admin.index'),
        url_for('admin.userlist'),
        url_for('admin.blogslist'),
        url_for('admin.tagslist'),
        url_for('admin.commentslist'),
        ]
    if path in urllist:
        # 判断是否登录
        if not session.get('AdminUser',None):
            return '<script>alert("请先登录");location.href="'+url_for('admin.login')+'?next='+path+'"</script>'


@admin.route('/')
def index():
    # 统计 用户,博文,评论,标签 数量
    data = {}
    data['usnum'] = User.query.filter().count()
    data['bsnum'] = Posts.query.filter().count()
    data['csnum'] = Comments.query.filter().count()
    data['tsnum'] = Tags.query.filter().count()
    data['admin'] = session.get('AdminUser',None)
    # print("---------"+data['admin'])
    return render_template('admin/index.html', **data)

# 用户列表
@admin.route('/user/list/')
def userlist():
    # 获取页码数
    p = int(request.args.get('p',1))
    # 获取用户数据  参数1 当前页码数  参数2 每页显示的数量
    users = User.query.filter().paginate(p,2)
    a = list(users.iter_pages())
    b = len(a)
    data = {'users':users, 'a':a, 'b':b}
    print(b)
    return render_template('admin/user/list.html',**data)


# 用户状态的修改
@admin.route('/user/statusedit/')
def useredit():
    #获取用户对象
    ob = User.query.get(request.args.get('uid'))
    # 更新状态
    ob.status = int(request.args.get('status'))
    # 执行
    db.session.add(ob)
    db.session.commit()
    res = jsonify({'msg':'用户状修改成功!!'})

    return res


# 博文列表
@admin.route('/blogs/list/')
def blogslist():
    # 获取页码数
    p = int(request.args.get('p',1))
    # 获取用户数据  参数1 当前页码数  参数2 每页显示的数量
    blogs = Posts.query.filter().paginate(p,3)
    a = list(blogs.iter_pages())
    b = len(a)
    data = {'blogs':blogs, 'a':a, 'b':b}
    print(b)
    return render_template('admin/blogs/list.html', **data)


# 博文的删除
@admin.route('/blogs/blogsedit/')
def blogsedit():
    #获取用户对象
    print(request.args.get('pid'))
    ob = Posts.query.get(request.args.get('pid'))
    # 删除
    db.session.delete(ob)
    db.session.commit()
    res = jsonify({'msg':'博文删除成功!!'})

    return res


# 标签列表
@admin.route('/tags/list/')
def tagslist():
    # 获取页码数
    p = int(request.args.get('p',1))
    # 获取用户数据  参数1 当前页码数  参数2 每页显示的数量
    tags = Tags.query.filter().paginate(p,3)

    a = list(tags.iter_pages())
    b = len(a)
    data = {'tags':tags, 'a':a, 'b':b}
    print(b)
    return render_template('admin/tags/list.html', **data)


# 标签的删除
@admin.route('/blogs/tagsdel/')
def tagsdel():
    #获取用户对象
    # print(request.args.get('pid'))
    ob = Tags.query.get(request.args.get('tid'))
    # 删除
    db.session.delete(ob)
    db.session.commit()
    res = jsonify({'msg':'标签删除成功!!'})

    return res


# ajax修改标签名
@admin.route('/blogs/tagsupdate/')
def tagsupdate():
    # 获取ajax传过来的信息
    tid = request.args.get('tid')
    title = request.args.get('title')
    # 找到相应的标签
    ob = Tags.query.get(tid)
    # 更新标签名
    ob.name = title
    db.session.add(ob)
    db.session.commit()

    res = jsonify({'msg':'ok', 'info':title})
    return res


# 添加标签
@admin.route('/blogs/tagsadd/', methods=['GET','POST'])
def tagsadd():
    data = {}
    # 获取信息
    data['name'] = request.form['po']
    ob = Tags(**data)
    # 执行添加
    db.session.add(ob)
    db.session.commit()

    res = "<script>alert('添加成功');location.href='{}'</script>".format(url_for('admin.tagslist'))
    return res

# 评论列表
@admin.route('/comments/list/')
def commentslist():
    # 获取页码数
    p = int(request.args.get('p',1))
    # 获取用户数据  参数1 当前页码数  参数2 每页显示的数量
    comments = Comments.query.filter().paginate(p,1)
    a = list(comments.iter_pages())
    b = len(a)
    data = {'comments':comments, 'a':a, 'b':b}
    print(b)
    return render_template('/admin/comments/list.html', **data)


# 评论的删除
@admin.route('/blogs/commentsdel/')
def commentsdel():
    #获取用户对象
    # print(request.args.get('pid'))
    ob = Comments.query.get(request.args.get('cid'))
    # 删除
    db.session.delete(ob)
    db.session.commit()
    res = jsonify({'msg':'标签删除成功!!'})



# 登录
@admin.route('/login', methods=['GET', 'POST'])
def login():
    nextpath = request.args.get('next', '/')
    # print(nextpath)

    if request.method == 'GET':
        return render_template('admin/login.html')
    elif request.method == 'POST':
        # 用户名密码
        name = request.form['name']
        pwd = request.form['pwd']

        # print(name,pwd)

        admin = AdminUser.query.filter_by(name=name).first()

        try:
            if admin.pwd == pwd:
                session['AdminUser'] = {'name': name, 'id': admin.id}
                res = '<script>alert("登录成功");location.href="{next}"</script>'.format(next=nextpath)
                return res
            else:
                res = '<script>alert("账号或者密码错误,请重新登录!!");history.back(-1)</script>'
                return res
        except:
            res = '<script>alert("账号或者密码错误,请重新登录!!");history.back(-1)</script>'
            return res

# # 用户注册
# @admin.route('/register', methods=['POST','GET'])
# def register():
#
#     if request.method == 'GET':
#         return render_template('admin/register.html')
#     elif request.method == 'POST':
#
#         dict_data = request.json
#         print(request.form['name'])
#         name = dict_data.get['name']
#         pwd = dict_data.get['pwd']
#
#         admin = AdminUser.query.filter_by(name=name).first()
#
#         try:
#             if admin.pwd == pwd:
#                 res = '<script>alert("该账号已经注册!!!");history.back(-1)</script>'
#                 return res
#         except:
#             res = '<script>alert("该账号已经注册!!!");history.back(-1)</script>'
#             return res
#
#         # admin = AdminUser()
#         admin.name = name
#         admin.pwd = pwd
#         admin.status = True
#
#         session['AdminUser'] = {'name': name, 'id': admin.id}
#
#         # return render_template('admin/index.html')
#         return "OK"


# 退出登录
@admin.route('/logout')
def logout():
    session.pop('AdminUser')
    return "<script>alert('退出成功');location.href='{}'</script>".format(url_for('admin.login'))
