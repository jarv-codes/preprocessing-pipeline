import re

import pytesseract
from PIL import Image


_HANGUL_SPACE_RE = re.compile(r'([가-힣]) ([가-힣])')
_HANGUL_BEFORE_PUNCT_RE = re.compile(r'([가-힣]) ([,.?!:;])')


def collapse_korean_spaces(text: str) -> str:
    """한글 OCR 결과에서 인접한 한글 음절 사이에 삽입된 단일 공백을 제거합니다.

    Tesseract 한국어 OCR은 글자마다 공백을 끼워 넣는 경향이 있어 가독성을 해칩니다.
    이 함수는 (1) 한글 음절-단일공백-한글 음절 패턴을 반복적으로 합쳐 주고,
    (2) 한글 뒤 구두점 앞 공백도 제거합니다. 표 구분자나 영문/숫자, 자모 불릿(예: ㅇ)은
    건드리지 않습니다.
    """
    prev = None
    while prev != text:
        prev = text
        text = _HANGUL_SPACE_RE.sub(r'\1\2', text)
    return _HANGUL_BEFORE_PUNCT_RE.sub(r'\1\2', text)


def ocr_image(image: Image.Image, lang: str = 'kor', threshold: int = 200,
              collapse_spaces: bool = True) -> str:
    """
    PIL 이미지 한 장에서 OCR로 텍스트를 추출합니다.

    :param image: PIL Image 객체
    :param lang: Tesseract 언어 설정 (기본값 'kor')
    :param threshold: 이진화 임계값 (0~255, 기본값 200)
    :param collapse_spaces: True이면 한글 사이 공백을 후처리로 제거 (기본값 True)
    :return: 추출된 텍스트 (앞뒤 공백 제거됨)
    """
    processed = image.convert('L')
    processed = processed.point(lambda p: 255 if p > threshold else 0)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed, lang=lang, config=config)
    if collapse_spaces:
        text = collapse_korean_spaces(text)
    return text.strip()
