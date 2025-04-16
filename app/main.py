from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import pandas as pd
from clickhouse_driver import Client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Data Ingestion Tool")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClickHouseConfig(BaseModel):
    host: str
    port: int
    database: str
    user: str
    jwt_token: str

class ColumnSelection(BaseModel):
    columns: List[str]

@app.post("/api/clickhouse/connect")
async def connect_clickhouse(config: ClickHouseConfig):
    try:
        client = Client(
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.jwt_token
        )
        # Test connection
        client.execute("SELECT 1")
        return {"status": "success", "message": "Connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/clickhouse/tables")
async def get_tables(config: ClickHouseConfig):
    try:
        client = Client(
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.jwt_token
        )
        tables = client.execute("SHOW TABLES")
        return {"tables": [table[0] for table in tables]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/clickhouse/columns/{table}")
async def get_columns(table: str, config: ClickHouseConfig):
    try:
        client = Client(
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.jwt_token
        )
        columns = client.execute(f"DESCRIBE TABLE {table}")
        return {"columns": [{"name": col[0], "type": col[1]} for col in columns]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/clickhouse/preview/{table}")
async def preview_data(table: str, config: ClickHouseConfig, column_selection: ColumnSelection):
    try:
        client = Client(
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.jwt_token
        )
        columns = ", ".join(column_selection.columns)
        data = client.execute(f"SELECT {columns} FROM {table} LIMIT 100")
        return {
            "columns": column_selection.columns,
            "data": [dict(zip(column_selection.columns, row)) for row in data]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/clickhouse-to-file")
async def clickhouse_to_file(config: ClickHouseConfig, table: str, column_selection: ColumnSelection):
    try:
        client = Client(
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.jwt_token
        )
        columns = ", ".join(column_selection.columns)
        data = client.execute(f"SELECT {columns} FROM {table}")
        
        df = pd.DataFrame(data, columns=column_selection.columns)
        output_file = f"{table}_export.csv"
        df.to_csv(output_file, index=False)
        
        return {
            "status": "success",
            "records_processed": len(data),
            "output_file": output_file
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/file-to-clickhouse")
async def file_to_clickhouse(
    file: UploadFile = File(...),
    config: str = Form(...),
    table_name: str = Form(...)
):
    try:
        config = ClickHouseConfig.parse_raw(config)
        client = Client(
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.jwt_token
        )
        
        # Read CSV file
        df = pd.read_csv(file.file)
        columns = df.columns.tolist()
        
        # Create table if not exists
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join([f'{col} String' for col in columns])}
        ) ENGINE = MergeTree() ORDER BY tuple()
        """
        client.execute(create_table_query)
        
        # Insert data
        data = df.values.tolist()
        client.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES", data)
        
        return {
            "status": "success",
            "records_processed": len(data)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 