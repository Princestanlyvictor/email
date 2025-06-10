import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
import os

# === SETUP GEMINI ===
genai.configure(api_key="AIzaSyCcp2P-5r_83OVSqFHB48ePkydXNfiSv3c")
model = genai.GenerativeModel('gemini-2.0-flash')

# === Streamlit UI ===
st.set_page_config(page_title="Email Generator with Gemini", layout="centered")
st.title("📧 AI Email Generator using Gemini")

st.markdown("Enter your email content or context, then choose tone and format to generate a polished email.")

# === User Input ===
user_input = st.text_area("✍️ Describe the purpose or content of the email:", height=150)

# === Options ===
tone = st.selectbox("🎭 Select Tone", ["Professional", "Friendly", "Concise", "Formal", "Empathetic"])
email_type = st.selectbox("🗂️ Select Email Type", ["Apology", "Thank You", "Follow-up", "Request", "Introduction"])

# === State to hold generated email ===
if "email_text" not in st.session_state:
    st.session_state.email_text = ""

# === Generate Email ===
if st.button("🚀 Generate Email"):
    prompt = f"""Generate an {email_type.lower()} email in a {tone.lower()} tone. Use the following context:\n{user_input}"""
    response = model.generate_content(prompt)
    st.session_state.email_text = response.text
    st.success("Email Generated!")

# === Display Result ===
if st.session_state.email_text:
    st.subheader("📨 Generated Email")
    st.write(st.session_state.email_text)

    # === Regenerate Email ===
    if st.button("🔄 Regenerate with Same Input"):
        prompt = f"""Regenerate the {email_type.lower()} email in a {tone.lower()} tone using this context:\n{user_input}"""
        response = model.generate_content(prompt)
        st.session_state.email_text = response.text
        st.success("Email Regenerated!")

    # === Download as PDF ===
    def save_pdf(email_content):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in email_content.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf_output = "generated_email.pdf"
        pdf.output(pdf_output)
        return pdf_output

    if st.button("📥 Download as PDF"):
        file_path = save_pdf(st.session_state.email_text)
        with open(file_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="email_output.pdf")

