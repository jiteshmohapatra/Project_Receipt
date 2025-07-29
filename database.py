# db.py

import os
import logging
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === Database Configuration ===
DATABASE_CONFIG = {
    'host': os.getenv("DB_HOST", 'bcpostgressqlserver.postgres.database.azure.com'),
    'database': os.getenv("DB_NAME", 'Bfl_ocr'),
    'user': os.getenv("DB_USER", 'Vertoxlabs'),
    'password': os.getenv("DB_PASSWORD", 'Vtx@2025'),
}

def init_db():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()

        # Table 1: extracted_receipts
        cur.execute('''
            CREATE TABLE IF NOT EXISTS extracted_receipts (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                category VARCHAR(50),
                amount TEXT,
                datetime TEXT,
                transaction_id TEXT NULL,
                person_name TEXT,
                upi_id TEXT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Table 2: brochure
        cur.execute('''
            CREATE TABLE IF NOT EXISTS brochure (
                id SERIAL PRIMARY KEY,
                session_id UUID UNIQUE,
                slno TEXT,
                date TEXT,
                account_name TEXT,
                debit TEXT,
                credit TEXT,
                amount TEXT,
                time TEXT,
                reason TEXT,
                procured_from TEXT NULL,
                location TEXT NULL,
                additional_receipt BYTEA NULL,
                additional_receipt2 BYTEA NULL,
                upload_stamp BYTEA,
                receiver_signature TEXT,
                image BYTEA,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        conn.commit()
        cur.close()
        conn.close()
        logging.info("✅ Database initialized successfully.")
    except Exception as e:
        logging.error(f"❌ Error initializing database: {e}")

def insert_extracted_receipt(user_id, category, fields):
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO extracted_receipts (
                user_id, category, amount, datetime, transaction_id, person_name, upi_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            user_id,
            category,
            fields.get("Amount"),
            fields.get("Date & Time"),
            fields.get("Transaction ID"),
            fields.get("Person Name"),
            fields.get("UPI ID")
        ))
        conn.commit()
        cur.close()
        conn.close()
        logging.info("📝 Receipt inserted into database.")
    except Exception as e:
        logging.error(f"❌ Failed to insert receipt: {e}")

def insert_or_update_brochure(data):
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO brochure (
                session_id, slno, date, account_name, debit, credit,
                amount, time , reason, procured_from, location, receiver_signature
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''(
            data
        ))
         
        conn.commit()
        cur.close()
        conn.close()
        logging.info(f"✅ Brochure created ")
    except Exception as e:
        logging.error(f"❌ Failed to create brochure: {e}")
