import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Proposal Generator")
st.title("AI Proposal & Contract Generator")

with st.form("proposal_form"):
    client_name = st.text_input("Client Name")
    company = st.text_input("Company")
    industry = st.selectbox("Industry", ["SMM", "Real Estate"])
    scope = st.text_area("Project Scope")
    deliverables = st.text_area("Deliverables")
    timeline = st.text_input("Timeline")
    budget = st.text_input("Budget")
    submitted = st.form_submit_button("Generate")

def generate_proposal(data):
    prompt = f"""
Create a professional proposal + contract.

Client: {data['client_name']}
Company: {data['company']}
Industry: {data['industry']}
Scope: {data['scope']}
Deliverables: {data['deliverables']}
Timeline: {data['timeline']}
Budget: {data['budget']}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
         messages=[
        {
            "role": "system",
            "content": "You are an expert proposal and contract generator for agencies. You produce professional, legally-sounding, client-ready documents."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
        temperature=0.7
    )
    return response.choices[0].message.content

if submitted:
    with st.spinner("Generating..."):
        result = generate_proposal({
            "client_name": client_name,
            "company": company,
            "industry": industry,
            "scope": scope,
            "deliverables": deliverables,
            "timeline": timeline,
            "budget": budget
        })
    st.markdown(result)
