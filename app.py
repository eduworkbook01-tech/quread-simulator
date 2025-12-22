import streamlit as st
import numpy as np
import engine
import matplotlib.pyplot as plt

# --- VISUALS: INJECT CUSTOM CSS ---
def local_css():
    st.markdown("""
    <style>
    /* 1. Import a futuristic font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300&display=swap');

    /* 2. Global Background & Text */
    .stApp {
        background-color: #0e1117; /* Very dark blue-black */
        color: #dcdde1;
        font-family: 'Roboto Mono', monospace;
    }

    /* 3. Headers (The "Orbitron" sci-fi look) */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00d2d3 !important; /* Cyan Neon */
        text-shadow: 0 0 10px rgba(0, 210, 211, 0.5);
    }

    /* 4. Buttons (Neon Borders) */
    .stButton>button {
        color: #00d2d3;
        border: 1px solid #00d2d3;
        background-color: transparent;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00d2d3;
        color: #0e1117;
        box-shadow: 0 0 20px rgba(0, 210, 211, 0.6);
    }

    /* 5. Special "Observe" Button (Red Warning Style) */
    div[data-testid="stVerticalBlock"] > div:nth-child(5) button {
        border-color: #ff6b6b;
        color: #ff6b6b;
    }
    
    /* 6. Metric Box Styling */
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #ff9ff3; /* Pink Neon */
        font-size: 3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# CALL THE FUNCTION
local_css()

# --- 1. The "Local AI" Logic ---
def explain_state_with_llm(state_vector, history):
    """
    Logic for 2-Qubit Explanation
    """
    probs = np.abs(state_vector) ** 2
    
    # Check for the famous "Bell State" (Entanglement)
    # This happens when |00> and |11> are both 50%, but the middle states are 0.
    if np.isclose(probs[0], 0.5) and np.isclose(probs[3], 0.5):
        return "✨ ENTANGLEMENT DETECTED! You have created a Bell State. The qubits are perfectly linked. If you measure Qubit 0 as '0', Qubit 1 becomes '0' instantly. If you measure '1', the other becomes '1'. They effectively communicate faster than light."

    # Check for simple Superposition on Q0
    if np.isclose(probs[0], 0.5) and np.isclose(probs[2], 0.5):
        return "Qubit 0 is in superposition, but Qubit 1 is still 0. They are not entangled yet."

    # Default Case
    return "The system is in a complex state. Check the probability bars to see the likelihood of each outcome."

def draw_bloch_vector(amplitude_0, amplitude_1):
    """
    Draws a simple 2D representation of the qubit state.
    """
    fig, ax = plt.subplots(figsize=(3, 3))
    
    # Draw the circle
    circle = plt.Circle((0, 0), 1, color='#b2bec3', fill=False, linewidth=2)
    ax.add_artist(circle)
    
    # Calculate coordinates (Projecting complex numbers to 2D circle)
    # This is a simplified view for teaching (Real part vs Imaginary/Probability)
    x = amplitude_1.real 
    y = amplitude_0.real
    
    # Draw the arrow representing the state
    ax.arrow(0, 0, x, y, head_width=0.1, head_length=0.1, fc='#6c5ce7', ec='#6c5ce7', width=0.02)
    
    # Labels
    ax.text(0, 1.1, "|0>", ha='center', fontsize=12)
    ax.text(1.1, 0, "|1>", va='center', fontsize=12)
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off') # Hide the square box
    
    return fig

# --- 2. The Rest of Your App (UI) ---
st.set_page_config(page_title="Quread.ai 2-Qubit", layout="centered")
st.title("⚛️ Quread.ai: Entanglement Studio")
st.write("Create a 'Bell State' by mixing Superposition (H) and Entanglement (CNOT).")

if 'circuit' not in st.session_state:
    st.session_state.circuit = engine.QuantumCircuit()
    st.session_state.history = []

# --- CONTROLS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.info("Qubit 0 (Control)")
    if st.button("H on Q0"):
        st.session_state.circuit.apply_gate("H", 0)
        st.session_state.history.append("H(q0)")
    if st.button("X on Q0"):
        st.session_state.circuit.apply_gate("X", 0)
        st.session_state.history.append("X(q0)")

with col2:
    st.success("Qubit 1 (Target)")
    if st.button("H on Q1"):
        st.session_state.circuit.apply_gate("H", 1)
        st.session_state.history.append("H(q1)")
    if st.button("X on Q1"):
        st.session_state.circuit.apply_gate("X", 1)
        st.session_state.history.append("X(q1)")

with col3:
    st.warning("Multi-Qubit Gates")
    if st.button("Apply CNOT"):
        st.session_state.circuit.apply_cnot()
        st.session_state.history.append("CNOT")
    
    st.write("") # Spacer
    if st.button("Reset Circuit"):
        st.session_state.circuit = engine.QuantumCircuit()
        st.session_state.history = []
st.divider()
col_measure, col_result = st.columns([1, 2])

with col_measure:
    # A big red button to simulate the "danger" of collapsing the state
    if st.button("👁️ OBSERVE (MEASURE)", type="primary"):
        # 1. Trigger the collapse in the engine
        result = st.session_state.circuit.collapse()
        
        # 2. Add to history
        st.session_state.history.append(f"Measure={result}")
        
        # 3. Store the specific result to show it big
        st.session_state.last_result = result

with col_result:
    if 'last_result' in st.session_state:
        st.metric(label="Collapsed Reality", value=f"|{st.session_state.last_result}⟩")
        st.caption("The wavefunction has collapsed. The probabilities are now 100% for this state.")
# --- VISUALIZATION ---
st.divider()

# Get state
vector = st.session_state.circuit.state
probs = st.session_state.circuit.measure()

# 1. Show the Math
st.subheader("State Vector (Amplitudes)")
# Formatting complex numbers for 4 states
st.latex(r"|\psi\rangle = " + 
         f"{vector[0].real:.2f}|00\\rangle + " + 
         f"{vector[1].real:.2f}|01\\rangle + " + 
         f"{vector[2].real:.2f}|10\\rangle + " + 
         f"{vector[3].real:.2f}|11\\rangle")

# 2. Show the Chart
# --- NEW DARK MODE CHART ---
st.subheader("Measurement Probabilities")

# Set the style to dark (black background)
plt.style.use('dark_background')

# Create figure with transparent background
fig, ax = plt.subplots()
fig.patch.set_facecolor('#0e1117') # Match app background
ax.set_facecolor('#0e1117')

states = ['|00⟩', '|01⟩', '|10⟩', '|11⟩']
# Use Neon Cyan for bars
bars = ax.bar(states, probs, color='#00d2d3')

# Add a glow effect (by adding a lighter border)
for bar in bars:
    bar.set_edgecolor('#c7ecee')
    bar.set_linewidth(1)

# Style the axes
ax.set_ylim(0, 1.1)
ax.set_ylabel("Probability")
ax.grid(color='#2d3436', linestyle='--', linewidth=0.5) # Faint grid lines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#b2bec3')
ax.spines['bottom'].set_color('#b2bec3')
ax.tick_params(axis='x', colors='#b2bec3')
ax.tick_params(axis='y', colors='#b2bec3')

st.pyplot(fig)
st.subheader("Qubit 0 Orientation")
# We just look at the first qubit's influence roughly
# (Note: Visualizing individual qubits when entangled is mathematically tricky, 
# so this works best before you hit CNOT)
fig_bloch = draw_bloch_vector(vector[0], vector[2]) 
st.pyplot(fig_bloch)
# --- 3. The "Explain" Button ---
st.divider()
st.subheader("🤖 Quread.ai Narrator")

if st.button("Explain this State", key="explain_btn"):
    # No spinner needed, it's instant!
    explanation = explain_state_with_llm(
        st.session_state.circuit.state, 
        st.session_state.history
    )
    st.success(explanation)