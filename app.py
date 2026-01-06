import streamlit as st
import numpy as np

# -----------------------------
# App config
# -----------------------------
st.set_page_config(page_title="WB Magic Box", page_icon="🧩", layout="centered")

# -----------------------------
# Custom CSS for design
# -----------------------------
PRIMARY = "#4B9FEA"
ACCENT = "#7C4DFF"
BG = "#0F172A"
CARD = "#111827"
TEXT = "#E5E7EB"
MUTED = "#9CA3AF"

CSS = f"""
<style>
.stApp {{
  background: linear-gradient(135deg, {BG} 0%, #0b1220 50%, #0a0f1a 100%);
  color: {TEXT};
  font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', Arial, sans-serif;
}}
.card {{
  background: {CARD};
  border: 1px solid #1F2937;
  border-radius: 14px;
  padding: 16px 18px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.35);
}}
.cell {{
  width: 70px; height: 70px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem; font-weight: 700;
  border-radius: 10px;
}}
.correct {{ background: linear-gradient(135deg, #22C55E, #16A34A); color: white; }}
.wrong {{ background: linear-gradient(135deg, #EF4444, #DC2626); color: white; }}
hr {{ border: none; border-top: 1px solid #1F2937; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def check_sums(grid: np.ndarray):
    n = grid.shape[0]
    row_sums = grid.sum(axis=1)
    col_sums = grid.sum(axis=0)
    diag1 = int(np.trace(grid))
    diag2 = int(np.trace(np.fliplr(grid)))
    target = row_sums[0]
    checks = {
        "rows": [s == target for s in row_sums],
        "cols": [s == target for s in col_sums],
        "diag": [diag1 == target, diag2 == target],
        "target": target,
    }
    return checks

def init_state():
    if "size" not in st.session_state:
        st.session_state.size = 3

init_state()

# -----------------------------
# Header
# -----------------------------
st.markdown(f"""
<div class="card">
  <h1>🧩 WB Magic Box</h1>
  <p style="color:{MUTED};">Choose a grid size (3×3, 4×4, 5×5). Enter numbers manually into each cell. Rows, columns, and diagonals highlight instantly.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# -----------------------------
# Controls
# -----------------------------
size = st.selectbox("Grid size", [3, 4, 5], index=[3, 4, 5].index(st.session_state.size))
st.session_state.size = size

# -----------------------------
# Editable Grid
# -----------------------------
grid = np.zeros((size, size), dtype=int)

cols = st.columns(size)
for r in range(size):
    for c in range(size):
        with cols[c]:
            val = st.number_input(f"Cell {r+1},{c+1}", min_value=1, max_value=9, step=1, key=f"cell_{r}_{c}")
            grid[r, c] = val

# -----------------------------
# Auto-check as you type
# -----------------------------
checks = check_sums(grid)
target = checks["target"]

# Display row results
st.subheader("Row checks")
row_html = '<div style="display:flex; gap:10px;">'
for i, ok in enumerate(checks["rows"]):
    row_html += f'<div class="cell {"correct" if ok else "wrong"}">Row {i+1}</div>'
row_html += "</div>"
st.markdown(row_html, unsafe_allow_html=True)

# Display column results
st.subheader("Column checks")
col_html = '<div style="display:flex; gap:10px;">'
for i, ok in enumerate(checks["cols"]):
    col_html += f'<div class="cell {"correct" if ok else "wrong"}">Col {i+1}</div>'
col_html += "</div>"
st.markdown(col_html, unsafe_allow_html=True)

# Display diagonal results
st.subheader("Diagonal checks")
diag_html = '<div style="display:flex; gap:10px;">'
diag_html += f'<div class="cell {"correct" if checks["diag"][0] else "wrong"}">Main Diag</div>'
diag_html += f'<div class="cell {"correct" if checks["diag"][1] else "wrong"}">Other Diag</div>'
diag_html += "</div>"
st.markdown(diag_html, unsafe_allow_html=True)

# Final result
if all(checks["rows"]) and all(checks["cols"]) and all(checks["diag"]):
    st.success(f"🎉 Magic square complete! Common sum = {target}")
else:
    st.warning(f"Not magic yet. Target sum = {target}")
