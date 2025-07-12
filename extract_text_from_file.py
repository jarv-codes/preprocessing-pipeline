import csv
import os
import json
from docx import Document
from pptx import Presentation
import PyPDF2

# 1. 에러 처리 데코레이터 정의
def handle_extraction_errors(func):
    """텍스트 추출 함수의 예외를 처리하는 데코레이터"""
    def wrapper(filepath):
        try:
            return func(filepath)
        except Exception as e:
            # 함수의 이름에서 파일 형식(예: 'csv')을 가져옴
            file_type = func.__name__.split('_')[1].upper()
            return f"Error reading {file_type}: {str(e)}"
    return wrapper

# 2. 각 추출 함수에 데코레이터 적용
@handle_extraction_errors
def extract_csv_text(filepath):
    """CSV 파일의 텍스트를 추출"""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return "\n".join([", ".join(row) for row in reader])

@handle_extraction_errors
def extract_docx_text(filepath):
    """DOCX 파일의 텍스트를 추출"""
    doc = Document(filepath)
    fullText = [para.text for para in doc.paragraphs]
    return "\n".join(fullText)

@handle_extraction_errors
def extract_ipynb_text(filepath):
    """Jupyter Notebook(.ipynb) 파일의 텍스트를 추출"""
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    text = []
    for cell in nb.get('cells', []):
        if cell.get('cell_type') in ['markdown', 'code']:
            text.append("".join(cell.get('source', [])))
    return "\n".join(text)

@handle_extraction_errors
def extract_md_text(filepath):
    """Markdown 파일의 텍스트를 추출"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

@handle_extraction_errors
def extract_pdf_text(filepath):
    """PDF 파일의 텍스트를 추출"""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = []
        for page in reader.pages:
            if page_text := page.extract_text():
                text.append(page_text)
    return "\n".join(text)

@handle_extraction_errors
def extract_ppt_text(filepath):
    """PPT/PPTX/PPTM 파일의 텍스트를 추출"""
    prs = Presentation(filepath)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n".join(text)

# 3. 딕셔너리를 사용하여 확장자와 함수를 매핑
EXTRACTORS = {
    '.csv': extract_csv_text,
    '.docx': extract_docx_text,
    '.ipynb': extract_ipynb_text,
    '.md': extract_md_text,
    '.pdf': extract_pdf_text,
    '.ppt': extract_ppt_text,
    '.pptx': extract_ppt_text,
    '.pptm': extract_ppt_text,
}

def extract_text_from_file(filepath):
    """파일 경로를 받아 적절한 텍스트 추출 함수를 호출"""
    ext = os.path.splitext(filepath)[1].lower()
    # 딕셔너리의 get 메서드를 사용하여 함수를 찾고, 없으면 기본 메시지 반환
    extractor_func = EXTRACTORS.get(ext)
    if extractor_func:
        return extractor_func(filepath)
    else:
        return "Unsupported file type"
