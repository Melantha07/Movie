#encoding=utf-8
__author__ = 'miaoshasha'
#---------脚本为：爬取电影数据--------------------
import requests
import json
import xlwt
import sys
import MySQLdb
import uuid
from  config import db,cursor
reload(sys)
sys.setdefaultencoding('UTF-8')

#获取第page页的电影内容
def get_movie(page):
    param = {'sort': "S", "range": "0,10", 'tags': "电影", 'start': "%s" % str (20 * page), 'countries': "中国大陆"}
    r = requests.get ('https://movie.douban.com/j/new_search_subjects', params=param)
    movies_list = json.loads (r.text)
    return movies_list

#解析第page页的电影内容
def parse_movie(page):
    movies_list=get_movie(page)
    movie = {}
    for i in range (0, len (movies_list["data"])):
        m = {
            "directors": ','.join ( movies_list["data"][i]["directors"]),
            "title": movies_list["data"][i]["title"],
            "rate": movies_list["data"][i]["rate"],
            "casts": ','.join (movies_list["data"][i]["casts"]),
            "cover": movies_list["data"][i]["cover"]
        }
        movie[i] = m
    return movie

#解析的电影初始数据存入数据库表里
def write_to_db():
    #爬取50页的电影数据，可自行修改页数
    for j in range (0, 50):
        movie=parse_movie(j)
        for i in range(0,len(movie)):
            id=str(uuid.uuid1()).replace('-','')
            # SQL 插入语句
            sql = "INSERT INTO movie_actor(id,directors,title, rate, casts,cover) \
                           VALUES ('%s','%s', '%s', '%s' , '%s','%s')" % \
                  (id,movie[i]["directors"], movie[i]["title"], movie[i]["rate"], movie[i]["casts"],movie[i]["cover"])
            try:
                # 执行sql语句
                cursor.execute (sql)
                # 提交到数据库执行
                db.commit ()
                print "-------插入%s成功------------" % str ((i+1)+j*20)
            except:
                # 发生错误时回滚
                print "-------插入%s失败-------------" % str (i)
                db.rollback ()
    # 关闭数据库连接
    db.close ()

# def cast_relation_db():
#     sql = '''SELECT CASTS FROM MOVIE'''
#     c = []
#     b = []
#     try:
#         # 执行sql语句
#         cursor.execute (sql)
#         results = cursor.fetchall ()
#     except:
#         print "Error: unable to fecth data"
#     # 关闭数据库连接
#     db.close ()
#     for row in results:
#         caster = row[0]
#         b = caster.split (",")
#         for i in range (0, len (b)):
#             c.append (b[i])
#             for i in range (0, len (c)):
#                 if c[i] == cast:
#                     del c[i]
#     m = list (set (c))
#     b={}
#     for i in range (0, len (m)):
#          b[i]=({'cast': m[i],'count': c.count (m[i])})



def main():
    write_to_db()
    #cast_relation_db ()

if __name__ == '__main__':
    main()





