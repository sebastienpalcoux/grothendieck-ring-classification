#!/usr/bin/env python3
"""Build the append-only review supplement; no frozen file is edited.

Requires reportlab and pypdf. Run from any directory. Content that awaits final audit
reconciliation is isolated in docs/prepublication_review_content.json.
"""
from pathlib import Path
import json
import shutil
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = json.loads((ROOT / 'docs/prepublication_review_content.json').read_text())
NAME = 'prepublication-review-2026-10-17.pdf'
OUT = ROOT / 'manuscripts' / NAME
historical = ROOT / 'manuscripts/rank8/paper/rank8.pdf'
if not historical.is_file():
    raise FileNotFoundError('Required historical rank-eight PDF is missing: ' + str(historical))
if not historical.read_bytes().startswith(b'%PDF-'):
    raise ValueError('Historical rank-eight manuscript is not a PDF: ' + str(historical))
OUT.parent.mkdir(parents=True, exist_ok=True)
WEB = 'https://sebastienpalcoux.github.io/grothendieck-ring-classification/review.html'
DOC = 'https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/docs/PREPUBLICATION_REVIEW.md'
REPO = 'https://github.com/sebastienpalcoux/grothendieck-ring-classification'

fontdir = Path('/usr/share/fonts/truetype/dejavu')
for name, filename in [('Sans', 'DejaVuSans.ttf'), ('SansBold', 'DejaVuSans-Bold.ttf'),
                       ('Serif', 'DejaVuSerif.ttf'), ('Mono', 'DejaVuSansMono.ttf')]:
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
    'h2': ParagraphStyle('h2', fontName='SansBold', fontSize=12.3, leading=17, textColor=TEAL, spaceBefore=14, spaceAfter=7),
    'body': ParagraphStyle('body', fontName='Sans', fontSize=9.1, leading=14.2, textColor=INK, spaceAfter=9),
    'small': ParagraphStyle('small', fontName='Sans', fontSize=8.0, leading=12.2, textColor=MUTED, spaceAfter=7),
    'code': ParagraphStyle('code', fontName='Mono', fontSize=7.3, leading=11.4, textColor=INK, spaceAfter=0),
    'equation': ParagraphStyle('equation', fontName='Serif', fontSize=14.3, leading=23, textColor=INK, spaceAfter=0),
    'notice': ParagraphStyle('notice', fontName='Sans', fontSize=9.0, leading=14.1, textColor=INK, spaceAfter=0),
}

def p(text, style='body'):
    return Paragraph(text, styles[style])

def safe(text):
    return escape(text)

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

story = []
story += [p('GROTHENDIECK RING CLASSIFICATION  /  RESEARCH NOTE', 'kicker'),
          p('Prepublication<br/>review &amp; errata', 'title'),
          p(f'{safe(CONTENT["date"])}<br/>{safe(CONTENT["version"])}', 'subtitle')]
story += [box(p('<b>Read these results and data with caution.</b><br/>The research and this review were generated by AI. They have not yet been independently verified by human experts or formalized in Lean. Computational success does not certify the categorical arguments on which a checker depends.', 'notice'), WARN, AMBER), Spacer(1, 12)]
story += [p('A companion to the historical manuscripts', 'h2'),
          p('<b>R8_2_24 is reopened.</b> The accepted continuation now covers 35 of 38 original cases. R6_4_155, R6_8_1660 and R8_2_24 remain open. This dated correction takes precedence over older claims of complete rank-eight classification through multiplicity two.'),
          p('Audited research baseline: <font name="Mono">' + CONTENT['baseline'][:12] + '</font>. The online review carries subsequent reconciliation and the precise scope of each replay.', 'small'),
          p('Rank three: induced-unit identity', 'h2'),
          p('In Proposition 6.3, “A uniform near-group exclusion” (p. 10), the sentence immediately before equation (6.2) must use <b>three</b> copies of the unit:'),
          box(p('(F ∘ I)(1) = 3·1 ⊕ Y ⊕ mX', 'equation')),
          Spacer(1, 8),
          p('Indeed, 1² + Y² + X² = 1 + 1 + (1 + Y + mX). The following restrictions of the central summands already have the correct total. This typographical correction does not change the argument or its conclusion.'),
          p('In the same proposition, the Ng-Schauenburg formula cited as being “in Section 3” should refer to <b>equation (4.2), Section 4</b> (source label <font name="Mono">eq:moments</font>).'),
          p(f'<a href="{DOC}" color="#126d6b">Current repository review</a>  |  <a href="{WEB}" color="#126d6b">Public review page</a>', 'small'),
          PageBreak()]

story += [p('CORRECTED PROOF DEPENDENCIES', 'kicker'),
          p('Rank six', 'h1'),
          p('Two passages cite Proposition 3.27, whose scope is R6_3_215, for reductions concerning different rings. Use the following dependencies in the frozen manuscript. The reference corrections do not settle either residual existence question.'),
          p('1. Theorem 11.7, proof on p. 155', 'h2'),
          p('At the common-field Galois conjugation step, read:'),
          box(p('Extend to this common field the Galois conjugation supplied for <b>R6_4_155</b> by <b>Proposition 7.1</b>, and for <b>R6_8_1660</b> by the unrestricted sphericalization reduction at the beginning of <b>Section 7.5</b>, certified in the unrestricted reduction file below.')),
          Spacer(1, 7),
          p('Source: <font name="Mono">frontier_tensor_functors.tex</font>, lines 105-106. Correct labels: <font name="Mono">prop:nonselfdual-neargroup-spherical</font> and <font name="Mono">subsec:frontier-1660</font>.', 'small'),
          p('2. Corollary 12.2, proof on p. 157', 'h2'),
          p('At the reduction preceding the full twist-one support argument, read:'),
          box(p('Apply the unrestricted sphericalization reduction for <b>R6_8_1660</b> described in <b>Section 7.5</b> (the same certificate), followed by <b>Lemma 11.6</b> on pseudo-unitary tensor functors.')),
          Spacer(1, 7),
          p('Source: <font name="Mono">dimension_block_20261016.tex</font>, lines 81-82. Lemma label: <font name="Mono">lem:pu-tensor-functors</font>. Both chapter paths are relative to <font name="Mono">manuscripts/rank6/papers/chapters/</font>.', 'small'),
          p('Unrestricted reduction certificate', 'h2'),
          code(['supplements/rank6/research/round4/m8/R6_8_1660_reduction.json']),
          Spacer(1, 8),
          p('The audit freshly replayed the unrestricted reduction: 640 signed quotients, 24 sign orbits and 58 nongauge character rejections. The retained original gauge orbit supplies the spherical section. This is a reduction check, not an existence or nonexistence proof for the source ring.'),
          box(p('<b>Both remain unresolved:</b> R6_4_155 and R6_8_1660. The rank-37 Verlinde obstruction rejects a particular witness; it does not exclude R6_8_1660 itself.', 'notice'), WARN, AMBER),
          PageBreak()]

story += [p('SCOPE, REPLAY AND OPEN REVIEW', 'kicker'),
          p('What the checks establish', 'h1'),
          p(CONTENT['r24_status'], 'h2'),
          box([p(safe(x)) for x in CONTENT['r24_paragraphs']], WARN, AMBER),
          PageBreak(),
          p('REPRODUCIBLE CHECKS', 'kicker'),
          p('Current repository replay', 'h1'),
          p('From the repository root, restore the split data and include historical stages explicitly:'),
          code(['python tools/restore_data.py',
                'python ' + CONTENT.get('replay_program', 'tools/verify_unified_20261016.py') + ' --historical',
                'python -O ' + CONTENT.get('replay_program', 'tools/verify_unified_20261016.py') + ' --historical']),
          Spacer(1, 7),
          p('Without <font name="Mono">--historical</font>, the dispatcher omits historical constructor replays. Original checkers that use <font name="Mono">assert</font> must run in normal Python: an optimized invocation alone removes those checks.', 'small'),
          p('The portable fermion checker replaces the scratch-only command in the frozen rank-six research note:'),
          code(['python evidence/unified_20261016/rank6/verify_fermion_crossing.py --repo .']),
          p(CONTENT['replay_heading'], 'h2')]
story += [p(safe(x), 'small') for x in CONTENT['replay_paragraphs']]
story += [p('Read the live reconciliation record', 'h2'),
          p(f'<a href="{DOC}" color="#126d6b"><b>docs/PREPUBLICATION_REVIEW.md</b></a><br/><a href="{WEB}" color="#126d6b"><b>GitHub Pages / review.html</b></a>', 'body'),
          p('The linked record takes precedence over this dated snapshot for later review outcomes. Source integrity, exact finite replay, categorical proof validity and independent expert review are distinct claims.', 'small')]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=50, leftMargin=50,
                        topMargin=48, bottomMargin=64,
                        title='Prepublication review and errata - 17 October 2026',
                        author='Grothendieck Ring Classification project (AI-generated review)',
                        subject='Dated corrections and verification scope; provisional research')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
destination = ROOT / 'site/dist/papers' / NAME
destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(OUT, destination)
print(OUT)
print(destination)

# Publish a reading edition that puts the dated correction before the frozen
# rank-eight text. Historical manuscript bytes and their commitments stay intact.
from pypdf import PdfReader, PdfWriter
reviewed = historical.with_name('rank8-reviewed.pdf')
writer = PdfWriter()
writer.append(str(OUT), import_outline=False)
writer.append(str(historical), import_outline=False)
writer.add_outline_item('Read first: review and corrections', 0)
writer.add_outline_item('Historical rank-eight manuscript', len(PdfReader(str(OUT)).pages))
writer.add_metadata({
    '/Title': 'Rank eight — reviewed reading edition, 17 October 2026',
    '/Author': 'Grothendieck Ring Classification project (AI-generated research)',
    '/Subject': 'Dated correction followed by the unchanged historical manuscript; R8_2_24 reopened',
})
with reviewed.open('wb') as stream:
    writer.write(stream)
reading_web = ROOT / 'site/dist/papers/rank8-reviewed.pdf'
shutil.copyfile(reviewed, reading_web)
print(reviewed)
print(reading_web)
