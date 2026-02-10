import streamlit as st
import random
import time
import json
import os

# Configurare Pagina
st.set_page_config(page_title="Loto Sim Pro v1.2", page_icon="🎰", layout="wide")

DB_FILE = "baza_sim_vizite.json"

# --- FUNCTII BAZA DE DATE (CONTOR OO) ---
def incarca_vizite():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {"vizite": 0}
    return {"vizite": 0}

def salveaza_vizite(date):
    with open(DB_FILE, "w") as f: json.dump(date, f)

date_sistem = incarca_vizite()

if 'v' not in st.session_state:
    date_sistem["vizite"] = date_sistem.get("vizite", 0) + 1
    salveaza_vizite(date_sistem)
    st.session_state['v'] = True

# --- TITLU SI CONTOR OO ---
st.title("🎰 Simulator Loto 20/80")
st.markdown(
    f"""
    <div style='text-align: right; margin-top: -55px;'>
        <span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>
            OO: {date_sistem.get('vizite', 0)}
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)
st.write("---")

# --- ZONA DE INPUT ---
with st.container():
    st.subheader("📥 Configurare Simulări")
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        # AM REPARAT AICI: Am scos virgula dublă
        tip_joc = st.selectbox("Câte numere vrei să verifici?", [1, 2, 3, 4, 5, 6, 7, 8], index=3)
    with col_in2:
        input_numere = st.text_input("Introdu numerele (cu spațiu):", "1 11 22 33")

st.divider()

# --- LOGICA DE CALCUL ---
if st.button("🚀 LANSEAZĂ SIMULAREA"):
    try:
        mele = set([int(n) for n in input_numere.replace(",", " ").split() if n.strip().isdigit()])
        
        if len(mele) != tip_joc:
            st.error(f"Eroare: Ai ales {tip_joc} numere, dar ai scris {len(mele)}!")
        else:
            status = st.empty()
            progress = st.progress(0)
            start_time = time.time()
            max_sim = 1000000 
            gasit = False
            
            for i in range(1, max_sim + 1):
                extragere = set(random.sample(range(1, 81), 20))
                
                if mele.issubset(extragere):
                    gasit = True
                    st.balloons()
                    st.success("🎯 REZULTAT GĂSIT!")
                    
                    # --- AFIȘARE PĂTRATE REZULTAT ---
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("🔢 Numerele Tale", str(sorted(list(mele))))
                    c2.metric("✅ Verificate", f"{tip_joc}/{tip_joc}")
                    c3.metric("🎲 Extragerea Nr.", f"{i:,}")
                    c4.metric("⏱️ Timp Calcul", f"{time.time() - start_time:.2f}s")
                    
                    # --- AFIȘARE PĂTRATE TIMP ---
                    st.write("### 📅 Timp de așteptare estimat (la 2 extrageri/zi):")
                    zile = i / 2
                    ani = zile / 365
                    luni = (ani - int(ani)) * 12
                    
                    p1, p2, p3 = st.columns(3)
                    p1.metric("Ani", int(ani))
                    p2.metric("Luni", int(luni))
                    p3.metric("Zile", int(zile % 30))
                    break
                
                if i % 100000 == 0:
                    progress.progress(i / max_sim)
                    status.text(f"🔍 Se verifică extragerea: {i:,}...")

            if not gasit:
                st.warning(f"Nu a ieșit în {max_sim:,} încercări. i5-ul zice să mai încerci!")
                
    except Exception as e:
        st.error("Verifică numerele introduse!")

st.divider()
st.caption("Simulator Profesional | Protocol OO-V7 | Hardware i5 Cloud")
