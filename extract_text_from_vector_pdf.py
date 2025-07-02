# Colab: pdf 이미지 개선 후 pdf추출

from pdf2image import convert_from_path
import pytesseract # 로컬 AI
import os
from PIL import Image # 이미지 처리를 위해 Pillow 라이브러리의 Image 모듈 추가

# PDF 파일 이름
pdf_file_path = filepath

# 추출할 페이지 범위
start_page = 1
end_page = 3

print("Colab 환경에서 OCR 정확도 개선 버전을 실행합니다...")

if not os.path.exists(pdf_file_path):
    print(f"오류: '{pdf_file_path}' 파일을 찾을 수 없습니다.")
else:
    try:
        # PDF를 이미지로 변환할 때 DPI를 높여 해상도를 개선 (기본값 200)
        images = convert_from_path(pdf_file_path, first_page=start_page, last_page=end_page, dpi=300)

        print(f"{len(images)}개의 페이지를 이미지로 변환했습니다.")

        for i, image in enumerate(images):
            page_num = start_page + i
            print(f"-> {page_num}페이지 OCR 처리 중...")

            # --- 이미지 전처리 시작 ---
            # 1. 흑백으로 변경
            processed_image = image.convert('L')
            # 2. 이진화: 특정 임계값보다 어두우면 검은색, 밝으면 흰색으로 변경
            threshold = 200
            processed_image = processed_image.point(lambda p: p > threshold and 255)
            # --- 이미지 전처리 끝 ---

            # Tesseract 설정: 페이지 분할 모드(psm) 6은 단일 텍스트 블록으로 인식하는 옵션
            config = r'--oem 3 --psm 6'

            # 처리된 이미지에서 한글(kor) 텍스트를 추출
            text = pytesseract.image_to_string(processed_image, lang='kor', config=config)

            print(f"### {page_num}페이지 ###")
            print(text.strip())
            print("---")

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
