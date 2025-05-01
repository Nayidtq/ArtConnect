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
            # Generate image description
            description = self.image_to_text(image)[0]['generated_text']
            
            # Create marketing strategy
            strategy = f"""
            Marketing Strategy for '{title}'
            
            Artwork Description:
            {description.capitalize()}
            
            Recommended Platforms:
            - Instagram: Perfect for showcasing the artwork in high quality
            - Facebook: Ideal for reaching collectors and galleries
            - Pinterest: Excellent for inspiration and discovery
            - LinkedIn: For connecting with art professionals
            
            Recommended Actions:
            1. Create a series of posts showing different aspects of the artwork
            2. Share the creative process behind the piece
            3. Publish testimonials from art experts
            4. Organize a virtual exhibition
            5. Collaborate with art world influencers
            
            Estimated Budget:
            - Social media advertising: $200-500
            - Professional photography: $100-300
            - Promotional material design: $150-400
            - Virtual event: $300-800
            
            Expected Results:
            - 30% increase in followers
            - 50-100 interactions per post
            - 5-10 gallery contacts
            - 3-5 purchase inquiries
            """
            
            return strategy
        except Exception as e:
            return f"Error generating marketing strategy: {str(e)}" 