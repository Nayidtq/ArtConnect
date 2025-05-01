import random
from datetime import datetime, timedelta
import json
import os
from transformers import pipeline
from PIL import Image

class ArtConnectMarketingAgent:
    def __init__(self):
        self.image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
        self.social_media_platforms = [
            "Instagram",
            "Facebook",
            "Twitter",
            "Pinterest",
            "LinkedIn"
        ]
        
        self.marketing_strategies = {
            "social_media": [
                "Daily content posting",
                "Featured stories",
                "Creative process Reels/TikToks",
                "Artist live sessions",
                "Interactive polls and questions",
                "Collaborations with other artists"
            ],
            "email": [
                "Weekly newsletter",
                "Virtual event invitations",
                "Exclusive offers",
                "Behind-the-scenes content",
                "Collector testimonials"
            ],
            "events": [
                "Virtual exhibition",
                "Gallery launch",
                "Artist workshop",
                "Charity auction",
                "Networking event"
            ]
        }
        
        self.content_types = {
            "images": [
                "Creative process photos",
                "Artwork details",
                "Space visualization photos",
                "Artwork comparisons",
                "Photos with collectors"
            ],
            "videos": [
                "Creation timelapse",
                "Studio tour",
                "Artist interview",
                "Expert reactions",
                "Related tutorial"
            ],
            "text": [
                "Artwork backstory",
                "Technical analysis",
                "Testimonials",
                "Art curiosities",
                "Historical comparisons"
            ]
        }
    
    def generate_campaign_plan(self, artwork_info, duration_days=30):
        """Generates a detailed marketing campaign plan"""
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)
        
        campaign = {
            "artwork_info": artwork_info,
            "duration": f"{duration_days} days",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "platforms": random.sample(self.social_media_platforms, 3),
            "weekly_plan": self._generate_weekly_plan(),
            "content_calendar": self._generate_content_calendar(duration_days),
            "budget_allocation": self._generate_budget_allocation(),
            "kpis": self._generate_kpis()
        }
        
        return campaign
    
    def _generate_weekly_plan(self):
        """Generates a weekly activity plan"""
        weekly_plan = []
        for week in range(1, 5):
            week_plan = {
                "week": week,
                "social_media": random.sample(self.marketing_strategies["social_media"], 2),
                "email": random.sample(self.marketing_strategies["email"], 1),
                "events": random.sample(self.marketing_strategies["events"], 1) if week % 2 == 0 else []
            }
            weekly_plan.append(week_plan)
        return weekly_plan
    
    def _generate_content_calendar(self, duration_days):
        """Generates a content calendar"""
        calendar = []
        for day in range(duration_days):
            content_day = {
                "day": day + 1,
                "content": {
                    "images": random.sample(self.content_types["images"], 1),
                    "videos": random.sample(self.content_types["videos"], 1) if day % 3 == 0 else [],
                    "text": random.sample(self.content_types["text"], 1)
                }
            }
            calendar.append(content_day)
        return calendar
    
    def _generate_budget_allocation(self):
        """Generates budget allocation"""
        total_budget = 1000  # Base budget in USD
        return {
            "social_media_ads": total_budget * 0.4,
            "content_creation": total_budget * 0.3,
            "events": total_budget * 0.2,
            "email_marketing": total_budget * 0.1
        }
    
    def _generate_kpis(self):
        """Generates KPIs for the campaign"""
        return {
            "engagement_rate": ">5%",
            "reach": ">10,000 people",
            "website_traffic": "+30%",
            "lead_generation": ">50 leads",
            "sales_conversion": ">2%"
        }
    
    def generate_report(self, campaign):
        """Generates a detailed campaign report"""
        report = {
            "summary": f"Marketing campaign for '{campaign['artwork_info']['title']}'",
            "duration": campaign["duration"],
            "platforms_used": ", ".join(campaign["platforms"]),
            "weekly_highlights": self._format_weekly_highlights(campaign["weekly_plan"]),
            "budget_summary": self._format_budget_summary(campaign["budget_allocation"]),
            "expected_results": campaign["kpis"]
        }
        return report
    
    def _format_weekly_highlights(self, weekly_plan):
        """Formats weekly highlights"""
        highlights = []
        for week in weekly_plan:
            week_str = f"Week {week['week']}:\n"
            week_str += f"- Social media: {', '.join(week['social_media'])}\n"
            week_str += f"- Email: {week['email'][0]}\n"
            if week['events']:
                week_str += f"- Event: {week['events'][0]}\n"
            highlights.append(week_str)
        return "\n".join(highlights)
    
    def _format_budget_summary(self, budget):
        """Formats budget summary"""
        return "\n".join([f"- {category}: ${amount:.2f}" for category, amount in budget.items()])

    def generate_marketing_strategy(self, image, title):
        try:
            # Generar descripción de la imagen
            description = self.image_to_text(image)[0]['generated_text']
            
            # Crear estrategia de marketing
            strategy = f"""
            Estrategia de Marketing para '{title}'
            
            Descripción de la obra:
            {description.capitalize()}
            
            Plataformas recomendadas:
            - Instagram: Perfecta para mostrar la obra en alta calidad
            - Facebook: Ideal para llegar a coleccionistas y galerías
            - Pinterest: Excelente para inspiración y descubrimiento
            - LinkedIn: Para conectar con profesionales del arte
            
            Acciones recomendadas:
            1. Crear una serie de posts mostrando diferentes aspectos de la obra
            2. Compartir el proceso creativo detrás de la pieza
            3. Publicar testimonios de expertos en arte
            4. Organizar una exposición virtual
            5. Colaborar con influencers del mundo del arte
            
            Presupuesto estimado:
            - Publicidad en redes sociales: $200-500
            - Fotografía profesional: $100-300
            - Diseño de material promocional: $150-400
            - Evento virtual: $300-800
            
            Resultados esperados:
            - Aumento del 30% en seguidores
            - 50-100 interacciones por publicación
            - 5-10 contactos de galerías
            - 3-5 consultas de compra
            """
            
            return strategy
        except Exception as e:
            return f"Error al generar la estrategia de marketing: {str(e)}" 