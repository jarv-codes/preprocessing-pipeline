# Colab: pdf 이미지 개선 후 pdf추출

from pdf2image import convert_from_path
import pytesseract # 로컬 AI
import os
from PIL import Image # 이미지 처리를 위해 Pillow 라이브러리의 Image 모듈 추가

def extract_ocr_text(filepath, start_page=1, end_page=None, lang='kor', dpi=300):
    """
    이미지 기반 PDF 파일에서 OCR을 사용해 텍스트를 추출합니다.

    :param filepath: PDF 파일 경로
    :param start_page: 시작 페이지
    :param end_page: 종료 페이지 (None이면 끝까지)
    :param lang: Tesseract 언어 설정 (기본값 'kor')
    :param dpi: 이미지 변환 해상도 (기본값 300)
    :return: 페이지별로 추출된 텍스트 리스트
    """
    if not os.path.exists(filepath):
        print(f"오류: '{filepath}' 파일을 찾을 수 없습니다.")
        return None

    try:
        # PDF를 이미지로 변환할 때 DPI를 높여 해상도를 개선 (기본값 200)
        images = convert_from_path(filepath, first_page=start_page, last_page=end_page, dpi=dpi)
        
        # 추출된 텍스트를 저장할 리스트
        all_texts = []

        print(f"총 {len(images)}개 페이지 OCR 처리 시작...")
        for i, image in enumerate(images):
            page_num = start_page + i
            print(f"-> {page_num}페이지 처리 중...")

            #--- 이미지 전처리 시작 ---
            # 1. 흑백으로 변경
            processed_image = image.convert('L')
            # 2. 이진화: 특정 임계값(threshold=200)보다 어두우면 검은색, 밝으면 흰색으로 변경
            processed_image = processed_image.point(lambda p: p > 200 and 255)
            # --- 이미지 전처리 끝 ---
            
            # # Tesseract 설정: 페이지 분할 모드(psm) 6은 단일 텍스트 블록으로 인식하는 옵션
            config = r'--oem 3 --psm 6'

            # 처리된 이미지에서 한글(kor) 텍스트를 추출
            text = pytesseract.image_to_string(processed_image, lang=lang, config=config)
            
            # 결과를 리스트에 추가
            all_texts.append(text.strip())
        
        # 모든 텍스트가 담긴 리스트를 반환
        return all_texts

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None

# --- 함수 사용 예시 ---
# if __name__ == '__main__':
#     pdf_path = 'scanned_document.pdf'
#     extracted_pages = extract_ocr_text(pdf_path, start_page=1, end_page=2)
#
#     if extracted_pages:
#         for idx, page_text in enumerate(extracted_pages):
#             print(f"--- {idx + 1} 페이지 결과 ---")
#             print(page_text)
