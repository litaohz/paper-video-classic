"""PDFium-backed source grounding. Boxes use top-left PDF-point coordinates."""
from pathlib import Path
import hashlib
import pypdfium2 as pdfium

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def quote_boxes(pdf, page_number, quote):
    if page_number < 1 or not quote.strip():
        raise ValueError('A 1-based page and a non-empty exact quote are required')
    with pdfium.PdfDocument(pdf) as doc:
        if page_number > len(doc):
            raise ValueError('Page is outside the document')
        page = doc[page_number - 1]
        width, height = page.get_size()
        text = page.get_textpage()
        search = text.search(quote, match_case=False, consecutive=False)
        matches = []
        while True:
            found = search.get_next()
            if found is None:
                break
            start, length = found
            rects = []
            for i in range(text.count_rects(start, length)):
                left, bottom, right, top = text.get_rect(i)
                rects.append([left, height-top, right, height-bottom])
            if rects:
                matches.append(rects)
        if not matches:
            raise ValueError(f'Quote not found on page {page_number}: {quote!r}. Scanned PDFs need OCR first.')
        if len(matches) != 1:
            raise ValueError(f'Ambiguous quote ({len(matches)} occurrences): {quote!r}; use a longer unique quote')
        return {'page': page_number, 'size': [width, height], 'quote': quote,
                'line_boxes': matches[0], 'pdf_sha256': sha256(pdf)}

def render_region(pdf, page_number, crop, scale=2):
    with pdfium.PdfDocument(pdf) as doc:
        page = doc[page_number-1]
        width, height = page.get_size()
        x0,y0,x1,y1 = crop
        if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
            raise ValueError('Crop must be within the real PDF page')
        bitmap = page.render(scale=scale, crop=(x0, height-y1, width-x1, y0))
        try:
            return bitmap.to_pil().convert('RGB').copy()
        finally:
            bitmap.close()

def ground(config, root):
    pdf = (root/config['pdf']).resolve()
    results=[]
    for mark in config['marks']:
        hit=quote_boxes(pdf,config['page'],mark['quote'])
        crop=config['crop']
        if not all(crop[0]<=r[0] and crop[1]<=r[1] and crop[2]>=r[2] and crop[3]>=r[3] for r in hit['line_boxes']):
            raise ValueError(f'Quote lies outside crop: {mark["quote"]}')
        results.append({**mark, **hit})
    return results
