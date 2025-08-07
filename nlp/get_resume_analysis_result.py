from flask import Flask, request, jsonify
import boto3
import pdfplumber
import io
from dotenv import load_dotenv
import os
from structural_analysis import structural_analysis
from docx import Document
import requests
from enums import FileContentType

app = Flask(__name__)

SECTION_KEYWORDS = ["profile", "professional experience", "experience", "education", "skills", "skills & abilities", "skills and abilities", "projects", "certifications", "summary", "contact", "languages", "awards", "strenghts", "courses", "tools", "hobbies", "activities and interests"]
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
PDF_MIME = "application/pdf"

@app.route('/process-resume', methods=['POST'])
def process_resume():
    data = request.json
    file_url = data["url"]
    fileType = data['fileType']

    load_dotenv(dotenv_path="../.env.local")

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    response = requests.get(file_url)
    file_content = response.content
    file_content_type = FileContentType.STANDARD
    text = ""

    if fileType == PDF_MIME:
        file_content_type, text = detect_multicolumn_layout_pdf(file_content)

    elif fileType == DOCX_MIME:
        file_content_type, text = detect_multicolumn_layout_docx(file_content)

    if file_content_type != FileContentType.MULTICOLUMN and file_content_type != FileContentType.TABLE :
        parsed_sections = detect_sections(text)
        analysis_result =  result_analysis(parsed_sections)

        return jsonify({"file_content_type": file_content_type.value,"process_result": analysis_result})
    else:
        return({"file_content_type": file_content_type.value})

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

def detect_multicolumn_layout_pdf(pdf_content):
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        text = ""
        for page in pdf.pages:
            words = page.extract_words()
            x_positions = [float(word['x0']) for word in words]

            if not x_positions:
                continue

            x_positions.sort()
            threshold = 50
            clusters = [[x_positions[0]]]

            for x in x_positions[1:]:
                if abs(x - clusters[-1][-1]) > threshold:
                    clusters.append([x])
                else:
                    clusters[-1].append(x)
            if len(clusters) >= 2:
                return FileContentType.MULTICOLUMN, text
            text += page.extract_text() + '\n'

    return FileContentType.STANDARD, text

def detect_multicolumn_layout_docx(docx_content):
    document = Document(io.BytesIO(docx_content))
    alignment_types = []
    text = ""
    isThereParagraph = False

    for para in document.paragraphs:
        if para.text != '':
            isThereParagraph = True
        if para.alignment is not None:
            alignment_types.append(para.alignment)
        text += para.text.strip() + '\n'
    unique_alignments = set(alignment_types)
    
    if len(unique_alignments) >= 2:
        return FileContentType.MULTICOLUMN, text
    
    if document.tables:
        if not isThereParagraph:
            return FileContentType.TABLE, text
        return FileContentType.CONTAINS_TABLE, text
    
    return FileContentType.STANDARD, text

if __name__ == '__main__':
    app.run(host="localhost", port=5000)
