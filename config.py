#encoding=utf-8
import  MySQLdb
global db
global cursor
db=MySQLdb.connect ("localhost", "root", "root", "movie", charset='utf8')
cursor=db.cursor()