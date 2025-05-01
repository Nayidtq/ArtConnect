import streamlit as st
import os
from PIL import Image
import numpy as np
from rembg import remove
import torch
from transformers import pipeline
import cv2
from title_generator import ArtTitleGenerator
from sales_agent import ArtSalesAgent
from marketing_agent import ArtConnectMarketingAgent
import tempfile

# Configuración de la página
st.set_page_config(
    page_title="ArtConnect - Tu Galería de Arte Digital",
    page_icon="🎨",
    layout="wide"
)

# Inicialización de los agentes
@st.cache_resource
def load_agents():
    title_generator = ArtTitleGenerator()
    sales_agent = ArtSalesAgent()
    marketing_agent = ArtConnectMarketingAgent()
    return title_generator, sales_agent, marketing_agent

title_generator, sales_agent, marketing_agent = load_agents()

# Función para procesar la imagen
def process_image(uploaded_file):
    # Guardar la imagen temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    # Cargar la imagen
    input_image = Image.open(tmp_path)
    
    # Eliminar el fondo
    output_image = remove(input_image)
    
    # Convertir a numpy array para procesamiento con OpenCV
    img_array = np.array(output_image)
    
    # Convertir a BGR para OpenCV
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
    
    # Aplicar filtros artísticos
    # 1. Filtro de acuarela
    watercolor = cv2.stylization(img_bgr, sigma_s=60, sigma_r=0.6)
    
    # 2. Filtro de boceto
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    
    # 3. Filtro de pintura al óleo
    oil_painting = cv2.xphoto.oilPainting(img_bgr, 7, 1)
    
    # Convertir de vuelta a PIL Image
    watercolor_pil = Image.fromarray(cv2.cvtColor(watercolor, cv2.COLOR_BGR2RGB))
    sketch_pil = Image.fromarray(sketch)
    oil_painting_pil = Image.fromarray(cv2.cvtColor(oil_painting, cv2.COLOR_BGR2RGB))
    
    # Limpiar archivo temporal
    os.unlink(tmp_path)
    
    return {
        'original': input_image,
        'watercolor': watercolor_pil,
        'sketch': sketch_pil,
        'oil_painting': oil_painting_pil
    }

# Interfaz principal
st.title("🎨 ArtConnect - Tu Galería de Arte Digital")
st.markdown("""
    ### Transforma tus fotos en obras de arte
    Sube una imagen y descubre cómo se vería como una obra de arte en diferentes estilos.
""")

# Carga de imagen
uploaded_file = st.file_uploader("Sube una imagen", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    with st.spinner('Procesando tu imagen...'):
        # Procesar la imagen
        processed_images = process_image(uploaded_file)
        
        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(processed_images['original'], caption="Imagen Original", use_column_width=True)
        
        with col2:
            st.image(processed_images['watercolor'], caption="Estilo Acuarela", use_column_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.image(processed_images['sketch'], caption="Estilo Boceto", use_column_width=True)
        
        with col4:
            st.image(processed_images['oil_painting'], caption="Estilo Pintura al Óleo", use_column_width=True)
        
        # Generar título artístico
        title = title_generator.generate_title(processed_images['original'])
        st.success(f"Título sugerido para tu obra: **{title}**")
        
        # Generar descripción de venta
        sales_description = sales_agent.generate_sales_description(
            processed_images['original'],
            title
        )
        st.info(f"Descripción para vender tu obra:\n\n{sales_description}")
        
        # Generar estrategia de marketing
        marketing_strategy = marketing_agent.generate_marketing_strategy(
            processed_images['original'],
            title
        )
        st.info(f"Estrategia de marketing:\n\n{marketing_strategy}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Desarrollado con ❤️ por ArtConnect</p>
        <p>© 2024 ArtConnect - Todos los derechos reservados</p>
    </div>
""", unsafe_allow_html=True) 