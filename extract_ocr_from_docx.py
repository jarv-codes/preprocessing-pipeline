import os
import zipfile
from io import BytesIO
from PIL import Image

from ocr_core import ocr_image


IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')


def _save_image_texts(texts, output_path, source):
    """이미지별 OCR 텍스트 리스트를 .md 또는 .txt로 저장."""
    if output_path.lower().endswith('.md'):
        title = os.path.splitext(os.path.basename(source))[0]
        sections = [f"## Image {i}\n\n{t}" for i, t in enumerate(texts, start=1)]
        content = f"# OCR Results — {title}\n\n" + "\n\n".join(sections) + "\n"
    else:
        sections = [f"--- Image {i} ---\n{t}" for i, t in enumerate(texts, start=1)]
        content = "\n\n".join(sections) + "\n"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def extract_ocr_from_docx(filepath, lang='kor', output_path=None):
    """
    DOCX 파일에 내장된 이미지들에서 OCR로 텍스트를 추출합니다.

    :param filepath: DOCX 파일 경로
    :param lang: Tesseract 언어 설정 (기본값 'kor')
    :param output_path: 결과 저장 경로. .md이면 이미지별 H2 섹션의 마크다운으로, .txt이면 구분선 포함 텍스트로 저장
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

        if output_path and texts:
            _save_image_texts(texts, output_path, source=filepath)

        return texts

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None
