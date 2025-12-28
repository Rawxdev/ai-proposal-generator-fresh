import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
from fpdf import FPDF
import re

# -------------------------
# ENV + CLIENT
# -------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Proposal Generator")
st.sidebar.title("Rawia's AI Proposal Generator")

st.header("Create Proposal & Contract")

# -------------------------
# FORM
# -------------------------
with st.form("proposal_form"):
    client_name = st.text_input("Client Name")
    company = st.text_input("Company")
    industry = st.selectbox("Industry", ["SMM", "Real Estate"])
    scope = st.text_area("Project Scope")
    deliverables = st.text_area("Deliverables (comma separated)")
    timeline = st.text_input("Timeline")
    budget = st.text_input("Budget")
    submitted = st.form_submit_button("Generate Proposal & Contract")

# -------------------------
# AI GENERATION
# -------------------------
def generate_proposal(data):
    prompt = f"""
You are a professional business consultant.

Create a detailed proposal + contract.

Client Name: {data['client_name']}
Company: {data['company']}
Industry: {data['industry']}
Project Scope: {data['scope']}
Deliverables: {data['deliverables']}
Timeline: {data['timeline']}
Budget: {data['budget']}

Include:
1. Proposal Overview
2. Scope of Work
3. Deliverables
4. Timeline
5. Pricing
6. Contract Terms
7. Sign-off
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# -------------------------
# TEXT CLEANER (KEY FIX)
# -------------------------
def clean_text(text):
    replacements = {
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# -------------------------
# PDF GENERATOR (STABLE)
# -------------------------
def create_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", size=11)

    safe_text = clean_text(text)

    for line in safe_text.split("\n"):
        pdf.set_x(pdf.l_margin)
        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(page_width, 8, line)

    file_path = "proposal_contract.pdf"
    pdf.output(file_path)
    return file_path

# -------------------------
# RUN
# -------------------------
if submitted:
    with st.spinner("Generating AI proposal..."):
        output = generate_proposal({
            "client_name": client_name,
            "company": company,
            "industry": industry,
            "scope": scope,
            "deliverables": deliverables,
            "timeline": timeline,
            "budget": budget
        })

    st.subheader("Generated Proposal & Contract")
    st.text_area("Output", output, height=400)

    pdf_path = create_pdf(output)

    with open(pdf_path, "rb") as f:
        st.download_button(
            "Download Proposal as PDF",
            f,
            file_name="proposal_contract.pdf",
            mime="application/pdf"
        )
