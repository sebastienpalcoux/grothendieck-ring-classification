#!/usr/bin/env python3
"""Build the standalone current research-status PDF.

The existing public filename remains stable. No manuscript is concatenated,
read, rewritten or presented as an alternative edition by this builder.
Content is maintained in docs/prepublication_review_content.json.
Requires reportlab; run from any working directory.
"""
from pathlib import Path
import json
import shutil
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = json.loads((ROOT / 'docs/prepublication_review_content.json').read_text())
NAME = 'prepublication-review-2026-10-17.pdf'
OUT = ROOT / 'manuscripts' / NAME
OUT.parent.mkdir(parents=True, exist_ok=True)
REPO = 'https://github.com/sebastienpalcoux/grothendieck-ring-classification'
WEB = 'https://sebastienpalcoux.github.io/grothendieck-ring-classification'

fontdir = Path('/usr/share/fonts/truetype/dejavu')
for name, filename in [('Sans', 'DejaVuSans.ttf'), ('SansBold', 'DejaVuSans-Bold.ttf'),
                       ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(fontdir / filename)))
pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='SansBold')

INK = colors.HexColor('#203738')
MUTED = colors.HexColor('#58696a')
TEAL = colors.HexColor('#126d6b')
LINE = colors.HexColor('#d4dfdc')
PAPER = colors.HexColor('#fbfcf8')
AMBER = colors.HexColor('#a46c24')
WARN = colors.HexColor('#f8f0df')
PALE = colors.HexColor('#edf4f1')
W, H = A4
WIDTH = W - 100
styles = {
    'kicker': ParagraphStyle('kicker', fontName='SansBold', fontSize=8.2, leading=11.8, textColor=TEAL, spaceAfter=10),
    'title': ParagraphStyle('title', fontName='SansBold', fontSize=29, leading=34, textColor=INK, spaceAfter=12),
    'subtitle': ParagraphStyle('subtitle', fontName='Sans', fontSize=11, leading=16, textColor=MUTED, spaceAfter=16),
    'h1': ParagraphStyle('h1', fontName='SansBold', fontSize=20, leading=26, textColor=INK, spaceAfter=13),
    'h2': ParagraphStyle('h2', fontName='SansBold', fontSize=12, leading=17, textColor=TEAL, spaceBefore=13, spaceAfter=7),
    'body': ParagraphStyle('body', fontName='Sans', fontSize=9.1, leading=14.2, textColor=INK, spaceAfter=9),
    'small': ParagraphStyle('small', fontName='Sans', fontSize=8.0, leading=12.2, textColor=MUTED, spaceAfter=7),
    'code': ParagraphStyle('code', fontName='Mono', fontSize=7.3, leading=11.4, textColor=INK),
    'notice': ParagraphStyle('notice', fontName='Sans', fontSize=9.0, leading=14.1, textColor=INK),
    'tablehead': ParagraphStyle('tablehead', fontName='SansBold', fontSize=8, leading=11.5, textColor=TEAL),
    'table': ParagraphStyle('table', fontName='Sans', fontSize=9, leading=13, textColor=INK),
}

def p(text, style='body'):
    return Paragraph(text, styles[style])

def safe(text):
    return escape(str(text))

def box(contents, fill=PALE, bar=TEAL, padding=12):
    cell = contents if isinstance(contents, list) else [contents]
    t = Table([[cell]], colWidths=[WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), fill),
        ('LINEBEFORE', (0, 0), (0, -1), 3, bar),
        ('LEFTPADDING', (0, 0), (-1, -1), padding),
        ('RIGHTPADDING', (0, 0), (-1, -1), padding),
        ('TOPPADDING', (0, 0), (-1, -1), padding),
        ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t

def code(lines):
    return box(p('<br/>'.join(safe(x) for x in lines), 'code'), padding=10)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(.6)
    canvas.line(50, 48, W-50, 48)
    canvas.setFont('Sans', 7.0)
    canvas.setFillColor(MUTED)
    canvas.drawString(50, 34, 'AI-generated research | No independent human verification or Lean formalization')
    canvas.drawRightString(W-50, 34, f'{doc.page}')
    canvas.restoreState()

def counts_table():
    fields = ['rank', 'bound', 'rings', 'excluded', 'models', 'open']
    rows = [[p(x, 'tablehead') for x in ['Rank', 'Bound', 'Rings', 'Excluded', 'Models', 'Open']]]
    for row in CONTENT['rank_counts']:
        if row['rings'] != row['excluded'] + row['models'] + row['open']:
            raise ValueError('Inconsistent classification partition: ' + str(row))
        rows.append([p(f"{row[x]:,}", 'table') for x in fields])
    table = Table(rows, colWidths=[48, 55, 105, 113, 87, WIDTH-408], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PALE),
        ('LINEBELOW', (0, 0), (-1, 0), .8, TEAL),
        ('LINEBELOW', (0, -1), (-1, -1), .8, TEAL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PAPER]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return table

story = [p('GROTHENDIECK RING CLASSIFICATION  /  RESEARCH NOTE', 'kicker'),
         p('Research status<br/>&amp; verification', 'title'),
         p(f'{safe(CONTENT["date"])}<br/>{safe(CONTENT["version"])}', 'subtitle'),
         box(p('<b>Read these results and data with caution.</b><br/>' + safe(CONTENT['caution']), 'notice'), WARN, AMBER),
         Spacer(1, 10), p('The current classification record', 'h2'),
         p(safe(CONTENT['summary'])), counts_table(), Spacer(1, 9)]
story += [p(safe(x), 'small') for x in CONTENT['coverage_notes']]
story += [p(f'<a href="{WEB}/" color="#126d6b">Public atlas</a>  |  <a href="{REPO}" color="#126d6b">GitHub repository</a>', 'small'), PageBreak()]

story += [p('MATHEMATICAL FRONTIER', 'kicker'), p('Three open cases', 'h1'),
          p('Each question concerns general complex fusion categorification. The reductions below are necessary conditions with explicit limits.')]
for case in CONTENT['open_cases']:
    story += [p(safe(case['id']) + '  /  ' + safe(case['heading']), 'h2')]
    story += [p(safe(x)) for x in case['paragraphs']]
story += [box(p('<b>Status discipline.</b> A restricted nonexistence result applies only under its stated assumptions. An exact computation of conditional equations does not discharge the missing categorical hypothesis.', 'notice')), PageBreak()]

story += [p('EXACT COMPUTATIONAL EVIDENCE', 'kicker'), p('What was checked', 'h1')]
for section in CONTENT['replay_sections']:
    story += [p(safe(section['heading']), 'h2')]
    story += [p(safe(x), 'small') for x in section['paragraphs']]
story += [PageBreak()]

story += [p('READING AND REPRODUCING THE RECORD', 'kicker'), p('Evidence and its limits', 'h1')]
for item in CONTENT['interpretation']:
    story += [p(safe(item['term']), 'h2'), p(safe(item['meaning']))]
story += [p('Replay from the repository root', 'h2'),
          code(['python3 tools/restore_data.py',
                'python3 ' + CONTENT['replay_program'],
                'python3 -O ' + CONTENT['replay_program']]),
          Spacer(1, 8), p(safe(CONTENT['replay_note']), 'small'),
          p('The rank-specific full-census commands, dependencies, receipts and limitations are documented in the verification guide. The aggregate release checks are separate from the mathematical certificate replays.', 'small'),
          p('Current sources', 'h2'),
          p(f'<a href="{REPO}/blob/main/docs/RESEARCH_STATUS.md" color="#126d6b"><b>Research status</b></a><br/>'
            f'<a href="{REPO}/blob/main/docs/VERIFY.md" color="#126d6b"><b>Verification guide</b></a><br/>'
            f'<a href="{WEB}/review.html" color="#126d6b"><b>Public research status page</b></a>'),
          p('The manuscript statements, individual ledger entries and their source-bound evidence should be read together. This note summarizes the current scope; it is not an independent proof certificate.', 'small')]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=50, leftMargin=50,
                        topMargin=48, bottomMargin=64,
                        title='Research status and verification - 17 October 2026',
                        author='Grothendieck Ring Classification project (AI-generated research)',
                        subject='Current classification, three open cases, computational scope and limitations')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
destination = ROOT / 'site/dist/papers' / NAME
destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(OUT, destination)
print(OUT)
print(destination)
