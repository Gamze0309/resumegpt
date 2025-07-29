from flask import Flask, request, jsonify
import boto3
import pdfplumber
import io
from dotenv import load_dotenv
import os
from structural_analysis import structural_analysis

app = Flask(__name__)

SECTION_KEYWORDS = ["profile", "professional experience", "experience", "education", "skills", "projects", "certifications", "summary", "contact", "languages", "awards", "strenghts", "courses", "tools"]

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

    parsed_sections = detect_sections(text)
    analysis_result =  result_analysis(parsed_sections)

    return jsonify({"process_result": analysis_result})

def detect_sections(text):
    lines = text.splitlines()
    sections = {}
    current_section = "other"
    sections[current_section] = []

    for line in lines:
        stripped = line.strip().lower()
        
        if stripped in SECTION_KEYWORDS:
            current_section = stripped
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if v}

def result_analysis(parsed_sections):
    process_result = {}
    structural_analysis_result = structural_analysis(parsed_sections)
    process_result["structural"] = structural_analysis_result

    return process_result

if __name__ == '__main__':
    app.run(host="localhost", port=5000)
