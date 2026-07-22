import streamlit as st

def show_ai_chat(client, df):

    st.markdown("---")
    st.subheader("🤖 AI Chat Assistant")

    question = st.text_input("Ask any business question")

    if st.button("Ask AI"):

        if question.strip() == "":
            st.warning("Please enter a question.")
            return

        if df is None:
            st.warning("Please upload a CSV or Excel file first.")
            return

        try:

            dataset_info = df.head(50).to_string(index=False)

            prompt = f"""
You are an expert Business Intelligence Analyst.

Dataset Columns:
{', '.join(df.columns)}

Dataset Sample:
{dataset_info}

User Question:
{question}

Answer in simple business language.
"""

            with st.spinner("Analyzing Dataset..."):

                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt
                )

            st.success(response.text)

        except Exception as e:

            st.error(f"Error: {e}")