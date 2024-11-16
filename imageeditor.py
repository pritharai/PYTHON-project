import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
import cv2
import numpy as np

# Function to apply filters and transformations
def apply_brightness(image, value):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(value)

def apply_contrast(image, value):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(value)

def apply_sharpness(image, value):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(value)

def apply_blur(image, value):
    return image.filter(ImageFilter.GaussianBlur(value))

def apply_edges(image):
    return image.filter(ImageFilter.FIND_EDGES)

def apply_invert(image):
    return ImageOps.invert(image.convert("RGB"))

def toggle_grayscale(image, is_grayscale):
    if is_grayscale:
        return ImageOps.grayscale(image)
    else:
        return image

# Function to turn a photo into a pencil sketch
def create_sketch(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blurred = cv2.GaussianBlur(inverted_image, (15, 15), 0)
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)
    return sketch

# Streamlit app
def main():
    st.title("Image Editor & Pencil Sketch Generator")

    # File uploader for the image
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Load image using PIL for editing and OpenCV for sketching
        image = Image.open(uploaded_file)
        image_cv = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Create tabs for Image Editing and Sketch Generation
        tab1, tab2 = st.tabs(["Image Editor", "Pencil Sketch Generator"])

        with tab1:
            st.header("Image Editor")
            st.image(image, caption="Original Image", use_column_width=True)

            # Edit Image options
            brightness = st.slider("Brightness", 0.0, 2.0, 1.0)
            contrast = st.slider("Contrast", 0.0, 2.0, 1.0)
            sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0)
            blur = st.slider("Blur", 0.0, 10.0, 0.0)
            edge_detection = st.checkbox("Edge Detection")
            invert_colors = st.checkbox("Invert Colors")
            grayscale = st.checkbox("Grayscale")

            # Apply Filters
            processed_image = image.copy()
            if brightness != 1.0:
                processed_image = apply_brightness(processed_image, brightness)
            if contrast != 1.0:
                processed_image = apply_contrast(processed_image, contrast)
            if sharpness != 1.0:
                processed_image = apply_sharpness(processed_image, sharpness)
            if blur != 0.0:
                processed_image = apply_blur(processed_image, blur)
            if edge_detection:
                processed_image = apply_edges(processed_image)
            if invert_colors:
                processed_image = apply_invert(processed_image)
            processed_image = toggle_grayscale(processed_image, grayscale)

            # Display processed image
            st.image(processed_image, caption="Processed Image", use_column_width=True)

            # Save button for processed image
            buf = io.BytesIO()
            processed_image.save(buf, format="PNG")
            byte_data = buf.getvalue()

            st.download_button(
                label="Download Processed Image",
                data=byte_data,
                file_name="processed_image.png",
                mime="image/png"
            )

        with tab2:
            st.header("Pencil Sketch Generator")
            st.write("Click the button below to convert the uploaded image into a pencil sketch.")

            # Generate the pencil sketch
            if st.button("Generate Pencil Sketch"):
                sketch = create_sketch(image_cv)
                # Zoom functionality using a slider
                zoom_factor = st.slider("Zoom Level", 0.5, 3.0, 1.0, step=0.1)

                # Apply zoom to the sketch
                height, width = sketch.shape[:2]
                zoomed_sketch = cv2.resize(sketch, (int(width * zoom_factor), int(height * zoom_factor)), interpolation=cv2.INTER_LINEAR)

                # Display the pencil sketch
                st.image(zoomed_sketch, caption="Pencil Sketch", use_column_width=True, clamp=True, channels="GRAY")

                # Save button for pencil sketch
                _, buffer = cv2.imencode(".png", sketch)
                st.download_button(
                    label="Download Pencil Sketch",
                    data=buffer.tobytes(),
                    file_name="pencil_sketch.png",
                    mime="image/png"
                )

if __name__ == "__main__":
    main()
