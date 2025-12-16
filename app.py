import streamlit as st
import cv2
import numpy as np

# ================= CONFIG =================
st.set_page_config(
    page_title="Fruit Ripeness Detection",
    page_icon="🍎",
    layout="centered"
)

# ================= HEADER =================
st.markdown(
    """
    <h1 style='text-align: center;'>🍎 Fruit Ripeness Detection</h1>
    <p style='text-align: center; color: gray;'>
    Klasifikasi kematangan buah berdasarkan warna dominan (HSV)
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ================= UPLOAD =================
uploaded_file = st.file_uploader(
    "📤 Upload gambar buah",
    type=["jpg", "jpeg", "png"]
)

# ================= LOGIC =================
def deteksi_kematangan(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hijau = cv2.inRange(hsv, np.array([35, 50, 50]), np.array([85, 255, 255]))
    kuning = cv2.inRange(hsv, np.array([20, 50, 50]), np.array([34, 255, 255]))

    merah1 = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))
    merah2 = cv2.inRange(hsv, np.array([170, 50, 50]), np.array([180, 255, 255]))
    merah = merah1 + merah2

    hijau_px = cv2.countNonZero(hijau)
    kuning_px = cv2.countNonZero(kuning)
    merah_px = cv2.countNonZero(merah)

    total = hijau_px + kuning_px + merah_px + 1

    persentase = {
        "Hijau": hijau_px / total,
        "Kuning": kuning_px / total,
        "Merah": merah_px / total
    }

    if persentase["Hijau"] > persentase["Kuning"] and persentase["Hijau"] > persentase["Merah"]:
        status = "Masih Mentah"
        warna = "🟢"
        tingkat = persentase["Hijau"]
    elif persentase["Merah"] > persentase["Hijau"] and persentase["Merah"] > persentase["Kuning"]:
        status = "Matang"
        warna = "🔴"
        tingkat = persentase["Merah"]
    else:
        status = "Setengah Matang"
        warna = "🟡"
        tingkat = persentase["Kuning"]

    return status, warna, tingkat, persentase

# ================= DISPLAY =================
if uploaded_file:
    bytes_data = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(bytes_data, cv2.IMREAD_COLOR)

    st.image(
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
        caption="Gambar Buah",
        use_container_width=True
    )

    status, ikon, tingkat, persentase = deteksi_kematangan(img)

    st.divider()

    st.markdown(
        f"""
        <h2 style='text-align:center;'>{ikon} {status}</h2>
        """,
        unsafe_allow_html=True
    )

    st.progress(float(tingkat))

    col1, col2, col3 = st.columns(3)
    col1.metric("Hijau", f"{persentase['Hijau']*100:.1f}%")
    col2.metric("Kuning", f"{persentase['Kuning']*100:.1f}%")
    col3.metric("Merah", f"{persentase['Merah']*100:.1f}%")

    st.caption(
        "Sistem menentukan kematangan berdasarkan proporsi warna dominan pada ruang warna HSV."
    )
