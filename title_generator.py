import random
from transformers import pipeline

class ArtConnectTitleGenerator:
    def __init__(self):
        self.generator = pipeline('text-generation', model='gpt2')
        self.adjectives = [
            "Ethereal", "Mystical", "Vibrant", "Serene", "Dynamic",
            "Timeless", "Whimsical", "Bold", "Delicate", "Captivating",
            "Enigmatic", "Radiant", "Harmonious", "Expressive", "Dreamlike"
        ]
        
        self.nouns = [
            "Horizon", "Journey", "Reflection", "Essence", "Moment",
            "Whisper", "Dance", "Silence", "Light", "Shadow",
            "Memory", "Dream", "Soul", "Spirit", "Vision"
        ]
        
        self.art_styles = [
            "Abstract", "Impressionist", "Surreal", "Contemporary",
            "Modern", "Expressionist", "Minimalist", "Cubist"
        ]
        
        self.colors = [
            "Azure", "Crimson", "Emerald", "Golden", "Indigo",
            "Violet", "Amber", "Pearl", "Onyx", "Ruby"
        ]
    
    def generate_title(self, artwork_info):
        # Generate a creative title based on the artwork's characteristics
        style = random.choice(self.art_styles)
        adjective = random.choice(self.adjectives)
        noun = random.choice(self.nouns)
        color = random.choice(self.colors)
        
        # Create different title patterns
        patterns = [
            f"{adjective} {noun}",
            f"{color} {noun}",
            f"{style} {noun}",
            f"{adjective} {style} {noun}",
            f"{color} {style} {noun}",
            f"{adjective} {color} {noun}",
            f"The {adjective} {noun} of {color}",
            f"{style} {adjective} {noun}"
        ]
        
        # Select a random pattern
        base_title = random.choice(patterns)
        
        # Add a subtitle if the artwork has specific tags
        if artwork_info.get("tags"):
            style_tags = [tag for tag in artwork_info["tags"] if tag in self.art_styles]
            if style_tags:
                subtitle = f" - A {style_tags[0]} Exploration"
                return base_title + subtitle
        
        return base_title
    
    def generate_description(self, title, artwork_info):
        # Generate a poetic description based on the title and artwork info
        descriptions = [
            f"'{title}' captures the essence of {', '.join(artwork_info['tags'][:2])} through its unique composition and emotional depth.",
            f"This piece, '{title}', represents a harmonious blend of {', '.join(artwork_info['tags'][:2])}, creating a visual symphony that resonates with the viewer.",
            f"In '{title}', the artist masterfully combines elements of {', '.join(artwork_info['tags'][:2])}, resulting in a work that transcends traditional boundaries.",
            f"'{title}' is a testament to the power of {', '.join(artwork_info['tags'][:2])}, inviting viewers to explore its layers of meaning and emotion."
        ]
        
        return random.choice(descriptions) 