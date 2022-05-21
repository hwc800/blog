
import pymysql
import blog.config_db as config_db


class MySql(object):
    def __init__(self, host, db_user, pwd, db_name):
        self.host = host
        self.db_user = db_user
        self.pwd = pwd
        self.db_name = db_name
        self.db = self._connect_db(self.host, self.db_user, self.pwd, self.db_name)

    def _connect_db(self, host, db_user, pwd, db_name):
        try:
            db = pymysql.connect(host=f"{host}", user=f"{db_user}", password=f"{pwd}", db=f"{db_name}", port=3306, charset='utf8')
        except Exception:
            raise Exception("connect failed。")
        return db

    def create(self,  sql):
        # sql = f'create table {table_name}({primary} int(124) primary key not null auto_increment{sql});'
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
        except Exception:
            raise ValueError("sql语句中的value错误。")

    def kill(self, aim_db, ips):
        import datetime

        for ip in ips:
            print(ip, datetime.datetime.now())
            cursor = self.db.cursor()
            # 查询是否有连接在一个状态超过指定时间，超过则杀掉
            sql = "SHOW PROCESSLIST;"
            try:
                cursor.execute(sql)
            except:
                raise SyntaxError("执行SHOW PROCESSLIST;语句失败")
            stat = cursor.fetchall()
            for client in stat:
                this_ip = client[2].split(":")[0]
                if client[2] != 'localhost' and client[3] == aim_db and this_ip != ip:
                    sql = f"kill {client[0]};"
                    try:
                        cursor.execute(sql)
                    except:
                        raise SyntaxError("The sql syntax error，please check be kill process does it exist.")

    def close(self):
        self.db.commit()
        self.db.close()

    def usetable(self, table_name, db_name):
        if self.istable(table_name):
            return Table(self.db, table_name, db_name)
        else:
            raise ValueError(f"传入的表:{table_name}不存在")

    def istable(self, table_name):
        cursor = self.db.cursor()
        sql = "show tables;"
        cursor.execute(sql)
        filter_tag = cursor.fetchall()
        tables = []
        for i in filter_tag:
            tables.append(i[0])
        if table_name in tables:
            return True
        else:
            return False


class Table(object):
    def __init__(self, db, table_name, db_name):
        self.db = db
        self.table = table_name
        self.db_name = db_name
        self.filename = self._field(self.db_name, self.table)

    def insert(self, **kwargs):
        # 参数为关键字参数
        key = ','.join(kwargs.keys())
        values = []
        for s in kwargs.values():
            if type(s) is int:
                values.append(str(s))
            elif type(s) is str:
                values.append(f'"{s}"')
            else:
                values.append(f'"{s}"')
        value = ','.join(values)
        cursor = self.db.cursor()
        sql = f"insert into {self.table}({key}) value ({value});"
        try:
            cursor.execute(sql)
        except:
            raise SyntaxError(f"The sql syntax error，insert failed。")

    def lock(self, pattern="write"):
        cursor = self.db.cursor()
        sql = f"lock tables {self.table} {pattern};"
        try:
            cursor.execute(sql)
        except Exception:
            raise Exception(f"lok failed，Please confirm the table {self.table} does it exist.")

    def unlock(self):
        cursor = self.db.cursor()
        sql = f"unlock tables"
        cursor.execute(sql)

    def _field(self, dbname, tablename):
        # 获取表结构
        sql = "select  table_name,column_name,column_comment  from " \
              f"information_schema.columns where table_schema ='{dbname}'  and table_name = '{tablename}';"
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
        except:
            raise ValueError(f"Please confirm {dbname},{tablename} does it exist.")
        key = cursor.fetchall()
        return key

    def max(self, version):
        sql = f"select max({version}) from {self.table}"
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
        except:
            raise ValueError(f"Please confirm the {version} field does it exist.")
        value = cursor.fetchall()
        return value

    def select(self, arr):
        sql = isql(arr)
        sql = f"select * from {self.table} where {sql};"
        fi = self.filename
        fields = []
        # 得到所有的字段名
        for ih in fi:
            fields.append(ih[1])
        cursor = self.db.cursor()
        cursor.execute(sql)
        slet = cursor.fetchall()
        # 给数据处理成键值对，然后返回
        dc = {}
        for i in slet:
            for j in range(len(i)):
                dc[fields[j]] = i[j]
        result = dc
        return result

    def multiple_select(self, arr):
        """返回全部的查询结果，每一条记录都是一个字典，装在一个列表中"""
        sql = isql(arr)
        sql = f"select * from {self.table} where {sql};"
        fi = self.filename
        fields = []
        result = []
        # 得到所有的字段名
        for ih in fi:
            fields.append(ih[1])
        cursor = self.db.cursor()
        cursor.execute(sql)
        slet = cursor.fetchall()
        # 给数据处理成键值对，然后返回
        for i in slet:
            dc = {}
            for j in range(len(i)):
                dc[fields[j]] = i[j]
            result.append(dc)
        return result

    def auto_select(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def update_table(self, need_update_file_names_and_datas=None, where_is_files=None):
        """
        这个函数用于修改数据表,参数是字典
        need_update_file_names_and_datas:key为要修改的字段名，value是对应字段要更新的数据
        where_is_files:  修改的条件(字段为字典)
        """
        num = 0
        number = 0
        files_and_value = ""
        where_file_and_value = ""
        need_update_size = len(need_update_file_names_and_datas)

        for key, value in need_update_file_names_and_datas.items():
            num += 1

            if type(value) == int:
                files_and_value += "%s=%s" % (key, value)
            elif type(value) == str:
                files_and_value += "%s='%s'" % (key, value)
            elif type(value) == bool:
                files_and_value += "%s=%s" % (key, value)
            else:
                files_and_value += "%s='%s'" % (key, value)

            if need_update_size != 1 and num != need_update_size:
                files_and_value += ","

        for key, value in where_is_files.items():
            number += 1

            if type(value) == int:
                where_file_and_value += "%s=%s" % (key, value)
            elif type(value) == str:
                where_file_and_value += "%s='%s'" % (key, value)
            elif type(value) == bool:
                where_file_and_value += "%s=%s" % (key, value)
            else:
                where_file_and_value += "%s='%s'" % (key, value)

            if len(where_is_files) != 1 and number != len(where_is_files):
                where_file_and_value += " and "

        sql = "UPDATE %s SET %s where %s;" % (self.table, files_and_value, where_file_and_value)
        cursor = self.db.cursor()
        cursor.execute(sql)


def isql(arr):
    # 处理sql语句，并组装成相应sql执行语句
    sql, op = "", 0
    for ar in arr:
        if type(ar) is str:
            kl = ar
            if op < len(arr)-1:
                sql = sql + f"{kl}" + " and "
            else:
                sql = sql + kl
        else:
            if len(ar) != 2:
                raise ValueError(f"{ar},非法格式")
            try:
                ar["op"]
            except:
                print(f"{ar}, 格式非法，请输入操作符‘op’。")
            kl, k = "", 0
            # 处理字符类型是否加单引号
            for ke in ar.keys():
                if ke != 'op' and type(ar[ke]) is int:
                    kl = f"{ke}{ar['op']}{ar[ke]}"
                elif ke != 'op':
                    kl = f"{ke}{ar['op']}'{ar[ke]}'"
                k += 1
            if op < len(arr)-1:
                sql = sql + f"{kl}" + " and "
            else:
                sql = sql + kl
        op += 1
    return sql


def or_(arr):
    kuo = "(.)"
    lunc, tag = "", 0
    for ar in arr:
        try:
            ar["op"]
        except:
            print(f"{ar}, 格式非法，请输入操作符‘op’。")
        if len(ar) != 2:
            raise ValueError(f"{ar},非法格式")
        kl, k = "", 0
        # 处理字符类型是否加单引号
        for ke in ar.keys():
            if ke != "op" and type(ar[ke]) is int:
                kl = f"{ke}{ar['op']}{ar[ke]}"
            elif ke != "op":
                kl = f"{ke}{ar['op']}'{ar[ke]}'"
            k += 1
        if tag < len(arr) - 1:
            lunc = lunc + f"{kl}" + " or "
        else:
            lunc = lunc + kl
        tag += 1
    lunc = kuo.replace(".", lunc)
    return lunc


def db_dict(filed, arr):
    ls = []
    for ar in arr:
        k = 0
        dt = {}
        for a in ar:
            dt[filed[k]] = a
            k += 1
        ls.append(dt)
    return ls


def select_user_mesg(id) -> list:
    """返回列表，每个元素都是一个字典，查询用户详情"""
    db = MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.user_table, config_db.DATABASE)
    sql = "select id,user_name,user_age,sex,authority,email from hwc.user_table as ut, hwc.user_authority as ua, " \
          "hwc.user_sex as us where ut.id=%d and ut.user_sex_id=us.sex_id and ut.authority_id=ua.authority_id;" % id
    g = table.auto_select(sql)
    f = db_dict(['id','user_name','user_age','sex','authority','email'], g)
    db.close()
    return f


def select_user_comment(comment_link):
    """
    某文章所有评论
    """
    db = MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.user_comment, config_db.DATABASE)
    result = table.multiple_select([{"comment_link": comment_link, "op": "="}])
    db.close()
    return result


def article_title(user_id=None):
    """查询文章简介表"""
    files = ["user_id", "article_title", "article_introduce", "article_link", "date", "article_id", "view_number", "like_number", "comment_number"]
    sql = "select hwc.user_data.user_id, article_title, article_introduce, article_link, date, hwc.user_data.article_id,view_number,like_number," \
          "comment_number from %s join hwc.user_view_number" \
              " on hwc.user_data.user_id=hwc.user_view_number.user_id and hwc.user_data.article_id=hwc.user_view_number.article_id;" % config_db.user_data
    if user_id:
        sql = "select hwc.user_data.user_id, article_title, article_introduce, article_link, date, hwc.user_data.article_id,view_number,like_number," \
              "comment_number from %s join hwc.user_view_number" \
              " on hwc.user_data.user_id=%s and hwc.user_data.article_id=hwc.user_view_number.article_id;" % (config_db.user_data, user_id)

    db = MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.user_data, config_db.DATABASE)
    g = table.auto_select(sql)
    result = db_dict(files, g)
    return result


def insert(tble, **kwargs):
    db = MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(tble, config_db.DATABASE)
    table.insert(**kwargs)
    db.close()
    return True


def select_markdown_content(article_id):
    """查询文章内容"""
    files = ["user_id", "content", "content_date"]
    sql = "select user_id, content, content_date from %s where article_id=%s;" % (config_db.markdown_content, article_id)
    db = MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(config_db.markdown_content, config_db.DATABASE)
    g = table.auto_select(sql)
    result = db_dict(files, g)
    return result


def select(table, **kwargs):
    db = MySql(config_db.HOST, config_db.USER, config_db.PWD, config_db.DATABASE)
    # 操作表类
    table = db.usetable(table, config_db.DATABASE)
    kes = []
    for key in kwargs:
        kes.append({key: kwargs[key], "op": "="})
    result = table.multiple_select(kes)
    return result


