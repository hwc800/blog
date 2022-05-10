

import pymysql


class DatabaseOperation(object):

    def __init__(self, ip, user, pwd, database, charset="utf8", port=3306):
        conn = pymysql.connect(host=ip, password=pwd, database=database, user=user, charset=charset, port=port)
        self.conn = conn
        pass

    def creat_table(self, table_name=None, fiels=None, primary_key="id"):
        """
        创建数据表调用时，需注意fiels为字典，key为字段名，value为字段类型和限制条件如：fiels={"id": "INT UNSIGNED AUTO_INCREMENT", "one": "int(12)", "two": "VARCHAR(100) NOT NULL"}
        table_name参数意如其名，数据表的名字
        primary_key字段为要设置的主键，默认为id（这个字段需要存在才能设置主键为id）
        """
        num = 0
        fiel_data = ""
        for key, value in fiels.items():
            num += 1

            if num == 1:
                fiel_data += key + " " + value + ","

            else:
                fiel_data += key + " " + value + ","

        sql = "CREATE TABLE IF NOT EXISTS %s(%s PRIMARY KEY ( `%s` ))ENGINE=InnoDB DEFAULT CHARSET=utf8;;" % (table_name, fiel_data, primary_key)
        curs = self.conn.cursor()
        curs.execute(sql)
        print("数据表添加成功。")

    def insert(self, table_name, need_insert_fiels_and_data=None):
        """need_insert_fiels_and_data: 这个参数是字典,字段是key，值是value"""

        need_insert_keys = " "
        need_insert_values = " "
        run_for_tage = 0

        for key, value in need_insert_fiels_and_data.items():
            run_for_tage += 1

            if run_for_tage == len(need_insert_fiels_and_data):
                need_insert_keys += "%s" % key
                if type(value) == int:
                    need_insert_values += "%s" % value
                elif type(value) == str:
                    need_insert_values += "'%s'" % value
                elif type(value) == bool:
                    need_insert_values += "%s" % value
                else:
                    need_insert_values += "'%s'" % value

            else:
                need_insert_keys += "%s, " % key
                if type(value) == int:
                    need_insert_values += "%s, " % value
                elif type(value) == str:
                    need_insert_values += "'%s', " % value
                elif type(value) == bool:
                    need_insert_values += "%s, " % value
                else:
                    need_insert_values += "'%s', " % value

        sql = "insert into %s (%s) values (%s);" % (table_name, need_insert_keys, need_insert_values)
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        print("insert table %s is success;" % table_name)

    def updata_table(self, table_name=None, need_update_file_names_and_datas=None, where_is_files=None):
        """
        这个函数用于修改数据表,参数是字典
        need_update_file_names_and_datas:key为要修改的字段名，value是对应字段要更新的数据
        where_is_files:  修改的条件(字段为字典)
        """
        num = 0
        number = 0
        files_and_value = ""
        where_file_and_value = ""

        for key, value in need_update_file_names_and_datas.items():
            num += 1

            if num == len(need_update_file_names_and_datas):

                if type(value) == int:
                    files_and_value += "%s=%s" % (key, value)
                elif type(value) == str:
                    files_and_value += "%s='%s'" % (key, value)
                elif type(value) == bool:
                    files_and_value += "%s=%s" % (key, value)
                else:
                    files_and_value += "%s='%s'" % (key, value)

            else:
                if type(value) == int:
                    files_and_value += "%s=%s," % (key, value)
                elif type(value) == str:
                    files_and_value += "%s='%s'," % (key, value)
                elif type(value) == bool:
                    files_and_value += "%s=%s," % (key, value)
                else:
                    files_and_value += "%s='%s'," % (key, value)

        for key, value in where_is_files.items():
            number += 1

            if number == len(where_is_files):
                if type(value) == int:
                    where_file_and_value += "%s=%s" % (key, value)
                elif type(value) == str:
                    where_file_and_value += "%s='%s'" % (key, value)
                elif type(value) == bool:
                    where_file_and_value += "%s=%s" % (key, value)
                else:
                    where_file_and_value += "%s='%s'" % (key, value)

            else:
                if type(value) == int:
                    where_file_and_value += "%s=%s" % (key, value)
                elif type(value) == str:
                    where_file_and_value += "%s='%s'" % (key, value)
                elif type(value) == bool:
                    where_file_and_value += "%s=%s" % (key, value)
                else:
                    where_file_and_value += "%s='%s'" % (key, value)

        sql = "UPDATE %s SET %s where %s;" % (table_name, files_and_value, where_file_and_value)
        self.conn.cursor().execute(sql)
        self.conn.commit()

    def add_file(self, table_name, field_name, class_and_condition):
        """新增一个字段： table_name：表名； field_name：字段名； class_and_condition：约束条件和字段类型（用标准格式写，如：int(12)、int(12) not null等）"""
        sql = "ALTER TABLE %s ADD %s %s" % (table_name, field_name, class_and_condition)
        print(sql)

        self.conn.cursor().execute(sql)

    def change_field_name(self, table_name, old_name, new_name, new_field_class):
        sql = "ALTER TABLE %s CHANGE %s %s %s;" % (table_name, old_name, new_name, new_field_class)
        print(sql)
        self.conn.cursor().execute(sql)

    def close_db(self):
        self.conn.close()

    def commit_option(self):
        self.conn.commit()

    def __del__(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    """
    在这里执行或调试
    不要随便动已经存在的表，测试前先确认已经存在的表有哪些
    """
    build_cersion_fiels = {
        "id": "INT UNSIGNED AUTO_INCREMENT",
         "TopTwo": "VARCHAR(40)",
         "TopThree": "VARCHAR(40)",
         "third": "int(10)",
         "fourth": "int(10)",
         "version": "VARCHAR(124)",
         "tag": "VARCHAR(225)",
         "pipeline": "VARCHAR(250)",
         "apkversion": "VARCHAR(124)",
         "BuildClass": "VARCHAR(124)",
         "CommitId": "VARCHAR(250)",
         "UpdaterChannelID": "int(12)",
         "PufferChannelId": "int(12)",
             }
    build_arges_files = {
        "id": "INT UNSIGNED AUTO_INCREMENT",
        "version": "VARCHAR(124)",
        "pipeline": "VARCHAR(250)",
        "arges": "TEXT",
    }

    version_code_files = {
        "id": "int(10)",
        "authority_id": "int(10)",
        "user_name": "VARCHAR(250)",
        "user_sex_id": "int(10)",
        "user_age": "int(10)",
        "email": "VARCHAR(250)",
    }
    # 这个表用来标记性别，性别表：1 男  2 女
    user_sex = {
        "sex_id": "int(10) ",
        "sex": "VARCHAR(250)",
    }
    # user_authority 权限表，分为bigroot、root、user三个级别对应1、2、3
    user_authority = {
        "authority_id": "int(10)",
        "authority": "VARCHAR(250)",
    }

    # 用户评论数据表
    user_comment = {
        "user_id": "int(10)",
        "comment_link": "text",
        "comment": "text",
        "comment_id": "VARCHAR(250)",
        "date": "text"
    }
    # 这个表用来支撑主页，主页回列出所有文章
    user_data = {
        "article_id": "VARCHAR(250)",
        "user_id": "text",
        "article_title": "text",
        "article_introduce": "text",
        "article_link": "text",
        "date": "text",
    }
    # 这个表用保存markdown文档内容
    markdown_content = {
        "article_id": "VARCHAR(250)",
        "user_id": "text",
        "content": "text",
        "content_date": "text",
    }
    #
    # conn = DatabaseOperation(ip="118.195.188.25", pwd="123456789", user="root", database="hwc")
    # conn.creat_table(table_name="user_comment", fiels=user_comment, primary_key="comment_id")

    # conn = DatabaseOperation(ip="9.135.94.3", pwd="123456789", user="root", database="version_num")
    # conn.change_field_name(table_name="version_code", old_name="center_number", new_name="top_fourth", new_field_class="varchar(125)")
    # conn.add_file(table_name="version_code", field_name="version", class_and_condition="int(12)")
    # conn.creat_table(table_name="version_code", fiels=version_code_files)
    # conn.updata_table(table_name="build_version", need_update_file_names_and_datas={"third": 4, "fourth": 1, "TopThree": "0.8.4"}, where_is_files={"id": 15})
    # conn.insert(table_name="build_version", need_insert_fiels_and_data={"third": 1, "fourth": 1, "TopThree": "0.7.1", "TopTwo": "0.7", "tag": "stable", "version": "0.7.1.1"})


    """
    CREATE TABLE IF NOT EXISTS `runoob_tbl`(
       `runoob_id` INT UNSIGNED AUTO_INCREMENT,
       `runoob_title` VARCHAR(100) NOT NULL,
       `runoob_author` VARCHAR(40) NOT NULL,
       `submission_date` DATE,
       PRIMARY KEY ( `runoob_id` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """


    def connect_db(host, db_user, pwd, db_name):
        db = pymysql.connect(host=f"{host}", user=f"{db_user}", password=f"{pwd}", db=f"{db_name}", port=3306,
                                 charset='utf8')
        return db


    # db = connect_db("118.195.188.25", "root", "123456789", "hwc")
    """
    sselect * from hwc.user_table as ut, hwc.user_authority as ua, hwc.user_sex as us where ut.user_sex_id=us.sex_id and ut.authority_id=ua.authority_id;
    多表联合查询
    """


