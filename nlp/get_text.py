from flask import Flask, request, jsonify
import boto3
import pdfplumber
import io
from dotenv import load_dotenv
import os
from sections_extraction import detect_sections

app = Flask(__name__)

@app.route('/process-resume', methods=['POST'])
def process_resume():
    data = request.json
    bucket = data['bucket']
    key = data['key']

    load_dotenv(dotenv_path="../.env.local")

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )
    obj = s3.get_object(Bucket=bucket, Key=key)
    pdf_content = obj['Body'].read()

    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'

    
    return jsonify({"text": detect_sections(text)})

if __name__ == '__main__':
    app.run(host="localhost", port=5000)
