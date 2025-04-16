import streamlit as st
import cv2
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from rembg import remove
import faiss
import os
import random
from sales_agent import ArtConnectSalesAgent
from title_generator import ArtConnectTitleGenerator
from marketing_agent import ArtConnectMarketingAgent

# Page configuration
st.set_page_config(
    page_title="ArtConnect - Art Analysis and Sales Platform",
    page_icon="🎨",
    layout="wide"
)

# Title and description
st.title("🎨 ArtConnect - Connecting Art with the World")
st.markdown("""
ArtConnect is your intelligent platform for art analysis and sales, providing:
- Automatic image analysis and enhancement
- AI-powered title and description generation
- Smart tagging and categorization
- Market-based price suggestions
- Gallery and collector outreach
- Sales and marketing assistance
""")

# Model initialization
@st.cache_resource
def load_models():
    # Load CLIP model for image analysis
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

# Image processing function
def process_image(image):
    # Convert to PIL format
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    # Remove background
    image_nobg = remove(image)
    
    # Enhance lighting
    image_np = np.array(image_nobg)
    lab = cv2.cvtColor(image_np, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    
    return enhanced

# Image analysis function
def analyze_image(image, model, processor):
    # Process image with CLIP
    inputs = processor(images=image, return_tensors="pt", padding=True)
    outputs = model.get_image_features(**inputs)
    
    # Here would go the logic to get tags, description and price
    # For now, we return a dictionary with example information
    return {
        "title": "Analyzed Artwork",
        "description": "A beautiful piece of art that shows...",
        "tags": ["painting", "modern art", "abstract"],
        "estimated_price": "$500 - $1000"
    }

# Main interface
def main():
    model, processor = load_models()
    sales_agent = ArtConnectSalesAgent()
    title_generator = ArtConnectTitleGenerator()
    marketing_agent = ArtConnectMarketingAgent()
    
    # Upload image
    uploaded_file = st.file_uploader("Upload an artwork image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Read image
        image = Image.open(uploaded_file)
        
        # Show original image
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Process image
        processed_image = process_image(image)
        
        # Show processed image
        st.image(processed_image, caption="Processed Image", use_container_width=True)
        
        # Analyze image
        if st.button("Analyze Artwork"):
            with st.spinner("Analyzing artwork..."):
                analysis = analyze_image(image, model, processor)
                
                # Generate creative title and description
                generated_title = title_generator.generate_title(analysis)
                generated_description = title_generator.generate_description(generated_title, analysis)
                
                # Update analysis with generated content
                analysis["title"] = generated_title
                analysis["description"] = generated_description
                
                # Show analysis results
                st.subheader("Analysis Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Title:**", analysis["title"])
                    st.write("**Description:**", analysis["description"])
                
                with col2:
                    st.write("**Tags:**", ", ".join(analysis["tags"]))
                    st.write("**Estimated Price:**", analysis["estimated_price"])
                
                # Generate marketing campaign
                if st.button("Generate Marketing Campaign"):
                    with st.spinner("Creating marketing campaign..."):
                        campaign = marketing_agent.generate_campaign_plan(analysis)
                        report = marketing_agent.generate_report(campaign)
                        
                        st.subheader("📢 Marketing Campaign Plan")
                        
                        st.write("**Campaign Summary:**")
                        st.write(report["summary"])
                        st.write(f"**Duration:** {report['duration']}")
                        st.write(f"**Platforms:** {report['platforms_used']}")
                        
                        st.write("**Weekly Plan:**")
                        st.text(report["weekly_highlights"])
                        
                        st.write("**Budget Allocation:**")
                        st.text(report["budget_summary"])
                        
                        st.write("**Expected Results:**")
                        for kpi, value in report["expected_results"].items():
                            st.write(f"- {kpi}: {value}")
                
                # Generate sales report
                sales_report = sales_agent.generate_sales_report(analysis)
                
                # Show sales report
                st.subheader("🤖 Sales and Marketing Report")
                
                st.write("**Market Reach:**")
                col3, col4 = st.columns(2)
                
                with col3:
                    st.write(f"Galleries to contact: {sales_report['galleries_contacted']}")
                    st.write("**Potential Markets:**")
                    for market in sales_report["potential_markets"]:
                        st.write(f"- {market}")
                
                with col4:
                    st.write(f"Clients to contact: {sales_report['clients_contacted']}")
                    st.write("**Recommended Next Steps:**")
                    for step in sales_report["recommended_next_steps"]:
                        st.write(f"- {step}")
                
                # Contact galleries and clients
                if st.button("Start Marketing Campaign"):
                    with st.spinner("Contacting galleries and clients..."):
                        sales_agent.contact_galleries(analysis)
                        sales_agent.contact_clients(analysis)
                        st.success("Marketing campaign initiated! Emails have been sent to galleries and clients.")

if __name__ == "__main__":
    main() 