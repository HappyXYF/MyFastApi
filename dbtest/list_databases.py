import pyodbc
from routes.mytestapi import check_odbc_driver

# 数据库连接配置
# 在Linux环境下，使用HOST\\INSTANCE格式可能无法工作，尝试使用HOST,PORT格式
DB_SERVER = "HAPPY_XU,1433"  # SQL Server默认端口为1433 49772
DB_NAME = "GT_DB_Epi5"
DB_USER = "sa"
DB_PASSWORD = "pw1234"
# 尝试使用更旧的ODBC驱动程序，可能与SQL Server 2008更兼容
DB_DRIVER = "{ODBC Driver 17 for SQL Server}"  # 尝试使用11.0，如果没有则尝试10.0

def list_databases():
    try:
        print("检查ODBC驱动是否可用...")
        if not check_odbc_driver():
            print("错误: SQL Server ODBC驱动未找到!")
            return False

        print("尝试连接SQL Server...")
        # 连接到SQL Server但不指定特定数据库
        # 使用IP地址代替主机名，并添加更多参数解决SSL协议问题
        # 使用IP地址和端口，完全禁用SSL加密
        conn_str = f"DRIVER={DB_DRIVER};SERVER={DB_SERVER};UID={DB_USER};PWD={DB_PASSWORD};TrustServerCertificate=yes;Encrypt=no;Connection Timeout=30;Login Timeout=30;"
        print(f"连接字符串: {conn_str}")

        conn = pyodbc.connect(conn_str)
        print("成功连接到SQL Server!")

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases")
        databases = cursor.fetchall()
        print("可用数据库:")
        for db in databases:
            print(f"- {db[0]}")

        conn.close()
        return True
    except Exception as e:
        print(f"连接错误: {str(e)}")
        return False
    os.environ["FREETDSCONF"] = "/home/happyxu/myFastApiProject/MyFastApi/dbtest/freetds.conf"
    try:
        print("尝试连接SQL Server...")
        # 连接到SQL Server但不指定特定数据库
        # 使用IP地址代替主机名，并添加更多参数解决SSL协议问题
        # 使用IP地址和端口，完全禁用SSL加密
        server = "sql2008"  # 使用FreeTDS配置中定义的连接名称
        conn = pymssql.connect(
            server=server,
            user=DB_USER,
            password=DB_PASSWORD,
            timeout=30,
            as_dict=True
        )

        print("成功连接到SQL Server!")

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases")
        databases = cursor.fetchall()
        print("可用数据库:")
        for db in databases:
            print(f"- {db[0]}")

        conn.close()
        return True
    except Exception as e:
        print(f"连接错误: {str(e)}")
        return False

if __name__ == "__main__":
    list_databases()
