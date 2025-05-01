import streamlit as st
import os
from PIL import Image
import numpy as np
import cv2
import tempfile

# Page configuration
st.set_page_config(
    page_title="ArtConnect - Your Digital Art Gallery",
    page_icon="🎨",
    layout="wide"
)

# Function to process image
def process_image(uploaded_file):
    try:
        # Save image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Load image
        input_image = Image.open(tmp_path)
        
        # Convert to numpy array for OpenCV processing
        img_array = np.array(input_image)
        
        # Convert to BGR for OpenCV
        if len(img_array.shape) == 3:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        
        # Apply artistic filters
        # 1. Watercolor filter
        watercolor = cv2.stylization(img_bgr, sigma_s=60, sigma_r=0.6)
        
        # 2. Sketch filter
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blurred, scale=256)
        
        # 3. Oil painting filter
        oil_painting = cv2.xphoto.oilPainting(img_bgr, 7, 1)
        
        # Convert back to PIL Image
        watercolor_pil = Image.fromarray(cv2.cvtColor(watercolor, cv2.COLOR_BGR2RGB))
        sketch_pil = Image.fromarray(sketch)
        oil_painting_pil = Image.fromarray(cv2.cvtColor(oil_painting, cv2.COLOR_BGR2RGB))
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return {
            'original': input_image,
            'watercolor': watercolor_pil,
            'sketch': sketch_pil,
            'oil_painting': oil_painting_pil
        }
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

# Main interface
st.title("🎨 ArtConnect - Your Digital Art Gallery")
st.markdown("""
    ### Transform your photos into works of art
    Upload an image and discover how it would look as an artwork in different styles.
""")

# Image upload
uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    with st.spinner('Processing your image...'):
        try:
            # Process image
            processed_images = process_image(uploaded_file)
            
            if processed_images is None:
                st.error("Failed to process image. Please try again.")
                st.stop()
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(processed_images['original'], caption="Original Image", use_column_width=True)
            
            with col2:
                st.image(processed_images['watercolor'], caption="Watercolor Style", use_column_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.image(processed_images['sketch'], caption="Sketch Style", use_column_width=True)
            
            with col4:
                st.image(processed_images['oil_painting'], caption="Oil Painting Style", use_column_width=True)
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            st.info("Please try another image or contact technical support.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Developed with ❤️ by ArtConnect</p>
        <p>© 2024 ArtConnect - All rights reserved</p>
    </div>
""", unsafe_allow_html=True) 