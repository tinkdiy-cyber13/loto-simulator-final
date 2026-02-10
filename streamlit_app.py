import streamlit as st
import random
import time
import pandas as pd

# Configurare Pagina (Aspect Modern)
st.set_page_config(page_title="Loto Sim Pro v1.1", page_icon="🎰", layout="wide")

st.title("🎰 Simulator Loto 20/80 - Bord de Control")
st.write("---")

# --- ZONA DE INPUT (Pătratul 1) ---
with st.container():
    st.subheader("📥 Configurare Bilete")
    col_in1, col_in2 = st.columns([1, 2])
    with col_in1:
        tip_joc = st.selectbox("Câte numere joci?",, index=0)
    with col_in2:
        input_numere = st.text_input("Scrie numerele tale (cu spațiu):", "1 11 22 33")

st.divider()

# --- LOGICA DE CALCUL ---
if st.button("🚀 LANSEAZĂ SIMULAREA"):
    try:
        mele = set([int(n) for n in input_numere.replace(",", " ").split() if n.strip().isdigit()])
        
        if len(mele) != tip_joc:
            st.error(f"Eroare: Ai ales joc de {tip_joc} numere, dar ai scris {len(mele)}!")
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
                    # --- INTERFAȚA PE PĂTRATE (Rezultat) ---
                    st.balloons()
                    st.success("🎯 REZULTAT GĂSIT!")
                    
                    # Rândul 1 de Pătrate
                    c1, c2, c3 = st.columns(3)
                    c1.metric("🔢 Numerele Tale", str(sorted(list(mele))))
                    c2.metric("✅ Numere Verificate", f"{tip_joc} din {tip_joc}")
                    c3.metric("🎲 Extragerile", f"{i:,}")
                    
                    # Rândul 2 de Pătrate (Timpul)
                    zile = i / 2
                    ani = zile / 365
                    luni = (ani - int(ani)) * 12
                    
                    st.write("### 📅 Timp de așteptare estimat:")
                    p1, p2, p3 = st.columns(3)
                    p1.metric("Ani", int(ani))
                    p2.metric("Luni", int(luni))
                    p3.metric("Zile", int(zile % 30))
                    
                    st.info(f"⏱️ Calcul finalizat în {time.time() - start_time:.2f} secunde.")
                    break
                
                if i % 100000 == 0:
                    progress.progress(i / max_sim)
                    status.text(f"Se verifică extragerea nr: {i:,}...")

            if not gasit:
                st.warning(f"Nu a ieșit în {max_sim:,} încercări. Matematica e crudă!")
                
    except Exception as e:
        st.error("Verifică formatul numerelor!")

# --- FOOTER ---
st.divider()
st.caption("Hardware: i5 Gen 13 Virtualized | Protocol: OO-Cloud")

