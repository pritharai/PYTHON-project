import cv2  # OpenCV for image processing
import streamlit as st  # Streamlit for creating the web app
import numpy as np  # For handling image data

def create_sketch(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blurred = cv2.GaussianBlur(inverted_image, (15, 15), 0)
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)
    return sketch

def main():
    st.title("Pencil Sketch Generator")
    st.write("Upload an image to convert it into a pencil sketch.")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image", use_column_width=True)

        sketch = create_sketch(image)

        zoom_factor = st.slider("Zoom Level", 0.5, 3.0, 1.0, step=0.1)

        height, width = sketch.shape[:2]
        zoomed_sketch = cv2.resize(sketch, (int(width * zoom_factor), int(height * zoom_factor)), interpolation=cv2.INTER_LINEAR)

        st.image(zoomed_sketch, caption="Pencil Sketch", use_column_width=True, clamp=True, channels="GRAY")

        if st.button("Download Sketch"):
            _, buffer = cv2.imencode(".png", sketch)
            st.download_button(
                label="Click to Download",
                data=buffer.tobytes(),
                file_name="pencil_sketch.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()