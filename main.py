# main.py

import os
import time
import re
import logging
import requests
import uuid
import base64
import threading
from io import BytesIO
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from word2number import w2n

# Flask apps
from flask import Flask

from voucher import voucher_app, run_voucher_app

# DB operations
from database import init_db, insert_extracted_receipt, insert_or_update_brochure

# Load environment
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AZURE_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_VISION_KEY")
API_URL = AZURE_ENDPOINT + 'vision/v3.2/read/analyze'

# Logging
logging.basicConfig(level=logging.INFO)

# State management
user_images = {}
user_state = {}


# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["start"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("📸 Send a receipt image (UPI or Voucher):", reply_markup=reply_markup)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🖼️ Image received.", reply_markup=ReplyKeyboardRemove())
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_bytes = await file.download_as_bytearray()
        user_id = update.message.from_user.id
        user_images[user_id] = file_bytes
        user_state[user_id] = {"stage": "main_category"}
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 UPI", callback_data="upi")],
            [InlineKeyboardButton("📄 Voucher", callback_data="voucher")]
        ])
        await update.message.reply_text("🔘 Choose the receipt type:", reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Image error: {e}")
        await update.message.reply_text("❌ Failed to process image.")

def extract_text_from_image(image_stream):
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_KEY,
        'Content-Type': 'application/octet-stream'
    }
    response = requests.post(API_URL, headers=headers, data=image_stream.getvalue())
    if response.status_code != 202:
        return None
    operation_url = response.headers['Operation-Location']
    while True:
        result = requests.get(operation_url, headers=headers).json()
        if result.get('status') == 'succeeded':
            break
        elif result.get('status') == 'failed':
            return None
        time.sleep(1)
    lines = []
    for read_result in result['analyzeResult']['readResults']:
        for line in read_result['lines']:
            lines.append(line['text'])
    logging.info("OCR Output:\n%s", '\n'.join(lines))
    return "\n".join(lines)


# Extract limited fields based on category
def extract_limited_fields(text, category):
    return "\n".join([
        f"• Amount: {extract_amount(text)}",
        f"• Date & Time: {extract_datetime(text)}",
        f"• Transaction ID: {extract_transaction_id(text)}",
        f"• Person Name: {extract_person_name(text)}",
        f"• UPI ID: {extract_upi_id(text)}"
    ])

# Extract amount like ₹1,234.56
def extract_amount(text):
    match = re.search(r'₹\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?', text)
    return match.group(0).strip() if match else "Not Found"

# Extract datetime from formats like "28 Feb 2025, 21:39" or "21:39 on 28 Feb 2025"
def extract_datetime(text):
    # Pattern 1: 21:39 on 28 Feb 2025
    match = re.search(r'(\d{1,2}:\d{2})\s+on\s+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})', text)
    if match:
        return f"{match.group(1)} on {match.group(2)}"
    
    # Pattern 2: 28 Feb 2025, 21:39
    match = re.search(r'(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}),?\s+(\d{1,2}:\d{2})', text)
    if match:
        return f"{match.group(2)} on {match.group(1)}"

    # Fallback: DD/MM/YYYY HH:MM
    match = re.search(r'\d{1,2}/\d{1,2}/\d{4}[ \t]+\d{1,2}:\d{2}', text)
    return match.group(0).strip() if match else "Not Found"

# Extract transaction ID (12+ alphanumeric characters, often UPI format)
def extract_transaction_id(text):
    match = re.search(r'\b([A-Z0-9]{12,})\b', text)
    return match.group(1) if match else "Not Found"

# Extract person name from lines like "Paid to\nNAME" or "Banking Name: NAME"
def extract_person_name(text):
    # Try 1: "Paid to\nRITIKESH MALIK"
    match = re.search(r'Paid to\s*\n?\s*([A-Z][A-Z\s.]{3,})', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Try 2: "Banking Name : RITIKESH MALIK"
    match = re.search(r'Banking Name\s*[:\-]\s*([A-Z][A-Z\s.]{3,})', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Try 3: Any standalone uppercase full name (fallback for OCR receipts)
    match = re.search(r'\b([A-Z]{3,}(?:\s+[A-Z]{3,})+)\b', text)
    if match:
        return match.group(1).strip()

    return "Not Found"

# Extract UPI ID like xyz@upi
def extract_upi_id(text):
    match = re.search(r'\b[\w.\-]+@[\w]+\b', text)
    return match.group(0).strip() if match else "Not Found"

# Callback handler for inline buttons
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if user_id not in user_images:
        await query.edit_message_text("❌ Please send a receipt image first.")
        return

    stage = user_state.get(user_id, {}).get("stage")

    if stage == "main_category":
        if data == "upi":
            user_state[user_id]["stage"] = "upi_subtype"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("\U0001F7E3 PhonePe", callback_data="PhonePe"),
                InlineKeyboardButton("\U0001F537 Paytm", callback_data="Paytm"),
                InlineKeyboardButton("\U0001F535 GooglePay", callback_data="GooglePay")]
            ])
            await query.edit_message_text("💡 Choose UPI type:", reply_markup=keyboard)
        else:
            user_state[user_id]["stage"] = "final"
            await process_receipt(query, user_id, category=data)

    elif stage == "upi_subtype":
        user_state[user_id]["stage"] = "final"
        await process_receipt(query, user_id, category=data)

async def process_receipt(query, user_id, category):
    try:
        image_stream = BytesIO(user_images.pop(user_id))
        text = extract_text_from_image(image_stream)
        if not text or len(text.strip()) < 10:
            await query.edit_message_text("⚠️ Image is unclear or unreadable.")
            return
        if category in ["PhonePe", "Paytm", "GooglePay"]:
            formatted = extract_limited_fields(text, category)
            fields = {}
            for line in formatted.splitlines():
                if line.startswith("• "):
                    try:
                        key, val = line[2:].split(":", 1)
                        fields[key.strip()] = val.strip()
                    except ValueError:
                        continue
            session_id = str(uuid.uuid4())
            # image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
            # user_data[session_id] = {
            #     "fields": fields,
            #     "image_base64": image_base64,
            #     "timestamp": time.time()
            # }
            insert_extracted_receipt(user_id, category, fields)
            link = f"http://192.168.1.3:5001/voucher?startapp=1"
            await query.edit_message_text(f"✅ Data saved and waiting for voucher....\n\n🌐 Fill voucher: {link}")
        else:
            await query.edit_message_text("⚠️ Unsupported category.")
    except Exception as e:
        logging.error(f"❌ Processing error: {e}")
        await query.edit_message_text("❌ Error while processing receipt.")


# 👇 Add this at the end of main.py (before `if __name__ == "__main__"`):
def start_voucher_server():
    thread = threading.Thread(
        target=run_voucher_app,
        kwargs={'host': '0.0.0.0', 'port': 5001, 'use_reloader': False},
        daemon=True
    )
    thread.start()

# Main
if __name__ == "__main__":
    init_db()
    start_voucher_server()  # ✅ Start the Flask voucher server
    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app_telegram.add_handler(CallbackQueryHandler(handle_callback))
    app_telegram.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), start))
    app_telegram.run_polling()

