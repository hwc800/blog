import db as mydb
import blog.config_db as config_db


def select_views_number_or_like_number(article_id) -> dict:
    """查询浏览量或点瓒数"""
    db = mydb.MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.user_view_number, config_db.DATABASE)
    result = table.select([{"article_id": article_id, "op": "="}])

    if not result:
        return {}

    return result


def select_user_comment_number(article_id) -> int:
    """查询评论数量"""
    db = mydb.MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.user_comment, config_db.DATABASE)
    sql = "select count(*) from %s where article_id=%s" % (config_db.user_comment, article_id)
    result = table.auto_select(sql)

    return result[0][0]


def insert_look_or_like_number(article_id, add_view_number=False, add_like_number=False):
    """更新文章浏览数量"""
    db = mydb.MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.user_view_number, config_db.DATABASE)
    result = table.select([{"article_id": article_id, "op": "="}])

    if not result:
        print(result)
        return False

    if add_view_number:
        sql = "update %s set view_number=%s where article_id=%s;" % (config_db.user_view_number, int(result["view_number"]) + 1, article_id)
        table.auto_select(sql)

    if add_like_number:
        sql = "update %s set like_number=%s where article_id=%s;" % (config_db.user_view_number, int(result["like_number"]) + 1, article_id)
        table.auto_select(sql)

    return True


def index_select(user_id) -> int:
    """查询评论数量"""
    db = mydb.MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.user_comment, config_db.DATABASE)
    sql = "select hwc.user_data.article_title as article_title,hwc.user_data.article_introduce as article_introduce," \
          "hwc.user_data.date as date,hwc.user_view_number.view_number as view_number,hwc.user_view_number.like_number as like_number," \
          "hwc.user_view_number.comment_number as comment_number from hwc.user_data join hwc.user_view_number on " \
          "hwc.user_view_number.article_id=hwc.user_data.article_id and hwc.user_view_number.user_id=%s;" % user_id

    result = table.auto_select(sql)
    g = mydb.db_dict(['article_title', 'article_introduce', 'date', 'view_number', 'like_number', 'like_number', "comment_number"], result)
    return g


def insert_views_number_or_like_number(**kwargs):
    """查询浏览量或点瓒数"""
    db = mydb.MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.user_view_number, config_db.DATABASE)
    try:
        table.insert(kwargs)
    except:
        db.rollback()
        return False

    return True