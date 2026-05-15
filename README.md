# 텍스트 추출 파이프라인 (Text Extraction Pipeline)

다양한 형식의 파일(.pdf, .docx, .csv 등)에서 텍스트 콘텐츠를 추출하는 파이썬 프로젝트입니다.

## 주요 기능
- **다양한 파일 지원**: PDF, DOCX, PPTX, CSV, Markdown, Jupyter Notebook 등 여러 형식의 파일에서 텍스트를 추출합니다.
- **간편한 사용**: 단일 함수(`extract_text_from_file`) 호출만으로 파일 종류를 자동으로 감지하고 텍스트를 추출합니다.
- **안정적인 에러 처리**: 파일 읽기 오류가 발생해도 프로그램이 중단되지 않습니다.
- **고급 OCR 추출**: 스캔된 PDF나 이미지 기반 PDF의 텍스트 인식을 위해 이미지 전처리 후 Tesseract OCR을 사용합니다.
- **DOCX 내장 이미지 OCR**: DOCX 본문 텍스트뿐 아니라 문서에 삽입된 이미지에 대해서도 OCR을 수행하여 함께 반환합니다.

## 프로젝트 구성

| 파일 | 역할 |
| --- | --- |
| `extract_text_from_file.py` | 진입점. 파일 확장자에 따라 적절한 추출 함수를 자동으로 선택합니다. DOCX 추출 시 내장 이미지의 OCR 결과를 본문 뒤에 함께 반환합니다. |
| `extract_ocr_from_pdf.py` | 이미지 기반(스캔) PDF의 페이지를 이미지로 변환한 뒤 페이지별 OCR 텍스트 리스트를 반환합니다. |
| `extract_ocr_from_docx.py` | DOCX 파일 내부(`word/media/`)에 포함된 이미지들을 추출해 이미지별 OCR 텍스트 리스트를 반환합니다. |
| `ocr_core.py` | 공통 OCR 유틸리티. PIL 이미지에 그레이스케일 변환 및 이진화 전처리를 적용한 후 Tesseract로 텍스트를 추출합니다. |

## 설치 방법

1.  **Tesseract OCR 엔진 설치**

    이 프로젝트의 OCR 기능을 사용하려면 Tesseract 엔진이 시스템에 설치되어 있어야 합니다.

    * **Windows**: [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)에서 설치 파일을 받아 설치하세요. 설치 시 "Add Tesseract to the system PATH" 옵션을 꼭 체크해야 합니다.
    * **macOS**: `brew install tesseract`
    * **Ubuntu/Debian**: `sudo apt update && sudo apt install tesseract-ocr`

2.  **PDF → 이미지 변환을 위한 Poppler 설치 (PDF OCR 사용 시 필수)**

    `extract_ocr_from_pdf.py`는 내부적으로 `pdf2image`를 사용하며, 이를 위해 Poppler가 필요합니다.

    * **Windows**: [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)에서 받아 PATH에 추가하세요.
    * **macOS**: `brew install poppler`
    * **Ubuntu/Debian**: `sudo apt install poppler-utils`

3.  **저장소 복제**
    ```bash
    git clone https://github.com/jarv-codes/preprocessing-pipeline.git
    cd preprocessing-pipeline
    ```

4.  **필요한 파이썬 라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    ```

## 사용법 (Usage)

이 프로젝트는 세 가지 방식의 텍스트 추출을 지원합니다.

### 1. 일반 파일 텍스트 추출

텍스트 기반의 문서 파일(.docx, .pdf, .pptx, .csv, .md, .ipynb 등)에서 텍스트를 추출할 때 사용합니다. DOCX의 경우 본문 텍스트와 함께 문서에 삽입된 이미지의 OCR 결과가 자동으로 이어 붙여집니다.

```python
from extract_text_from_file import extract_text_from_file

# 추출하고 싶은 파일의 경로
filepath = 'example.docx'

# 함수를 호출하여 텍스트 추출
text = extract_text_from_file(filepath)

# 결과 출력
print(text)
```

### 2. 이미지 기반 PDF 텍스트 추출 (OCR)

스캔되거나, 글자가 이미지로 저장된 PDF 파일에서 텍스트를 추출할 때 사용합니다. 이 기능은 Tesseract OCR 엔진과 Poppler가 설치되어 있어야 합니다.

```python
from extract_ocr_from_pdf import extract_ocr_from_pdf

# 스캔된 PDF 파일 경로
filepath = 'scanned_document.pdf'

# OCR 함수를 호출하여 페이지별 텍스트 리스트 추출
ocr_pages = extract_ocr_from_pdf(filepath, start_page=1, end_page=3, lang='kor', dpi=300)

# 결과 출력
for i, page_text in enumerate(ocr_pages, start=1):
    print(f"--- Page {i} ---")
    print(page_text)
```

### 3. DOCX 내장 이미지 OCR 추출

DOCX 파일에 삽입된 이미지(스크린샷, 다이어그램 등)에서만 OCR 텍스트를 추출하고 싶을 때 사용합니다. `extract_text_from_file`을 사용하면 본문과 자동으로 함께 반환되지만, 이미지 텍스트만 별도로 다루고 싶다면 다음과 같이 직접 호출할 수 있습니다.

```python
from extract_ocr_from_docx import extract_ocr_from_docx

# DOCX 파일 경로
filepath = 'report.docx'

# 내장 이미지별 OCR 텍스트 리스트 추출
image_texts = extract_ocr_from_docx(filepath, lang='kor')

for i, text in enumerate(image_texts, start=1):
    print(f"--- Image {i} ---")
    print(text)
```

### 4. 단일 이미지 OCR (저수준 유틸리티)

PIL `Image` 객체 한 장에 대해 직접 OCR을 수행하고 싶다면 `ocr_core.ocr_image`를 사용합니다. 내부적으로 그레이스케일 변환과 이진화(기본 임계값 200)를 거쳐 인식률을 높입니다.

```python
from PIL import Image
from ocr_core import ocr_image

image = Image.open('snippet.png')
text = ocr_image(image, lang='kor', threshold=200)
print(text)
```
