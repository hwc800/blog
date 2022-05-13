import json

import requests as requests
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import db
import blog.config_db as config_db


# Create your views here.
def comment(requests):
    if requests.method == 'GET':
        from blog import token as tk

        token = requests.COOKIES.get("token")
        msg_token = tk.check_token_and(token)

        if not msg_token:
            # 验证登陆状态
            return HttpResponseRedirect("/login")

        return render(requests, "page/login/comment.html")


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


def box_index(requests):
    if requests.method == 'GET':
        from blog import token as tk

        token = requests.COOKIES.get("token")
        msg_token = tk.check_token_and(token)

        if not msg_token:
            # 验证登陆状态
            return HttpResponseRedirect("/login")

        result = db.article_title()
        page = 0
        data = {}

        for app in result:
            data[page] = app
            page += 1

        content = {"data": data}
        rep = render(requests, "mytemplates/box_index.html", content)
        rep.set_cookie("is_log", "sdffffodxx324mkfjigo")
        rep.set_cookie("is_root", "10re0gr4##**ty45555cccdert2143546##@%^%00")

        return rep


def box_content(requests):
    import datetime, time
    if requests.method == 'POST':
        user_id = requests.COOKIES.get("user_id")
        content_title = requests.POST.get("content_title")
        article_introduce = requests.POST.get("article_introduce")

        # 插入content
        g = requests.POST.get("content")
        content_id = str(time.time())
        content_date = str(datetime.datetime.now())[:19]
        content = g
        content = content.replace("\"", "\\'")
        try:
            db.insert(config_db.markdown_content, user_id=user_id, content=content, content_date=content_date, article_id=content_id)
        except:
            return JsonResponse({"data": "no"})

        # 插入导航表
        try:
            db.insert(config_db.user_data, article_id=content_id, user_id=user_id, article_title=content_title, article_introduce=article_introduce, date=content_date)
        except:
            return JsonResponse({"data": "no"})

        return JsonResponse({"data": "ok"})


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

        if not title:
            return JsonResponse({"data": "no"})

        title = title[0]["article_title"]
        data = {
            "content": content,
            "title": title,
        }
        return render(requests, "page/show_mode.html", data)


def user_index(requests):
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
    # 严重登陆
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




