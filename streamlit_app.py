import streamlit as st
import random
import time

st.set_page_config(page_title="Loto Sim 20/80", page_icon="🎰")
st.title("🎰 Simulator Loto 20/80")
st.write("---")

tip_joc = st.selectbox("Câte numere verificăm?", [4, 5, 6, 7, 8], index=0)
input_numere = st.text_input(f"Introdu cele {tip_joc} numere:", "1 11 22 33")

if st.button("🚀 LANSEAZĂ CALCULUL"):
    try:
        mele = set([int(n) for n in input_numere.replace(",", " ").split() if n.strip().isdigit()])
        if len(mele) != tip_joc:
            st.error(f"Pune fix {tip_joc} numere!")
        else:
            st.info(f"Rulăm 1.000.000 de teste pe i5 Virtual...")
            start = time.time()
            gasit = False
            for i in range(1, 1000001):
                extragere = set(random.sample(range(1, 81), 20))
                if mele.issubset(extragere):
                    st.balloons()
                    st.success(f"🎯 GĂSIT la extragerea {i:,}!")
                    st.write(f"📈 Timp estimat de joc: {i/2/365:.1f} ani.")
                    gasit = True
                    break
            if not gasit:
                st.warning("Nu a ieșit în 1.000.000 de încercări. Mai încearcă!")
            st.write(f"⏱️ Viteza i5: {time.time()-start:.2f} sec")
    except:
        st.error("Pune doar cifre!")