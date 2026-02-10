import streamlit as st
import random
import time
import json
import os

# Configurare Pagina
st.set_page_config(page_title="Loto Sim Pro v1.6", page_icon="🎰", layout="wide")

DB_FILE = "baza_sim_vizite.json"

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
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)
st.write("---")

# --- ZONA DE INPUT ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    tip_joc = st.selectbox("Câte numere verifici?", [1,2,3,4,5,6,7,8], index=3)
with col_in2:
    input_numere = st.text_input("Introdu numerele tale:", "1 2 3 4")

# --- BUTON SIMULARE ---
if st.button("🎰 LANSEAZĂ SIMULAREA (MIXED)"):
    try:
        mele = set([int(n) for n in input_numere.replace(",", " ").split() if n.strip().isdigit()])
        if len(mele) != tip_joc:
            st.error(f"Pune fix {tip_joc} numere!")
        else:
            # --- "CLEPSIDRA" VIZUALĂ ---
            monitor = st.empty()
            progress = st.progress(0)
            
            start_time = time.time()
            max_sim = 2000000 
            gasit = False
            urna = list(range(1, 81))
            
            for i in range(1, max_sim + 1):
                random.shuffle(urna) 
                extragere = set(random.sample(urna, 20))
                
                if mele.issubset(extragere):
                    gasit = True
                    st.balloons()
                    
                    st.markdown("### 📊 Rezultate Simulare (Mixed Mode)")
                    res_html = f"""
                    <div style='display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px;'>
                        <span style='background:#003366; color:white; padding:8px 15px; border-radius:8px; font-size:16px; font-weight:bold; border: 1px solid #22d3ee;'>🔢 Nr: {sorted(list(mele))}</span>
                        <span style='background:#003366; color:white; padding:8px 15px; border-radius:8px; font-size:16px; font-weight:bold; border: 1px solid #22d3ee;'>🎲 Extragere: {i:,}</span>
                        <span style='background:#003366; color:white; padding:8px 15px; border-radius:8px; font-size:16px; font-weight:bold; border: 1px solid #22d3ee;'>⏱️ Speed: {time.time()-start_time:.2f}s</span>
                    </div>
                    """
                    st.markdown(res_html, unsafe_allow_html=True)
                    
                    zile_tot = i / 2
                    ani = int(zile_tot // 365)
                    luni = int((zile_tot % 365) // 30)
                    zile = int(zile_tot % 30)
                    
                    st.write(f"#### 📅 Timp estimat de așteptare:")
                    t_col1, t_col2, t_col3 = st.columns(3)
                    t_col1.metric("Zile", zile)
                    t_col2.metric("Luni", luni)
                    t_col3.metric("Ani", ani)
                    break
                
                # --- ACTUALIZARE MONITOR (CLEPSIDRA) ---
                if i % 25000 == 0: # Actualizăm mai des pentru efect vizual
                    elaps = time.time() - start_time
                    progress.progress(i / max_sim)
                    monitor.markdown(f"""
                        <div style='background:#1e1e1e; padding:20px; border-radius:10px; border-left: 5px solid #22d3ee;'>
                            <h4 style='color:#22d3ee; margin:0;'>⏳ ANALIZĂ ÎN CURS...</h4>
                            <p style='font-family:monospace; font-size:20px; color:white; margin:10px 0;'>
                                🎲 Extrageri procesate: <b>{i:,}</b><br>
                                ⏱️ Timp scurs: <b>{elaps:.1f} secunde</b>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

            if not gasit:
                st.warning(f"După {max_sim:,} încercări agitate, nu a ieșit încă.")
    except:
        st.error("Eroare la procesare!")

st.divider()
st.caption("Simulator Mixed Mode | Real-Time Tracker | v1.6")

