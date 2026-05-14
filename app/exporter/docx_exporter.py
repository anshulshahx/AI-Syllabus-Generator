import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from app.schemas.models import SyllabusResponse

EXPORTS_DIR = "outputs/exports"

def set_run(run, size=11, bold=False, color=None, italic=False):
    run.font.name   = "Arial"
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_divider(doc):
    p   = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"),   "single")
    bottom.set(qn("w:sz"),    "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "B0C4DE")
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_heading(doc, text, size=13, color=(31, 78, 121)):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    set_run(run, size=size, bold=True, color=color)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(5)

def add_bullet(doc, text):
    p   = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    set_run(run, size=11)

def add_numbered(doc, text):
    p   = doc.add_paragraph(style="List Number")
    run = p.add_run(text)
    set_run(run, size=11)

def export_syllabus_to_docx(syllabus: SyllabusResponse) -> str:
    doc = Document()

    # ── Page margins ──
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    # ── Title ──
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("ACADEMIC SYLLABUS")
    set_run(r, size=20, bold=True, color=(31, 78, 121))

    t2 = doc.add_paragraph()
    t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = t2.add_run("NBA Accreditation  |  OBE-Based Curriculum")
    set_run(r2, size=11, italic=True, color=(100, 100, 100))
    add_divider(doc)

    # ── Course info table ──
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    row = table.rows[0]
    lc  = row.cells[0]
    lp  = lc.paragraphs[0]
    lr  = lp.add_run("Course Name")
    set_run(lr, bold=True, color=(31, 78, 121))
    tc_pr = lc._tc.get_or_add_tcPr()
    shd   = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  "DCE6F1")
    tc_pr.append(shd)
    vc  = row.cells[1]
    vp  = vc.paragraphs[0]
    vr  = vp.add_run(syllabus.course_name)
    set_run(vr)
    doc.add_paragraph()
    add_divider(doc)

    # ── Units ──
    add_heading(doc, "Course Units")
    for unit in syllabus.units:
        add_heading(doc, f"{unit.unit_id}: {unit.unit_title}", size=12, color=(21, 101, 192))

        p = doc.add_paragraph()
        r = p.add_run("Objectives:")
        set_run(r, bold=True, size=11)
        for obj in unit.unit_objectives:
            add_bullet(doc, obj)

        p2 = doc.add_paragraph()
        r2 = p2.add_run("Outcomes:")
        set_run(r2, bold=True, size=11)
        for outcome in unit.unit_outcomes:
            add_bullet(doc, outcome)

        p3 = doc.add_paragraph()
        r3 = p3.add_run("Assessments:")
        set_run(r3, bold=True, size=11)
        for assessment in unit.assessments:
            add_bullet(doc, assessment)

        p4 = doc.add_paragraph()
        r4 = p4.add_run("Readings:")
        set_run(r4, bold=True, size=11)
        for reading in unit.readings:
            add_bullet(doc, reading)

        add_divider(doc)

    # ── Textbooks ──
    if syllabus.textbooks:
        add_heading(doc, "Suggested Textbooks")
        for book in syllabus.textbooks:
            add_numbered(doc, book)
        add_divider(doc)

    # ── YouTube ──
    if syllabus.youtube_resources:
        add_heading(doc, "YouTube & Online Resources")
        for resource in syllabus.youtube_resources:
            add_numbered(doc, resource)
        add_divider(doc)

    # ── Save ──
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    safe_name = syllabus.course_name.replace(" ", "_")
    filename  = f"{EXPORTS_DIR}/{safe_name}_syllabus.docx"
    doc.save(filename)
    print(f"DOCX exported: {filename}")
    return os.path.abspath(filename)