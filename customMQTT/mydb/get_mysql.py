import pymysql
connection = pymysql.connect(
    host='192.168.31.193',
    user='root',
    password='123456',
    db='qn',
    charset='utf8mb4',  # 防中文乱码
    cursorclass=pymysql.cursors.DictCursor  # 返回字典格式
)

##获取外部数据库的值
def get_mysql_outer_value()->list[tuple[str, float]]:
    rtn:list[tuple[str, float]]=[]
    with connection.cursor() as cursor:
        sql = "SELECT value,collectName FROM  qn_hedatarecv_realtimedata   ORDER BY collectTime DESC"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if len(row.get("collectName","")) >= 2:
                rtn.append((row["value"],row["collectName"]))
    #######
    return rtn


