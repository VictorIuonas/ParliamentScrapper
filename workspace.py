import pytesseract
from PIL import Image
import sys
from pdf2image import convert_from_path
import os
import io

pdf_path = 'output/session_2.pdf'
output_filename = 'result.txt'
pages = convert_from_path(pdf_path)
pg_cntr = 1

sub_dir = str('images/session_2/')

if not os.path.exists(sub_dir):
    os.makedirs(sub_dir)

for page in pages:
    if pg_cntr <= 20:
        filename = f'pg_{pg_cntr}_session_2.jpg'

        saved_page_path = os.path.join(sub_dir, filename)
        page.save(saved_page_path)

        with io.open(output_filename, 'a+', encoding='utf8') as f:
            f.write(f"================ PAGE {pg_cntr} =============================\n")
            f.write(pytesseract.image_to_string(saved_page_path, lang='spa'))
            f.write("==============================================================\n")
        pg_cntr += 1
