import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime
import random
from transformers import pipeline
from PIL import Image

class ArtSalesAgent:
    def __init__(self):
        self.galleries_db = self._load_galleries_db()
        self.clients_db = self._load_clients_db()
        self.email_templates = self._load_email_templates()
        self.image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    
    def _load_galleries_db(self):
        # This would typically load from a database or file
        # For now, using a sample database
        return [
            {
                "name": "Modern Art Gallery",
                "email": "contact@modernart.com",
                "location": "New York",
                "specialties": ["contemporary", "modern", "abstract"],
                "price_range": "$$$"
            },
            {
                "name": "Classic Arts",
                "email": "info@classicarts.com",
                "location": "London",
                "specialties": ["classical", "renaissance", "baroque"],
                "price_range": "$$$$"
            },
            {
                "name": "Urban Gallery",
                "email": "hello@urbangallery.com",
                "location": "Los Angeles",
                "specialties": ["street art", "urban", "contemporary"],
                "price_range": "$$"
            }
        ]
    
    def _load_clients_db(self):
        # Sample collector database
        return [
            {
                "name": "John Collector",
                "email": "john@example.com",
                "preferences": ["abstract", "modern"],
                "budget": "$$$"
            },
            {
                "name": "Sarah Artlover",
                "email": "sarah@example.com",
                "preferences": ["contemporary", "minimalist"],
                "budget": "$$$$"
            },
            {
                "name": "Mike Investor",
                "email": "mike@example.com",
                "preferences": ["classical", "renaissance"],
                "budget": "$$$$$"
            }
        ]
    
    def _load_email_templates(self):
        return {
            "gallery": """
            Dear {gallery_name},
            
            I hope this email finds you well. I am writing to introduce a remarkable artwork that I believe would be a perfect fit for your gallery.
            
            Title: {artwork_title}
            Style: {artwork_style}
            Estimated Price: {artwork_price}
            
            {artwork_description}
            
            The piece aligns perfectly with your gallery's focus on {gallery_specialties} and would make a valuable addition to your collection.
            
            I would be delighted to arrange a viewing at your convenience. Please let me know if you would like to see more details or discuss potential collaboration.
            
            Best regards,
            ArtConnect Sales Team
            """,
            
            "client": """
            Dear {client_name},
            
            I hope you're doing well. I wanted to share an exclusive opportunity with you regarding a unique artwork that matches your interest in {client_preferences}.
            
            Title: {artwork_title}
            Style: {artwork_style}
            Price: {artwork_price}
            
            {artwork_description}
            
            This piece would make a stunning addition to your collection. As a valued client, you have priority access to this artwork before it's made available to the general market.
            
            Please let me know if you would like to arrange a private viewing or discuss the details further.
            
            Warm regards,
            ArtConnect Sales Team
            """
        }
    
    def find_matching_galleries(self, artwork_info):
        matching_galleries = []
        for gallery in self.galleries_db:
            if any(tag in gallery["specialties"] for tag in artwork_info["tags"]):
                matching_galleries.append(gallery)
        return matching_galleries
    
    def find_matching_clients(self, artwork_info):
        matching_clients = []
        for client in self.clients_db:
            if any(tag in client["preferences"] for tag in artwork_info["tags"]):
                matching_clients.append(client)
        return matching_clients
    
    def generate_sales_report(self, artwork_info):
        matching_galleries = self.find_matching_galleries(artwork_info)
        matching_clients = self.find_matching_clients(artwork_info)
        
        return {
            "galleries_contacted": len(matching_galleries),
            "clients_contacted": len(matching_clients),
            "potential_markets": [
                f"{gallery['location']} ({gallery['name']})" for gallery in matching_galleries
            ],
            "recommended_next_steps": [
                "Schedule gallery presentations",
                "Prepare artwork documentation",
                "Set up client viewings",
                "Create marketing materials",
                "Plan exhibition strategy"
            ]
        }
    
    def contact_galleries(self, artwork_info):
        matching_galleries = self.find_matching_galleries(artwork_info)
        for gallery in matching_galleries:
            email_content = self.email_templates["gallery"].format(
                gallery_name=gallery["name"],
                artwork_title=artwork_info["title"],
                artwork_style=", ".join(artwork_info["tags"]),
                artwork_price=artwork_info["estimated_price"],
                artwork_description=artwork_info["description"],
                gallery_specialties=", ".join(gallery["specialties"])
            )
            # In a real implementation, this would send actual emails
            print(f"Email sent to gallery: {gallery['name']}")
    
    def contact_clients(self, artwork_info):
        matching_clients = self.find_matching_clients(artwork_info)
        for client in matching_clients:
            email_content = self.email_templates["client"].format(
                client_name=client["name"],
                client_preferences=", ".join(client["preferences"]),
                artwork_title=artwork_info["title"],
                artwork_style=", ".join(artwork_info["tags"]),
                artwork_price=artwork_info["estimated_price"],
                artwork_description=artwork_info["description"]
            )
            # In a real implementation, this would send actual emails
            print(f"Email sent to client: {client['name']}")

    def generate_sales_description(self, image, title):
        try:
            # Generar descripción de la imagen
            description = self.image_to_text(image)[0]['generated_text']
            
            # Crear descripción de venta
            sales_description = f"""
            {title}
            
            {description.capitalize()}
            
            Esta obra única captura la esencia del arte contemporáneo, combinando técnicas tradicionales con un enfoque moderno.
            Perfecta para coleccionistas que buscan piezas únicas y significativas.
            
            Características:
            - Técnica mixta
            - Obra original
            - Lista para colgar
            - Certificado de autenticidad incluido
            
            Inversión en arte que apreciará con el tiempo.
            """
            
            return sales_description
        except Exception as e:
            return f"Error al generar la descripción: {str(e)}" 