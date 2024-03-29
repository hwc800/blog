import json
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import db
import blog.config_db as config_db

from blog import token as tk

from box import views_function
# Create your views here.
# blog留言
def comment(requests):
    if requests.method == 'GET':

        token = requests.COOKIES.get("token")
        msg_token = tk.check_token_and(token)

        if not msg_token:
            # 验证登陆状态
            return HttpResponseRedirect("/login")

        return render(requests, "page/comment.html")


# 关于博主)
def about(requests):
    if requests.method == 'GET':

        return render(requests, "page/about.html")


# 模板
def box_mode(requests):
    if requests.method == 'GET':
        from blog import token as tk

        token = requests.COOKIES.get("token")
        msg_token = tk.check_token_and(token)

        if not msg_token:
            # 验证登陆状态
            return HttpResponseRedirect("/login")

        rep = render(requests, "page/mode.html")
        return rep


# 主页
def box_index(requests):
    if requests.method == 'GET':

        result = db.article_title()
        page = 0
        data = {}

        for app in result:
            data[page] = app
            page += 1

        content = {"data": data}
        content["new"] = result[-1]
        rep = render(requests, "mytemplates/box_index.html", content)
        rep.set_cookie("is_log", "sdffffodxx324mkfjigo")
        rep.set_cookie("is_root", "10re0gr4##**ty45555cccdert2143546##@%^%00")

        return rep


# 存储模板传递的数据
def box_content(requests):
    import datetime, time
    if requests.method == 'POST':
        token = requests.COOKIES.get("token")
        msg_token = tk.check_token_and(token)

        if not msg_token:
            # 验证登陆状态
            return HttpResponseRedirect("/login")
        user_id = msg_token["user_id"]
        content_title = requests.POST.get("content_title")
        article_introduce = requests.POST.get("article_introduce")

        # 插入content
        g = requests.POST.get("content")
        content_id = str(time.time())
        content_date = str(datetime.datetime.now())[:19]
        content = g
        content = content.replace("\"", "\\'")
        if not db.insert(config_db.markdown_content, user_id=user_id, content=content, content_date=content_date, article_id=content_id):
            return JsonResponse({"data": "no"})

        # 插入导航表
        if not db.insert(config_db.user_data, article_id=content_id, user_id=user_id, article_title=content_title, article_introduce=article_introduce, date=content_date):
            return JsonResponse({"data": "no"})
        # 浏览量点赞量数据初始化
        mydb = db.MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
        # 操作表类
        table = mydb.usetable(config_db.user_view_number, config_db.DATABASE)
        try:
            table.insert(article_id=content_id, user_id=user_id, view_number=0, like_number=0, comment_number=0)
        except:
            JsonResponse({"data": "no"})

        return JsonResponse({"data": "ok"})


# 文章详情界面
def box_show_mode(requests):
    if requests.method == "GET":

        article_id = requests.GET.get("article_id")

        if not article_id:
            return JsonResponse({"data": "no"})
        result = db.select_markdown_content(article_id)
        title = db.select(config_db.user_data, article_id=article_id)

        if not result:
            return JsonResponse({"data": "no"})

        content = result[0]["content"]

        if "\n" in content:
            content = content.replace("\n", "\\n")

        elif "\t" in content:
            content = content.replace("\t", "\\t")

        elif "\a" in content:
            content = content.replace("\a", "\\a")

        elif "\a" in content:
            content = content.replace("#", r"\#")

        if not title:
            return JsonResponse({"data": "no"})

        title = title[0]["article_title"]
        data = {
            "content": content,
            "title": title,
        }

        res = render(requests, "page/show_mode.html", data)
        res.set_cookie("article_id", article_id)

        views_function.insert_look_or_like_number(article_id, add_view_number=True)

        return res


def user_index(requests):
    # 我的界面
    if requests.method == 'GET':
        from blog import token as tk

        token = requests.COOKIES.get("token")
        msg_token = tk.check_token_and(token)
        if not msg_token:
            # 严重登陆状态
            return HttpResponseRedirect("/login")

        try:
            result = db.article_title(user_id="%s" % msg_token["user_id"])
        except:
            return render(requests, "page/user_index.html")

        page = 0
        data = {}
        for app in result:
            data[page] = app
            page += 1
        content = {
            "data": data
        }
        return render(requests, "page/user_index.html", content)


def login(requests):
    if requests.method == "GET":
        return render(requests, "page/login/login.html")


def set_token(requests):
    # 验证登陆
    if requests.method == "POST":
        user_name = requests.POST.get("user_name")
        password = requests.POST.get("password")
        result = db.select(config_db.user_table, user_name=user_name)

        if not result:
            return JsonResponse({"data": "no"})

        if password != result[0]["password"]:
            return JsonResponse({"data": "no"})

        from blog import token as tk

        token = tk.get_token(user_id=result[0]["user_id"])
        res = HttpResponse(json.dumps({"data": "ok"}), content_type='application/json')
        res.cookies.load({"token": token})

        return res


def edit_page(requests):
    # 修改文章
    if requests.method == 'GET':
        from blog import token as tk

        token = requests.COOKIES.get("token")
        msg_token = tk.check_token_and(token)
        if not msg_token:
            # 严重登陆状态
            return HttpResponseRedirect("/login")

        article_id = requests.GET.get("article_id")

        if not article_id:
            return JsonResponse({"data": "no"})
        result = db.select_markdown_content(article_id)
        title = db.select(config_db.user_data, article_id=article_id)
        content = result[0]["content"]

        if "\n" in content:
            content = content.replace("\n", "\\n")

        elif "\t" in content:
            content = content.replace("\t", "\\t")

        elif "\a" in content:
            content = content.replace("\a", "\\a")

        if not title:
            return JsonResponse({"data": "no"})
        article_title = title[0]["article_title"]
        article_introduce = title[0]["article_introduce"]
        data = {
            "content": content,
            "title": article_title,
            "article_introduce": article_introduce,
        }

        res = render(requests, "page/edit_page.html", data)
        res.set_cookie("article_id", article_id)

        return res


# 修改文章数据
def update_content(requests):
    import datetime, time
    if requests.method == 'POST':
        token = requests.COOKIES.get("token")
        msg_token = tk.check_token_and(token)

        if not msg_token:
            # 验证登陆状态
            return HttpResponseRedirect("/login")
        user_id = msg_token["user_id"]
        content_title = requests.POST.get("content_title")
        article_introduce = requests.POST.get("article_introduce")

        # 插入content
        g = requests.POST.get("content")
        content_id = requests.COOKIES.get("content_id")
        content_date = str(datetime.datetime.now())[:19]
        content = g
        content = content.replace("\"", "\\'")

        datas = {
            "content": content,
        }
        # 修改content
        if not db.update(config_db.markdown_content, need_update_file_names_and_datas=datas, where_is_files={"content_id": content_id}):
            return JsonResponse({"data": "no"})

        # 修改导航表
        datas = {
            "content_title": content_title,
            "article_introduce": article_introduce,
        }
        if not db.update(config_db.user_data, need_update_file_names_and_datas=datas, where_is_files={"content_id": content_id}):
            return JsonResponse({"data": "no"})

        return JsonResponse({"data": "ok"})
