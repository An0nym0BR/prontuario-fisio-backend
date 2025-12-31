from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pdf(atendimento):
    pdf = canvas.Canvas("relatorio.pdf", pagesize=A4)
    pdf.drawString(50, 800, "RELATÓRIO FISIOTERAPÊUTICO")
    pdf.drawString(50, 760, f"Paciente: {atendimento['nome']}")
    pdf.drawString(50, 740, f"EVA: {atendimento['eva']}")
    pdf.save()

