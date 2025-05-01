import torch
from transformers import pipeline
from PIL import Image

class ArtTitleGenerator:
    def __init__(self):
        self.image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    
    def generate_title(self, image):
        # Generar descripción de la imagen
        description = self.image_to_text(image)[0]['generated_text']
        
        # Crear título artístico basado en la descripción
        title = f"'{description.capitalize()}'"
        
        return title

    def generate_description(self, title, artwork_info):
        # Generate a poetic description based on the title and artwork info
        descriptions = [
            f"'{title}' captures the essence of {', '.join(artwork_info['tags'][:2])} through its unique composition and emotional depth.",
            f"This piece, '{title}', represents a harmonious blend of {', '.join(artwork_info['tags'][:2])}, creating a visual symphony that resonates with the viewer.",
            f"In '{title}', the artist masterfully combines elements of {', '.join(artwork_info['tags'][:2])}, resulting in a work that transcends traditional boundaries.",
            f"'{title}' is a testament to the power of {', '.join(artwork_info['tags'][:2])}, inviting viewers to explore its layers of meaning and emotion."
        ]
        
        return random.choice(descriptions) 