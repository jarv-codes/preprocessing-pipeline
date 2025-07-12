# 텍스트 추출 파이프라인 (Text Extraction Pipeline)

다양한 형식의 파일(.pdf, .docx, .csv 등)에서 텍스트 콘텐츠를 추출하는 파이썬 프로젝트입니다.

## 주요 기능
- **다양한 파일 지원**: PDF, DOCX, PPTX, CSV, Markdown, Jupyter Notebook 등 여러 형식의 파일에서 텍스트를 추출합니다.
- **간편한 사용**: 단일 함수(`extract_text_from_file`) 호출만으로 파일 종류를 자동으로 감지하고 텍스트를 추출합니다.
- **안정적인 에러 처리**: 파일 읽기 오류가 발생해도 프로그램이 중단되지 않습니다.
- **고급 OCR 추출**: 스캔된 PDF나 이미지 기반 PDF의 텍스트 인식을 위해 이미지 전처리 후 Tesseract OCR을 사용합니다.

## 설치 방법

1.  **Tesseract OCR 엔진 설치**

    이 프로젝트의 OCR 기능을 사용하려면 Tesseract 엔진이 시스템에 설치되어 있어야 합니다.

    * **Windows**: [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)에서 설치 파일을 받아 설치하세요. 설치 시 "Add Tesseract to the system PATH" 옵션을 꼭 체크해야 합니다.
    * **macOS**: `brew install tesseract`
    * **Ubuntu/Debian**: `sudo apt update && sudo apt install tesseract-ocr`

2.  **저장소 복제**
    ```bash
    git clone https://github.com/jarv-codes/preprocessing-pipeline.git
    cd preprocessing-pipeline
    ```

3.  **필요한 파이썬 라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    ```

## 사용법 (Usage)

이 프로젝트는 두 가지 방식의 텍스트 추출을 지원합니다.

### 1. 일반 파일 텍스트 추출

텍스트 기반의 문서 파일(.docx, .pdf, .pptx 등)에서 텍스트를 추출할 때 사용합니다.

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

스캔되거나, 글자가 이미지로 저장된 PDF 파일에서 텍스트를 추출할 때 사용합니다. 이 기능은 Tesseract OCR 엔진이 설치되어 있어야 합니다.

```python
from extract_text_from_vector_pdf import extract_ocr_text

# 스캔된 PDF 파일 경로
filepath = 'scanned_document.pdf'

# OCR 함수를 호출하여 텍스트 추출
ocr_text = extract_ocr_text(filepath, start_page=1, end_page=3, lang='kor', dpi=300)

# 결과 출력
print(ocr_text)
```
