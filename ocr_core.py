import pytesseract
from PIL import Image


def ocr_image(image: Image.Image, lang: str = 'kor', threshold: int = 200) -> str:
    """
    PIL 이미지 한 장에서 OCR로 텍스트를 추출합니다.

    :param image: PIL Image 객체
    :param lang: Tesseract 언어 설정 (기본값 'kor')
    :param threshold: 이진화 임계값 (0~255, 기본값 200)
    :return: 추출된 텍스트 (앞뒤 공백 제거됨)
    """
    processed = image.convert('L')
    processed = processed.point(lambda p: 255 if p > threshold else 0)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed, lang=lang, config=config)
    return text.strip()
