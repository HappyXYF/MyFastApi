from fastapi import FastAPI, HTTPException
import pyodbc
from typing import List, Optional
import uvicorn
from pydantic import BaseModel
from models.client_model import Client

app = FastAPI()

# 数据库连接配置
# 在Linux环境下，使用HOST\\INSTANCE格式可能无法工作，尝试使用HOST,PORT格式
DB_SERVER = "HAPPY_XU\SQLEXPRESS,49772"  # SQL Server默认端口为1433
DB_NAME = "GT_DB_Epi5"
DB_USER = "sa"
DB_PASSWORD = "pw1234"
DB_DRIVER = "{ODBC Driver 17 for SQL Server}"

# 构建连接字符串
def get_connection_string():
    # 添加超时设置和其他连接选项
    return f"DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD};TrustServerCertificate=yes;Connection Timeout=30;Login Timeout=30"

# 检查ODBC驱动是否可用
def check_odbc_driver():
    try:
        global DB_DRIVER
        drivers = pyodbc.drivers()
        if DB_DRIVER not in drivers:
            # 尝试使用其他可用的SQL Server驱动
            for driver in drivers:
                if 'SQL Server' in driver:
                    DB_DRIVER = "{" + driver + "}"
                    return True
            return False
        return True
    except Exception:
        return False

# # 定义Client模型
# class Client(BaseModel):
#     id: Optional[int] = None
#     name: str
#     email: str
#     phone: Optional[str] = None
#     address: Optional[str] = None
    
#     class Config:
#         orm_mode = True

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon"}

# 获取所有Client
@app.get("/clients", response_model=List[Client])
async def get_clients():
    try:
        if not check_odbc_driver():
            raise HTTPException(status_code=500, detail="SQL Server ODBC driver not found. Please install the ODBC Driver 17 for SQL Server.")
        conn = pyodbc.connect(get_connection_string())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Client")
        columns = [column[0] for column in cursor.description]
        clients = []
        for row in cursor:
            client_dict = dict(zip(columns, row))
            clients.append(Client(**client_dict))
        conn.close()
        return clients
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 根据ID获取特定Client
@app.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: int):
    try:
        if not check_odbc_driver():
            raise HTTPException(status_code=500, detail="SQL Server ODBC driver not found. Please install the ODBC Driver 17 for SQL Server.")
        conn = pyodbc.connect(get_connection_string())
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Client WHERE ClientID = {client_id}")
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Client not found")
        columns = [column[0] for column in cursor.description]
        client_dict = dict(zip(columns, row))
        conn.close()
        return Client(**client_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 创建新的Client
@app.post("/clients", response_model=Client)
async def create_client(client: Client):
    try:
        if not check_odbc_driver():
            raise HTTPException(status_code=500, detail="SQL Server ODBC driver not found. Please install the ODBC Driver 17 for SQL Server.")
        conn = pyodbc.connect(get_connection_string())
        cursor = conn.cursor()
        # 假设Client表有name, email, phone, address字段
        query = """
        INSERT INTO Client (name, email, phone, address)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, client.name, client.email, client.phone, client.address)
        conn.commit()
        # 获取新创建的Client的ID
        cursor.execute("SELECT @@IDENTITY")
        client_id = cursor.fetchone()[0]
        client.id = client_id
        conn.close()
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 更新Client
@app.put("/clients/{client_id}", response_model=Client)
async def update_client(client_id: int, client: Client):
    try:
        if not check_odbc_driver():
            raise HTTPException(status_code=500, detail="SQL Server ODBC driver not found. Please install the ODBC Driver 17 for SQL Server.")
        conn = pyodbc.connect(get_connection_string())
        cursor = conn.cursor()
        # 检查Client是否存在
        cursor.execute(f"SELECT * FROM Client WHERE id = {client_id}")
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Client not found")
        # 更新Client
        query = """
        UPDATE Client
        SET name = ?, email = ?, phone = ?, address = ?
        WHERE id = ?
        """
        cursor.execute(query, client.name, client.email, client.phone, client.address, client_id)
        conn.commit()
        client.id = client_id
        conn.close()
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 删除Client
@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    try:
        if not check_odbc_driver():
            raise HTTPException(status_code=500, detail="SQL Server ODBC driver not found. Please install the ODBC Driver 17 for SQL Server.")
        conn = pyodbc.connect(get_connection_string())
        cursor = conn.cursor()
        # 检查Client是否存在
        cursor.execute(f"SELECT * FROM Client WHERE id = {client_id}")
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Client not found")
        # 删除Client
        cursor.execute(f"DELETE FROM Client WHERE id = {client_id}")
        conn.commit()
        conn.close()
        return {"message": "Client deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8009)
