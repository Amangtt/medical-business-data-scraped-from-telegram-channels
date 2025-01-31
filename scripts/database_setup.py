import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
import psycopg2
CSV_FILE_PATH="./Data/preprocessed/medical_telegram_data.csv"
# Configure logging to write to file & display in Jupyter Notebook
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("./logs/database_setup.log"),  # Log to file
        logging.StreamHandler()  # Log to Jupyter Notebook
    ]
)

# Load environment variables
load_dotenv("./.env")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")


try:
    # Establish the connection
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    
    logging.info("✅ Successfully connected to the PostgreSQL database.")
    # Create a cursor object
    cursor = connection.cursor()

    # Execute a simple query
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    logging.info('PostgreSQL version: {db_version[0]}')
    print(f"PostgreSQL version: {db_version[0]}")

      # Create a table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS medical_businesses (
        id SERIAL PRIMARY KEY,
        channel_title VARCHAR(255) NOT NULL,
        channel_username VARCHAR(100),
        message_id int,
        message TEXT,
        message_date TIMESTAMP,
        media_path TEXT,
        emoji_used TEXT,       -- New column for extracted emojis
        youtube_links TEXT 
    );
    """
    cursor.execute(create_table_query)

     # Load CSV into the table using COPY
    with open(CSV_FILE_PATH, "r", encoding="utf-8") as file:
        next(file)  # Skip the header row
        cursor.copy_expert(
            "COPY medical_businesses(channel_title, channel_username, message_id, message,message_date,media_path,emoji_used,youtube_links) FROM STDIN WITH CSV HEADER",
            file
        )
    
    
  
    connection.commit()
   
    logging.info("✅ Table 'medical_businesses' created successfully (or already exists).")
    logging.info("✅ Data successfully inserted from CSV.")

except Exception as e:
    logging.error(f"❌ Connection failed: {e}")
    print(f"❌ Connection failed: {e}")
finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    