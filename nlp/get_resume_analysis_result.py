from flask import Flask, request, jsonify
import boto3
import pdfplumber
import io
from dotenv import load_dotenv
import os
from structural_analysis import structural_analysis
from contextual_analysis import contextual_analysis
from structural_analysis import nlp
from docx import Document
import requests
import re

app = Flask(__name__)

SECTION_KEYWORDS = ["profile", "professional experience", "experience", "education", "skills", "skills & abilities", "skills and abilities", "projects", "certifications", "summary", "contact", "languages", "awards", "strenghts", "courses", "tools", "hobbies", "activities and interests"]
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
PDF_MIME = "application/pdf"

@app.route('/process-resume', methods=['POST'])
def process_resume():
    data = request.json
    file_url = data["url"]
    file_type = data['fileType']

    load_dotenv(dotenv_path="../.env.local")

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    response = requests.get(file_url)
    file_content = response.content
    text = ""

    if file_type == PDF_MIME:
        text = get_content_pdf(file_content)

    elif file_type == DOCX_MIME:
        text = get_content_docx(file_content)

    if len(text) < 1500 or len(text) > 12000:
        return({"process_result": {"structural": "The number of characters in your resume does not meet the standards. It is either too long or too short."}})

    parsed_sections = detect_sections(text)
    analysis_result =  result_analysis(parsed_sections, file_content, file_type)

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

def result_analysis(parsed_sections, text, file_type):
    process_result = {}
    process_result["structural"] = structural_analysis(parsed_sections, text, file_type)
    process_result["contextual"] = contextual_analysis(parsed_sections)

    return process_result

def get_content_pdf(pdf_content):
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + '\n'

    return text

def get_content_docx(docx_content):
    text = ""
    for para in Document(io.BytesIO(docx_content)).paragraphs:
        text += para.text.strip() + '\n'

    return text

if __name__ == '__main__':
    app.run(host="localhost", port=5000)
