import os
import logging
import psycopg2
import base64
import uuid
from flask import Flask, render_template_string, request, jsonify, send_file
from datetime import datetime
from io import BytesIO
from email.message import EmailMessage
import smtplib



# Shared storage for session data
voucher_data = {}

# Flask app
voucher_app = Flask(__name__)


LOGO_PATH = "static/logo.png"

# Database Config
DATABASE_CONFIG = {
    'host': 'bcpostgressqlserver.postgres.database.azure.com',
    'database': 'Bfl_ocr',
    'user': 'Vertoxlabs',
    'password': 'Vtx@2025',
}

VOUCHER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Voucher</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            border: 2px solid #000;
            padding: 20px;
        }
        h2, h3, h4 {
            text-align: center;
            margin: 5px 0;
        }
        h4 {
            font-size: 14px;
            font-weight: normal;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 20px;
            flex-wrap: wrap;
        }
        .header img {
            max-height: 80px;
            width: auto;
            height: auto;
            max-width: 120px;
            flex-shrink: 0;
        }
        .header-text {
            flex: 1;
        }
        @media (max-width: 600px) {
            .header {
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            .header img {
                max-width: 80px;
            }
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        td {
            padding: 8px;
            border: 1px solid #000;
        }
        .label {
            font-weight: bold;
            width: 30%;
        }
        .input {
            width: 100%;
            border: none;
            font-size: 16px;
        }
        .input:focus {
            outline: none;
            border-bottom: 1px solid #000;
        }
        .signature {
            margin-top: 40px;
            text-align: right;
        }
        .btn {
            margin-top: 20px;
            background: #007bff;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .btn:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="/static/logo.png" alt="Company Logo">
        <div class="header-text">
            <h2>BARIFLO CYBERNETICS PRIVATE LIMITED</h2>
            <h4>CIN - U74999OR 2018PTC029923, ROOM NO-207, TB1-2, KIIT TBI, PATIA, BHUBANESWAR, ODISHA</h4>
            <h3>PAYMENT VOUCHER</h3>
        </div>
    </div>

    <table>
        <tr>
            <td class="label">Sl. No.</td>
            <td><input type="text" id="slno" class="input" value="{{ data.get('Sl No', '') }}"></td>
            <td class="label">Date</td>
            <td><input type="date" id="date" class="input" value="{{ data.get('Date', '') }}"></td>
        </tr>
        <tr>
            <td class="label">Name of the Account</td>
            <td colspan="3"><input type="text" id="account_name" class="input" value="{{ data.get('Name of the Account', '') }}"></td>
        </tr>
        <tr>
            <td class="label">Type of Expenses</td>
            <td colspan="3"><input type="text" id="debit" class="input" value="{{ data.get('DEBIT', '') }}"></td>
        </tr>
        <tr>
            <td class="label">Transaction ID</td>
            <td colspan="3"><input type="text" id="credit" class="input" value="{{ data.transaction_id or '' }}"></td>
        </tr>
        <tr>
            <td class="label">Amount (Rs.)</td>
            <td colspan="3"><input type="text" id="amount" class="input" value="{{ data.amount or '' }}"></td>
        </tr>
      <tr>
            <td class="label">Time</td>
            <td colspan="3"><input type="time" id="time" class="input" value="{{ data.get('Time', '') }}"></td>
        </tr>
        <tr>
            <td class="label">Reason</td>
            <td colspan="3">
                <select id="reason" class="input">
                    <option value="">-- Select Reason --</option>
                    <option value="Diesel purchases" {% if data.get('Reason') == 'Diesel purchases' %}selected{% endif %}>Diesel purchases</option>
                    <option value="Labour Charges" {% if data.get('Reason') == 'Labour Charges' %}selected{% endif %}>Labour Charges</option>
                    <option value="Consumables and raw materials" {% if data.get('Reason') == 'Consumables and raw materials' %}selected{% endif %}>Consumables and raw materials</option>
                    <option value="Travel expenses" {% if data.get('Reason') == 'Travel expenses' %}selected{% endif %}>Travel expenses</option>
                </select>
            </td>
        </tr>
        <tr>
            <td class="label">The items/services were procured from</td>
            <td colspan="3"><input type="text" id="procured_from" class="input" value="{{ data.get('Procured From', '') }}"></td>
        </tr>
        <tr>
            <td class="label">Location</td>
            <td colspan="3"><input type="text" id="location" class="input" value="{{ data.get('Location', '') }}"></td>
        </tr>
        
        <tr>
            <td class="label">Additional Receipt</td>
            <td colspan="3"><input type="file" id="additional_receipt" class="input" accept="image/*,application/pdf"></td>
        </tr>
        <tr>
            <td class="label">Additional Location</td>
            <td colspan="3"><input type="file" id="additional_receipt2" class="input" accept="image/*,application/pdf"></td>
        </tr>
        <tr>
            <td class="label">Upload Stamp</td>
            <td colspan="3"><input type="file" id="upload_stamp" class="input" accept="image/*,application/pdf"></td>
        </tr>
    </table>

    <div class="signature">
        <label>Receiver Signature:</label>
        <input type="text" id="receiver_signature" class="input" value="{{ data.get('Receiver Signature', '') }}">
    </div>

    <button class="btn" onclick="saveVoucher()">Save Voucher</button>

   <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
   <script src="/static/savePDF.js"></script>

<script>
    function saveVoucher() {
        const form = document.body;

        html2canvas(form).then(canvas => {
            const imageData = canvas.toDataURL('image/png');

            const formData = new FormData();
            formData.append('image_data', imageData);
            formData.append('slno', document.getElementById('slno').value);
            formData.append('date', document.getElementById('date').value);
            formData.append('account_name', document.getElementById('account_name').value);
            formData.append('debit', document.getElementById('debit').value);
            formData.append('credit', document.getElementById('credit').value);
            formData.append('amount', document.getElementById('amount').value);
            formData.append('time', document.getElementById('time').value);
            formData.append('reason', document.getElementById('reason').value);
            formData.append('procured_from', document.getElementById('procured_from').value);
            formData.append('location', document.getElementById('location').value);
            formData.append('receiver_signature', document.getElementById('receiver_signature').value);

            const fileInput1 = document.getElementById('additional_receipt');
            if (fileInput1.files.length > 0) {
                formData.append('additional_receipt', fileInput1.files[0]);
            }
            const fileInput3 = document.getElementById('additional_receipt2');
            if (fileInput3.files.length > 0) {
                formData.append('additional_receipt2', fileInput3.files[0]);
            }

            const fileInput2 = document.getElementById('upload_stamp');
            if (fileInput2.files.length > 0) {
                formData.append('upload_stamp', fileInput2.files[0]);
            }

            // 🔁 Change this to fetch and then trigger PDF
            fetch(`/save_voucher`, {
                method: 'POST',
                body: formData
            })
            .then(resp => {
                if (!resp.ok) throw new Error("Server error");
                return resp.json();
            })
            .then(result => {
                if (!result.record_id) {
                    throw new Error("No record ID returned from server.");
                }

                // 1️⃣ Download PNG image from voucher image endpoint
                fetch(`/voucher_image/${result.record_id}`)
                    .then(imgResp => {
                        if (!imgResp.ok) throw new Error("Failed to fetch voucher image.");
                        return imgResp.blob();
                    })
                    .then(blob => {
                        const imageLink = document.createElement('a');
                        imageLink.href = URL.createObjectURL(blob);
                        imageLink.download = "voucher.png";
                        document.body.appendChild(imageLink);
                        imageLink.click();
                        imageLink.remove();

                        // 2️⃣ Generate and download PDF
                        savePDF(result.record_id, () => {
                            alert("✅ Voucher saved and PDF downloaded!");
                        });
                    })
                    .catch(imgErr => {
                        console.error(imgErr);
                        alert("⚠️ Voucher saved, but image fetch failed.");
                        // Still generate the PDF even if image failed
                        savePDF(result.record_id, () => {
                            alert("✅ Voucher saved and PDF downloaded!");
                        });
                    });
            })
            .catch(err => {
                console.error(err);
                alert("❌ Failed to save voucher.");
            });

        });
    }
</script>

</body>
</html>
"""

from flask import Flask, render_template_string, request, jsonify, send_file
from datetime import datetime
from io import BytesIO

# Shared storage for session data
voucher_data = {}

# Flask app
voucher_app = Flask(__name__)

# Path to your logo file (place logo.png in a folder called 'static')
LOGO_PATH = "static/logo.png"

# Database Config
DATABASE_CONFIG = {
    'host': 'bcpostgressqlserver.postgres.database.azure.com',
    'database': 'Bfl_ocr',
    'user': 'Vertoxlabs',
    'password': 'Vtx@2025',
}

# Initialize the database
def init_db():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS brochure (
                id SERIAL PRIMARY KEY,
                slno TEXT,
                date TEXT,
                account_name TEXT,
                debit TEXT,
                credit TEXT,
                amount TEXT,
                time TEXT,
                reason TEXT,
                procured_from TEXT,
                location TEXT,
                additional_receipt BYTEA,
                additional_receipt2 BYTEA,
                upload_stamp BYTEA,
                receiver_signature TEXT,
                image BYTEA,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        logging.info("✅ Database initialized.")
    except Exception as e:
        logging.error(f"❌ Failed to init DB: {e}")

# 👇 Render empty voucher form
@voucher_app.route("/voucher", methods=["GET"])
def voucher_form():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT slno FROM brochure ORDER BY id DESC LIMIT 1;")
        last_slno_row = cur.fetchone()

        # Extract number from last slno
        if last_slno_row and last_slno_row[0].startswith("BCPL"):
            last_num = int(''.join(filter(str.isdigit, last_slno_row[0])))
            next_slno = f"BCPL{last_num + 1}"
        else:
            next_slno = "BCPL1"
        # Fetch only transaction_id and amount from the latest extracted_receipt
        cur.execute('''
            SELECT transaction_id, amount
            FROM extracted_receipts
            ORDER BY created_at DESC
            LIMIT 1;
        ''')
        row = cur.fetchone()
        cur.close()
        conn.close()
        logging.info(f"Fetched row: {row}")
        data = {
            "Sl No" : next_slno,
            "transaction_id": row[0] if row else '',
            "amount": row[1] if row else ''
        }

        return render_template_string(VOUCHER_HTML, data=data)

    except Exception as e:
        logging.error(f"❌ Failed to fetch receipt data: {e}")
        return render_template_string(VOUCHER_HTML, data={})


# 👇 Save voucher to DB after submission
@voucher_app.route('/save_voucher', methods=['POST'])
def save_voucher():
    try:
        data = request.form
        image_data_url = data.get('image_data')
        header, encoded = image_data_url.split(',', 1)
        image_bytes = base64.b64decode(encoded)

        additional_receipt = request.files.get('additional_receipt')
        print("111111111111")
        additional_receipt2 = request.files.get('additional_receipt2')
        print("2222222222222")
        upload_stamp = request.files.get('upload_stamp')
        print("33333333333333")

        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO brochure (
                slno, date, account_name, debit, credit, amount, time,
                reason, procured_from, location, additional_receipt,additional_receipt2,
                upload_stamp, receiver_signature, image
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            RETURNING id;
        ''', (
            data['slno'],
            data['date'],
            data['account_name'],
            data['debit'],
            data['credit'],
            data['amount'],
            data['time'],
            data['reason'],
            data['procured_from'],
            data['location'],
            additional_receipt.read() if additional_receipt else None,
            additional_receipt2.read() if additional_receipt2 else None,
            upload_stamp.read() if upload_stamp else None,
            data['receiver_signature'],
            psycopg2.Binary(image_bytes)
        ))
        print("444444444")
        
        record_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        # return send_file(
        #     BytesIO(image_bytes),
        #     mimetype='image/png',
        #     as_attachment=True,
        #     download_name=f"voucher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        # )
        return jsonify({"message": "✅ Voucher saved", "record_id": record_id})
    except Exception as e:
        logging.error(f"❌ Failed to save voucher: {e}")
        return jsonify({"message": "❌ Failed to save voucher."}), 500

# 🔄 Optional route: serves only image if needed later (you can delete if unused)
@voucher_app.route('/voucher_image/<int:record_id>')
def get_voucher_image(record_id):
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute('SELECT image FROM brochure WHERE id = %s', (record_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row and row[0]:
            return send_file(BytesIO(row[0]), mimetype='image/png')
        else:
            return "No image found", 404
    except Exception as e:
        logging.error(f"❌ Error retrieving voucher image: {e}")
        return "Server error", 500


@voucher_app.route('/send_pdf_email', methods=['POST'])
def send_pdf_email():
    try:
        data = request.get_json()
        pdf_base64 = data.get('pdfBase64')
        file_name = data.get('fileName', 'voucher.pdf')
        recipients = data.get('recipients', [])

        if not pdf_base64 or not recipients:
            return jsonify({'success': False, 'error': 'Missing PDF or recipients'}), 400

        pdf_bytes = base64.b64decode(pdf_base64)

        send_pdf_email_multiple(pdf_bytes, file_name, recipients)

        return jsonify({'success': True, 'message': 'Email sent'})

    except Exception as e:
        logging.error(f"❌ Error sending PDF email: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Helper function to send PDF email to multiple recipients
def send_pdf_email_multiple(pdf_bytes, file_name, recipients):
    SMTP_SERVER = 'smtp.gmail.com'   # <-- Replace with your SMTP server
    SMTP_PORT = 587                            # <-- Replace if different port is used
    SMTP_USER = 'bariflolabs@gmail.com'      # <-- Replace with your email
    SMTP_PASS = 'gpgivlqkkbyullzw'         # <-- Replace with your email password

    msg = EmailMessage()
    msg['Subject'] = 'Payment Voucher PDF'
    msg['From'] = SMTP_USER
    msg['To'] = ", ".join(recipients)
    msg.set_content('Please find the attached payment voucher PDF.')

    msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename=file_name)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)        

# Run
def run_voucher_app(host='0.0.0.0', port=5001, use_reloader=False):
    init_db()
    voucher_app.run(host=host, port=port, use_reloader=use_reloader)