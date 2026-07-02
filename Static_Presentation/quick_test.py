# test_quick.py - Fixed GPT Image model test

import os
import time
import requests
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def save_image(image_data, model_name):
    """Save image from either URL or base64"""
    timestamp = int(time.time())
    filename = f"test_{model_name}_{timestamp}.png"

    # URL case
    if isinstance(image_data, str) and image_data.startswith("http"):
        img_bytes = requests.get(image_data).content

    # base64 case
    else:
        img_bytes = base64.b64decode(image_data)

    with open(filename, "wb") as f:
        f.write(img_bytes)

    print(f"💾 Saved: {filename}")


def quick_test():
    """Quick test for GPT image models"""

    models = [
        "gpt-image-2",
        "gpt-image-1.5",
        "gpt-image-1-mini"
    ]
    
    for model in models:
        try:
            print(f"\n🧪 Testing {model}...")
            #prompt  ="Create a professional graphical abstract slide (scientific infographic style) titled 'Project Overview & Stakeholder' for a machine learning project. The slide should visually communicate a pipeline from stakeholder need to data source to solution and outputs. Include: (1) Stakeholder section: Securitas Security Operations, Security Operations Manager, with pain point that manual review of customer feedback is time-consuming and reactive, and need for proactive identification of security risks across client locations. (2) Solution section: a predictive NLP model that analyzes customer reviews to automatically identify business categories and detect security risks. (3) Data Source section: Yelp Open Dataset with 50,000+ reviews sampled from 6.9M total reviews, covering 7 business categories (Restaurants, Retail, Health, Services, Hospitality, Entertainment, Education), and containing rich free-text fields with metadata such as star ratings, timestamps, location, and tips. (4) Key Outputs section: Text Analysis using NLP for security signals, Risk Scoring for multi-category security risk assessment, Category Prediction for business type classification, and Tip Data Integration for enhanced detection from short-form feedback. Visual style should be a clean modern scientific infographic with a left-to-right or top-to-bottom flow diagram, arrows showing data flow, and icons representing stakeholder, dataset, AI model, text analysis, and risk alerts. Use a corporate color palette (blue, grey, white), minimal text, and strong visual hierarchy suitable for an academic machine learning presentation."
            #prompt = "Create a professional graphical abstract infographic titled 'Technical Approach & Methodology' for a machine learning NLP security risk prediction system. Show a clean pipeline from left to right: raw Yelp reviews → feature engineering → model inputs → security risk detection outputs. Emphasize text-based feature engineering. Include visual blocks for TF-IDF vectorization (5,000 features), word n-grams (1–2 words), and security keyword detection. Add a structured table-style visualization of security-specific features grouped into categories: Crime (robbery, theft, stolen), Safety (unsafe, danger, hazard), Personnel (security, guard, police), Incidents (fight, aggressive, alarm), Environment (dark, lighting, parking). Include additional feature icons for sentiment analysis (VADER), urgency markers (exclamation, caps), time features (night vs day), business context (open status, review velocity), and tip data (sentiment + keywords). Use a clean scientific diagram style with arrows, modular blocks, minimal text, and corporate color palette (blue, grey, white). Make it visually structured like a research paper graphical abstract."
            #prompt = "Create a professional ML performance evaluation graphical abstract titled 'Model Performance Results'. Show a clean comparison table visual in the center with four models: Text Only (89.17%), Text + Base Security (89.17%), Text + Security Categories (89.23%), and Text + Security + Tips (89.63%) highlighted as best model. Emphasize improvement progression with arrows showing incremental gains (+0.00%, +0.06%, +0.46%). Add a highlighted badge for best model: 'Text + Security Features + Tip Data'. Include performance metrics section showing Accuracy 89.63%, F1-score 0.885, Precision 89.2%, Recall 89.5%. On the right side, include a category-wise performance bar chart: Restaurants (98.50%), Health (77.97%), Services (78.93%), Retail (46.65%), Hospitality (62.44%), Entertainment (30.43%), Education (2.13%). Add a key insight callout: 'Tip data improves accuracy by +0.46%'. Use clean academic dashboard style, minimal text, blue/grey corporate palette, and clear data visualization emphasis." 
            #prompt = "Create a scientific graphical abstract titled 'Feature Importance Analysis' for a machine learning security risk model. Show a ranked bar chart of top 10 features with importance values: std_tip_sentiment (2.13%), tip_count (2.08%), max_tip_sentiment (1.80%), avg_tip_sentiment (1.77%), food (1.43%), avg_tip_age_days (1.33%), newest_tip_age_days (1.17%), min_tip_sentiment (0.97%), appointment (0.83%), store (0.82%). Visually differentiate feature types using color coding: Tip features (majority), Text features, Base features. Add a pie chart showing feature type distribution: Text 60%, Tip 28%, Base 12%. Include a side panel showing security risk patterns: mentions peak 8pm–12am, high-risk categories Entertainment and Hospitality, low-risk Health and Education, and keyword frequencies (unsafe, dark, security). Add a clean research infographic style with structured charts, minimal text, and clear labeling."
            #prompt = "Create a graphical abstract titled 'Tip Data Impact Analysis' for a security risk prediction system. Show a central dashboard visualization highlighting tip effectiveness: 8 test cases, 1 improvement, 12.5% effectiveness, +0.46% accuracy gain. Include a horizontal correlation bar chart showing: Security Tip Ratio (72%), Total Security Keywords (68%), Negative Sentiment (61%), Recent Tips <15 days (55%), Tip Count (43%). Add a visual flow showing tips as early warning signals before formal reviews. Include key insights callouts: security tip ratio is strongest predictor, recent tips are most valuable, sentiment shift indicates emerging issues, and multiple tips signal high risk. Add strategic recommendation icons: real-time alerts, prioritization of >50% security tips, and combined review + tip analysis. Use clean analytical dashboard style with emphasis on risk intelligence and early warning signals."
            prompt = "Create a professional graphical abstract titled 'Deployment & Future Roadmap' for a machine learning security risk prediction system. Show a 3-phase roadmap timeline from left to right. Phase 1 MVP (Month 1): API deployment (FastAPI/Flask), real-time review processing, risk alerts. Phase 2 Enhancement (Months 2–3): real-time dashboard, integration with security systems, feedback loop, multilingual support. Phase 3 Scale (Months 4–6): multi-client support, predictive analytics, mobile alerts, response system integration. Include a technical stack section with icons: Python 3.8+, Scikit-learn, FastAPI/Flask, PostgreSQL/vector DB, Docker. Add a KPI panel showing: >85% detection rate, <15% false positives, <8h response time, >90% adoption, 3–5x ROI. Include a future research section with icons for image analysis, social media monitoring, IoT integration, predictive forecasting, and explainable AI (SHAP/LIME). Use clean enterprise architecture style with roadmap visualization and corporate blue-grey palette."
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size="1024x1024",
                n=1,
                quality="high"
            )

            img = response.data[0]

            print(f"✅ {model} works!")

            if hasattr(img, "url") and img.url:
                print(f"🔗 URL: {img.url}")
                save_image(img.url, model)

            elif hasattr(img, "b64_json") and img.b64_json:
                print("🧾 Received base64 image")
                save_image(img.b64_json, model)

            else:
                print("⚠️ No image data returned")

            return model

        except Exception as e:
            print(f"❌ {model} failed: {e}")

    print("\n❌ No working models found")
    return None


if __name__ == "__main__":
    print("Testing GPT Image Models...")
    print("-" * 50)
    quick_test()