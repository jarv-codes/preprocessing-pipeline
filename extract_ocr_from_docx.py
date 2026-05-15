import os
import zipfile
from io import BytesIO
from PIL import Image

from ocr_core import ocr_image


IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')


def extract_ocr_from_docx(filepath, lang='kor'):
    """
    DOCX 파일에 내장된 이미지들에서 OCR로 텍스트를 추출합니다.

    :param filepath: DOCX 파일 경로
    :param lang: Tesseract 언어 설정 (기본값 'kor')
    :return: 이미지별로 추출된 텍스트 리스트 (빈 결과는 제외)
    """
    if not os.path.exists(filepath):
        print(f"오류: '{filepath}' 파일을 찾을 수 없습니다.")
        return None

    try:
        texts = []
        with zipfile.ZipFile(filepath) as z:
            media_files = [
                name for name in z.namelist()
                if name.startswith('word/media/') and name.lower().endswith(IMAGE_EXTS)
            ]

            if not media_files:
                return []

            print(f"총 {len(media_files)}개 이미지 OCR 처리 시작...")
            for i, name in enumerate(media_files, start=1):
                print(f"-> {i}/{len(media_files)} ({name}) 처리 중...")
                with z.open(name) as f:
                    image = Image.open(BytesIO(f.read()))
                    text = ocr_image(image, lang=lang)
                    if text:
                        texts.append(text)

        return texts

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None
