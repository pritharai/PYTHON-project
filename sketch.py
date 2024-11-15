import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io

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

def main():
    # Streamlit UI components
    st.title("Image Editor")
    
    # Upload image
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg", "bmp", "gif"])
    
    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)
        
        # Convert to editable image (a copy)
        processed_image = image.copy()

        # Sliders and buttons
        brightness = st.slider("Brightness", 0.0, 2.0, 1.0)
        contrast = st.slider("Contrast", 0.0, 2.0, 1.0)
        sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0)
        blur = st.slider("Blur", 0.0, 10.0, 0.0)
        edge_detection = st.checkbox("Edge Detection")
        invert_colors = st.checkbox("Invert Colors")
        grayscale = st.checkbox("Grayscale")

        # Apply Filters
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
        
        # Save button
        buf = io.BytesIO()
        processed_image.save(buf, format="PNG")
        byte_data = buf.getvalue()

        st.download_button(
            label="Download Image",
            data=byte_data,
            file_name="processed_image.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
