import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Fruit Ripeness Detection",
    page_icon="🍅",
    layout="centered"
)

st.markdown(
    "<h1 style='text-align:center;'>🍅 Fruit Ripeness Detection</h1>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload gambar buah", type=["jpg", "jpeg", "png"]
)

def deteksi_kematangan_pil(img):
    img = img.convert("RGB")
    data = np.array(img)

    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]

    hijau = np.sum((g > r) & (g > b))
    merah = np.sum((r > g) & (r > b))
    kuning = np.sum((r > 150) & (g > 150) & (b < 120))

    total = hijau + kuning + merah + 1

    persentase = {
        "Hijau": hijau / total,
        "Kuning": kuning / total,
        "Merah": merah / total
    }

    if persentase["Hijau"] > persentase["Merah"] and persentase["Hijau"] > persentase["Kuning"]:
        return "Masih Mentah 🟢", persentase["Hijau"], persentase
    elif persentase["Merah"] > persentase["Hijau"] and persentase["Merah"] > persentase["Kuning"]:
        return "Matang 🔴", persentase["Merah"], persentase
    else:
        return "Setengah Matang 🟡", persentase["Kuning"], persentase

if uploaded_file:
    img = Image.open(uploaded_file)

    st.image(img, caption="Gambar Buah", use_container_width=True)

    status, tingkat, p = deteksi_kematangan_pil(img)

    st.subheader(status)
    st.progress(float(tingkat))

    c1, c2, c3 = st.columns(3)
    c1.metric("Hijau", f"{p['Hijau']*100:.1f}%")
    c2.metric("Kuning", f"{p['Kuning']*100:.1f}%")
    c3.metric("Merah", f"{p['Merah']*100:.1f}%")

    st.caption("Deteksi dilakukan berdasarkan dominasi warna RGB (tanpa OpenCV).")
