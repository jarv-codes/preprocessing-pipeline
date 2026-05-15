import os
from pdf2image import convert_from_path

from ocr_core import ocr_image


def _save_page_texts(texts, output_path, source, start_page):
    """페이지별 OCR 텍스트 리스트를 .md 또는 .txt로 저장."""
    if output_path.lower().endswith('.md'):
        title = os.path.splitext(os.path.basename(source))[0]
        sections = [f"## Page {start_page + i}\n\n{t}" for i, t in enumerate(texts)]
        content = f"# OCR Results — {title}\n\n" + "\n\n".join(sections) + "\n"
    else:
        sections = [f"--- Page {start_page + i} ---\n{t}" for i, t in enumerate(texts)]
        content = "\n\n".join(sections) + "\n"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def extract_ocr_from_pdf(filepath, start_page=1, end_page=None, lang='kor', dpi=300, output_path=None):
    """
    이미지 기반 PDF 파일에서 OCR을 사용해 페이지별 텍스트를 추출합니다.

    :param filepath: PDF 파일 경로
    :param start_page: 시작 페이지
    :param end_page: 종료 페이지 (None이면 끝까지)
    :param lang: Tesseract 언어 설정 (기본값 'kor')
    :param dpi: 이미지 변환 해상도 (기본값 300)
    :param output_path: 결과 저장 경로. .md이면 페이지별 H2 섹션의 마크다운으로, .txt이면 구분선 포함 텍스트로 저장
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

        if output_path:
            _save_page_texts(all_texts, output_path, source=filepath, start_page=start_page)

        return all_texts

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="이미지 기반 PDF에서 OCR로 페이지별 텍스트를 추출합니다."
    )
    parser.add_argument("filepath", help="PDF 파일 경로")
    parser.add_argument("-o", "--output", help="결과 저장 경로 (.md 또는 .txt). 생략하면 stdout에 출력")
    parser.add_argument("--start", type=int, default=1, help="시작 페이지 (기본: 1)")
    parser.add_argument("--end", type=int, default=None, help="종료 페이지 (기본: 끝까지)")
    parser.add_argument("--lang", default="kor", help="Tesseract 언어 (기본: kor)")
    parser.add_argument("--dpi", type=int, default=300, help="이미지 변환 DPI (기본: 300)")
    args = parser.parse_args()

    results = extract_ocr_from_pdf(
        args.filepath,
        start_page=args.start,
        end_page=args.end,
        lang=args.lang,
        dpi=args.dpi,
        output_path=args.output,
    )
    if results and not args.output:
        for idx, t in enumerate(results):
            print(f"--- Page {args.start + idx} ---")
            print(t)
            print()
