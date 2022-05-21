
HOST = "118.195.188.25"
PWD = "qs@A190!=Lkisje.stfp?#;"
USER = "root"
DATABASE = "hwc"


"""
user_table = {
    "id": "int(10)",
    "authority_id": "int(10)",
    "user_name": "VARCHAR(250)",
    "user_sex_id": "int(10)",
    "user_age": "int(10)",
    "email": "VARCHAR(250)",
}
"""
user_table = "user_table"
user_table_id = "id"
user_table_authority_id = "authority_id"
user_table_user_name = "user_name"
user_table_user_sex_id = "user_sex_id"
user_table_user_age = "user_age"
user_table_email = "email"
# 这个表用来标记性别，性别表：1 男  2 女
"""
user_sex = {
    "sex_id": "int(10) ",
    "sex": "VARCHAR(250)",
}
"""
user_sex = "user_sex"
user_sex_sex_id = "sex_id"
user_sex_sex = "sex"
# user_authority 权限表，分为bigroot、root、user三个级别对应1、2、3
"""
user_authority = {
    "authority_id": "int(10)",
    "authority": "VARCHAR(250)",
}
"""
user_authority = "user_authority"
user_authority_authority_id = "authority_id"
user_authority_authority = "authority"
# 用户评论数据表
"""
user_comment = {
    "user_id": "int(10)",
    "comment_link": "text",
    "comment": "text",
    "comment_id": "VARCHAR(250)",
    "date": "text"
}
"""
user_comment = "user_comment"
user_comment_comment_id = "comment_id"
user_comment_user_id = "user_id"
user_comment_comment_link = "comment_link"
user_comment_comment = "comment"
user_comment_date = "date"

# 这个表用来支撑主页，主页回列出所有文章

"""
user_data = {
        "article_id": "VARCHAR(250)",
        "user_id": "text",
        "article_title": "text",
        "article_introduce": "text",
        "article_link": "text",
        "date": "text",
    }
"""
user_data = "user_data"
user_data_article_id = "article_id"
user_data_user_id = "user_id"
user_data_article_title = "article_title"
user_data_article_introduce = "article_introduce"
user_data_article_link = "article_link"
user_data_date = "date"
"""
markdown_content = {
        "article_id": "VARCHAR(250)",
        "user_id": "text",
        "content": "text",
        "content_date": "text",
    }
"""
# 保存文章内容的表
markdown_content = "markdown_content"
markdown_content_article_id = "article_id"
markdown_content_user_id = "user_id"
markdown_content_content = "content"
markdown_content_content_data = "content_date"
# user_view_number 文章浏览量、点瓒数量
"""
user_view_number = {
    "article_id": "VARCHAR(250)",
    "user_id": "VARCHAR(250)",
    "view_number": "VARCHAR(250)",
    "like_number": "VARCHAR(250)",
}
"""
user_view_number = "user_view_number"
user_view_number_article_id = "article_id"
user_view_number_user_id = "user_id"
user_view_number_view_number = "view_number"
user_view_number_like_number = "like_number"
"""
    # number_of_visits 博客留言表
    number_of_visits = {
        "user_id": "VARCHAR(250)",
        "book": "text",
        "book_id": "VARCHAR(250)",
        "date": "text"
    }
"""
number_of_visits = "number_of_visits"
number_of_visits_user_id = "user_id"
number_of_visits_book = "book"
number_of_visits_book_id = "book_id"
number_of_visits_date = "date"
"""
    # 用户留言
    guest_book = {
        "user_id": "VARCHAR(250)",
        "book": "text",
        "book_id": "VARCHAR(250)",
        "date": "text"
    }
"""
guest_book = "guest_book"
guest_book_user_id = "user_id"
guest_book_book = "book"
guest_book_book_id = "book_id"
guest_book_date = "date"