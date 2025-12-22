import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="Quread.ai Blog", layout="wide")

# Apply the same Dark Mode style (Optional, but keeps it consistent)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #dcdde1; }
    h1, h2, h3 { color: #00d2d3 !important; font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("📚 Quantum Learning Hub")
st.write("Watch my latest breakdowns of quantum concepts.")
st.divider()

# --- VIDEO POST 1 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. What is a Qubit?")
    # REPLACE THIS URL with your actual YouTube video link
    st.video("https://www.youtube.com/watch?v=s71X6QY_rQM") 
    st.caption("A deep dive into Superposition and how we visualize it.")

with col2:
    st.markdown("### Key Takeaways")
    st.markdown("""
    * Classical bits are 0 OR 1.
    * Qubits are complex vectors.
    * **Superposition** is not 'both at once', it is a linear combination.
    """)

st.divider()

# --- VIDEO POST 2 ---
st.subheader("2. Understanding Entanglement")
st.video("https://www.youtube.com/watch?v=zNzzGgr2mhk") # Example URL
st.caption("Why Einstein called it 'Spooky Action at a Distance'.")