import argparse
from pathlib import Path

import fitz  # PyMuPDF

SAFE_EXTS = {"png", "jpeg", "jpg", "jb2", "jpx", "tiff", "bmp"}


def extract_images_from_pdf(filepath: str, output_dir: str = "extracted_images",
                            dedupe: bool = True) -> int:
    """
    PDF에 임베드된 이미지를 페이지별로 추출해 저장합니다.

    :param filepath: PDF 파일 경로
    :param output_dir: 추출된 이미지를 저장할 디렉터리 (기본값 'extracted_images')
    :param dedupe: 동일 xref 이미지를 중복 저장하지 않음 (기본값 True)
    :return: 저장된 이미지 개수
    """
    src = Path(filepath)
    if not src.exists():
        print(f"오류: '{filepath}' 파일을 찾을 수 없습니다.")
        return 0

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    seen = set()
    count = 0

    with fitz.open(src) as doc:
        for page_index, page in enumerate(doc, start=1):
            for img_index, img in enumerate(page.get_images(full=True), start=1):
                xref = img[0]
                if dedupe and xref in seen:
                    continue
                seen.add(xref)

                base = doc.extract_image(xref)
                ext = base["ext"] if base["ext"] in SAFE_EXTS else "bin"
                image_path = out / f"page_{page_index:03d}_img_{img_index:02d}.{ext}"
                image_path.write_bytes(base["image"])
                count += 1

    print(f"추출 완료: {count}개 이미지")
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PDF에 임베드된 이미지를 페이지별로 추출합니다."
    )
    parser.add_argument("filepath", help="PDF 파일 경로")
    parser.add_argument("-o", "--output", default="extracted_images",
                        help="저장 디렉터리 (기본: extracted_images)")
    parser.add_argument("--no-dedupe", action="store_true",
                        help="동일 이미지(xref) 중복 저장 허용")
    args = parser.parse_args()

    extract_images_from_pdf(args.filepath, args.output, dedupe=not args.no_dedupe)
