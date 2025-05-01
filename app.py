import streamlit as st
from PIL import Image, ImageOps
import random
import numpy as np

# Page configuration
st.set_page_config(
    page_title="ArtConnect - Your Digital Art Gallery",
    page_icon="🎨",
    layout="wide"
)

def analyze_style(image):
    try:
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Calculate color distribution
        unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
        color_diversity = unique_colors / (img_array.shape[0] * img_array.shape[1])
        
        # Calculate brightness
        grayscale = ImageOps.grayscale(image)
        brightness = np.mean(np.array(grayscale)) / 255
        
        # Calculate contrast
        contrast = np.std(np.array(grayscale)) / 255
        
        # Determine style characteristics
        style_analysis = {
            'color_palette': 'Vibrant' if color_diversity > 0.3 else 'Minimalist',
            'brightness': 'Bright' if brightness > 0.6 else 'Dark',
            'contrast': 'High' if contrast > 0.3 else 'Low',
            'style_type': determine_style_type(color_diversity, brightness, contrast)
        }
        
        return style_analysis
    except Exception as e:
        st.error(f"Error analyzing style: {str(e)}")
        return None

def determine_style_type(color_diversity, brightness, contrast):
    if color_diversity > 0.3 and brightness > 0.6:
        return "Impressionist"
    elif color_diversity < 0.2 and contrast > 0.3:
        return "Minimalist"
    elif brightness < 0.4 and contrast > 0.3:
        return "Expressionist"
    elif color_diversity > 0.4 and brightness > 0.5:
        return "Pop Art"
    else:
        return "Contemporary"

def evaluate_price(image):
    try:
        # Get basic image characteristics
        width, height = image.size
        total_pixels = width * height
        
        # Calculate complexity (simple metric)
        grayscale = ImageOps.grayscale(image)
        complexity = sum(grayscale.histogram()) / total_pixels
        
        # Base price calculation
        base_price = 100  # Starting price in USD
        
        # Adjust price based on size
        size_factor = total_pixels / (1000 * 1000)  # Normalize to 1MP
        size_price = base_price * size_factor
        
        # Adjust price based on complexity
        complexity_factor = complexity / 255  # Normalize to 0-1
        complexity_price = size_price * (1 + complexity_factor)
        
        # Add some randomness for market variation
        market_variation = random.uniform(0.8, 1.2)
        final_price = complexity_price * market_variation
        
        # Round to nearest 10
        final_price = round(final_price / 10) * 10
        
        return {
            'base_price': round(base_price),
            'size_factor': round(size_factor, 2),
            'complexity_factor': round(complexity_factor, 2),
            'final_price': round(final_price)
        }
    except Exception as e:
        st.error(f"Error evaluating price: {str(e)}")
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
            # Open image
            image = Image.open(uploaded_file)
            
            # Create grayscale version
            grayscale = ImageOps.grayscale(image)
            
            # Create inverted version
            inverted = ImageOps.invert(image)
            
            # Analyze style
            style_info = analyze_style(image)
            
            # Evaluate price
            price_info = evaluate_price(image)
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption="Original Image", use_column_width=True)
            
            with col2:
                st.image(grayscale, caption="Grayscale Style", use_column_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.image(inverted, caption="Inverted Style", use_column_width=True)
            
            with col4:
                st.image(grayscale, caption="Black & White", use_column_width=True)
            
            # Display style analysis
            st.markdown("---")
            st.subheader("🎨 Style Analysis")
            
            if style_info:
                st.markdown(f"""
                ### Artistic Style: {style_info['style_type']}
                
                **Characteristics:**
                - Color Palette: {style_info['color_palette']}
                - Brightness: {style_info['brightness']}
                - Contrast: {style_info['contrast']}
                
                *This analysis is based on visual characteristics of the image and 
                compares them with known artistic styles.*
                """)
            else:
                st.warning("Could not analyze the style of this image.")
            
            # Display price evaluation
            st.markdown("---")
            st.subheader("💰 Price Evaluation")
            
            if price_info:
                st.markdown(f"""
                ### Estimated Value: ${price_info['final_price']:,}
                
                **Price Breakdown:**
                - Base Price: ${price_info['base_price']:,}
                - Size Factor: {price_info['size_factor']}x
                - Complexity Factor: {price_info['complexity_factor']}x
                
                *Note: This is an automated estimate based on image characteristics. 
                Actual market value may vary based on artistic merit, artist reputation, 
                and current market trends.*
                """)
            else:
                st.warning("Could not evaluate price for this image.")
            
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