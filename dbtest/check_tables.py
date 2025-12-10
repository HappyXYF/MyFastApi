
import pyodbc
from routes.mytestapi import get_connection_string, check_odbc_driver

def check_tables():
    try:
        print("检查ODBC驱动是否可用...")
        if not check_odbc_driver():
            print("错误: SQL Server ODBC驱动未找到!")
            return False

        print("尝试连接数据库...")
        conn_str = get_connection_string()
        conn = pyodbc.connect(conn_str)
        print("成功连接到数据库!")

        cursor = conn.cursor()
        # 检查Client表是否存在
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Client'
        """)
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("Client表存在!")
            # 获取表结构
            cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Client'")
            columns = cursor.fetchall()
            print("Client表结构:")
            for col in columns:
                print(f"- {col[0]} ({col[1]})")

            # 获取表中的记录数
            cursor.execute("SELECT COUNT(*) FROM Client")
            count = cursor.fetchone()[0]
            print(f"Client表中有 {count} 条记录")
        else:
            print("Client表不存在!")
            # 列出所有表
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            tables = cursor.fetchall()
            print("数据库中的表:")
            for table in tables:
                print(f"- {table[0]}")

        conn.close()
        return True
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

if __name__ == "__main__":
    check_tables()
