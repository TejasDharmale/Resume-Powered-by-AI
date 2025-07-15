import streamlit as st
import re

def display_gemini_response(response, highlight_percentage=False):
    if "error" in response:
        if "503" in response["error"] or "overloaded" in response["error"].lower():
            st.error("The AI model is currently overloaded. Please wait a moment and try again.")
        else:
            st.error(response["error"])
    else:
        content = response['candidates'][0]['content']['parts'][0]['text']
        if highlight_percentage:
            match = re.search(r"(\d{1,3}(?:\.\d+)?%)", content)
            if match:
                percent_str = match.group(1)
                try:
                    score = float(percent_str.strip('%'))
                    st.markdown(f"## 🟢 Score: {score:.1f}/100")
                except Exception:
                    st.markdown(f"## 🟢 Score: {percent_str}")
                rest = content.replace(percent_str, '', 1).strip()
                if rest:
                    st.write(rest)
            else:
                st.warning("No score detected in the response.")
                st.write(content)
        else:
            st.write("**Response Content:**")
            st.write(content) 