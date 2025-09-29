import streamlit as st
import pandas as pd
import json
from utils.checklist_loader import load_checklist
from utils.document_parser import extract_text_from_files
from fpdf import FPDF

st.set_page_config(page_title="Evaluación de Contratos", layout="wide")
st.title("Evaluación de Contratos vs Checklist")

# 1. Subida de múltiples documentos
uploaded_files = st.file_uploader("Sube los documentos del contrato (PDF/Word)", type=["pdf", "docx"], accept_multiple_files=True)

# 2. Cargar checklist
checklist = load_checklist("./data/requisitos.json")

# 3. Procesar documentos y evaluar requisitos
results = []
if uploaded_files:
    docs_text = extract_text_from_files(uploaded_files)
    for req in checklist:
        estado = "no cumple"
        fuente = ""
        for doc_name, doc_text in docs_text.items():
            if req["item"].lower() in doc_text.lower() or req["descripcion"].lower() in doc_text.lower():
                estado = "cumple"
                fuente = doc_name
                break
        results.append({
            "Requisito": req["item"],
            "Descripción": req["descripcion"],
            "Estado": estado,
            "Fuente": fuente
        })

    # 4. Mostrar tabla de resultados
    df = pd.DataFrame(results)
    st.subheader("Informe de Evaluación")
    st.dataframe(df)

    # 5. Resumen general
    estados = [r["Estado"] for r in results]
    if all(e == "cumple" for e in estados):
        resumen = "cumple"
    elif any(e == "cumple" for e in estados):
        resumen = "cumple parcialmente"
    else:
        resumen = "no cumple"
    st.markdown(f"**Resumen general:** El contrato {resumen}")

    # 6. Exportar informe en PDF
    def export_pdf(df, resumen):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Informe de Evaluación de Contrato", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Resumen general: {resumen}", ln=True, align="L")
        pdf.ln(10)
        for idx, row in df.iterrows():
            pdf.multi_cell(0, 10, txt=f"Requisito: {row['Requisito']}\nDescripción: {row['Descripción']}\nEstado: {row['Estado']}\nFuente: {row['Fuente']}\n", border=0)
            pdf.ln(2)
        return pdf.output(dest="S").encode("latin-1")

    pdf_bytes = export_pdf(df, resumen)
    st.download_button("Descargar informe en PDF", data=pdf_bytes, file_name="informe_evaluacion.pdf", mime="application/pdf")
else:
    st.info("Sube los documentos del contrato para iniciar la evaluación.")
