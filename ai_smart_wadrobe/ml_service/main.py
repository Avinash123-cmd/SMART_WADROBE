from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from datetime import datetime
import json

app = FastAPI(title="Smart Wardrobe ML Service", docs_url="/docs")

# Simple in-memory model for demo
class DemoModel:
    def predict(self, features):
        # Demo logic: higher score for moderate temperatures
        temp = features.get('temperature', 25)
        if 20 <= temp <= 28:
            return 0.85
        elif temp < 10 or temp > 35:
            return 0.4
        else:
            return 0.7

model = DemoModel()

class PredictionRequest(BaseModel):
    temperature: float
    humidity: float = 50.0
    occasion: str = "daily"
    user_id: int = 1

@app.get("/")
def root():
    return {
        "service": "Smart Wardrobe ML Service",
        "status": "running",
        "endpoints": ["/predict", "/health", "/docs"]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model_loaded": True
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Prepare features
        features = {
            'temperature': request.temperature,
            'humidity': request.humidity,
            'occasion': request.occasion
        }
        
        # Get prediction
        score = model.predict(features)
        
        # Generate recommendations
        recommendations = []
        occasions = {
            'daily': ['Casual Outfit', 'Comfort Wear', 'Everyday Style'],
            'formal': ['Business Formal', 'Office Wear', 'Professional Attire'],
            'party': ['Party Outfit', 'Evening Wear', 'Celebration Style']
        }
        
        for outfit in occasions.get(request.occasion, ['Smart Casual', 'Everyday Style']):
            recommendations.append({
                'name': outfit,
                'score': round(score - np.random.uniform(0, 0.1), 2),
                'description': f'Perfect for {request.occasion} occasion'
            })
        
        return {
            "status": "success",
            "temperature": request.temperature,
            "occasion": request.occasion,
            "overall_score": round(score, 2),
            "recommendations": sorted(recommendations, key=lambda x: x['score'], reverse=True)[:3]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)