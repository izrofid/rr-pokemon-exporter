import streamlit as st
import base64
from io import BytesIO
from PIL import Image

st.title("Team Viewer")

qp = st.query_params
if "img" in qp:
    try:
        img_data = base64.b64decode(qp["img"])
        image = Image.open(BytesIO(img_data))
        st.image(image, caption="Your Team", use_column_width=True)
    except Exception as e:
        st.error(f"Failed to load image: {e}")
else:
    st.warning("No image provided.")
