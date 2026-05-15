import os
from pdf2image import convert_from_path

from ocr_core import ocr_image


def extract_ocr_from_pdf(filepath, start_page=1, end_page=None, lang='kor', dpi=300):
    """
    이미지 기반 PDF 파일에서 OCR을 사용해 페이지별 텍스트를 추출합니다.

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
        images = convert_from_path(filepath, first_page=start_page, last_page=end_page, dpi=dpi)

        all_texts = []
        print(f"총 {len(images)}개 페이지 OCR 처리 시작...")
        for i, image in enumerate(images):
            page_num = start_page + i
            print(f"-> {page_num}페이지 처리 중...")
            all_texts.append(ocr_image(image, lang=lang))

        return all_texts

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None
