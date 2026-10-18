#!/usr/bin/env python3
"""Create share-card QR SVGs from reviewed public URLs; requires reportlab."""
import json
from pathlib import Path
from reportlab.graphics import renderSVG
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'guide/cards.json').read_text(encoding='utf-8'))
for card in data['cards']:
    widget = QrCodeWidget(data['reader_url'] + 'cards/' + card['slug'] + '.html', barLevel='M')
    x0, y0, x1, y1 = widget.getBounds()
    size = 130
    drawing = Drawing(size, size, transform=[size/(x1-x0), 0, 0, size/(y1-y0), 0, 0])
    drawing.add(widget)
    (root / 'site/cards' / ('qr-' + card['id'] + '.svg')).write_text(renderSVG.drawToString(drawing), encoding='utf-8')
print('Created 5 QR SVGs.')
