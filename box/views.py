from django.http import JsonResponse
from django.shortcuts import render
import db
import blog.config_db as config_db


# Create your views here.
def root_login(requests):
    if requests.method == 'GET':
        return render(requests, "page/login/login.html")


def box_mode(requests):
    if requests.method == 'GET':
        rep = render(requests, "page/mode.html")
        rep.set_cookie("user_id", 10000)
        rep.set_cookie("is_log", "sdffffodxx324mkfjigo")
        rep.set_cookie("is_root", "10re0gr4##**ty45555cccdert2143546##@%^%00")
        return rep


def box_index(requests):
    if requests.method == 'GET':
        result = db.article_title()
        page = 0
        data = {}
        for app in result:
            data[page] = app
            page += 1
        content = {
            "data": data
        }
        rep = render(requests, "mytemplates/box_index.html", content)
        rep.set_cookie("user_id", 10000)
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
        db.insert(config_db.markdown_content, user_id=user_id, content=content, content_date=content_date, article_id=content_id)
        data = {"content": g}
        # 插入导航表
        db.insert(config_db.user_data, article_id=content_id, user_id=user_id, article_title=content_title, article_introduce=article_introduce, date=content_date)

        return JsonResponse({"data": "no"})


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
        user_id = requests.COOKIES.get("user_id")
        result = db.article_title(user_id="%s" % user_id)
        page = 0
        data = {}
        for app in result:
            data[page] = app
            page += 1
        content = {
            "data": data
        }
        return render(requests, "page/user_index.html", content)
        # return JsonResponse({"data": "no"})