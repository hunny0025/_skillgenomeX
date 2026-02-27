"""
services/prediction_service.py – Prediction Business Logic
SkillGenome X

Encapsulates all prediction logic: skill scoring, explainability,
workforce assessment, recommendations, opportunities, and trust metadata.
"""
import numpy as np
from pipeline.preprocessing import FEATURE_COLUMNS


class PredictionService:
    """Stateless service that takes a model + signals and produces predictions."""

    @staticmethod
    def predict(model_state: dict, signals: dict, domain: str = "General") -> dict:
        """
        Run the full prediction pipeline.

        Args:
            model_state: dict with skill_model, anomaly_model, training_score, feature_names
            signals: dict of behavioral dimension values (0-100)
            domain: selected work domain

        Returns:
            Full prediction result dict ready for JSON response.
        """
        feature_names = [
            'creation_output', 'learning_behavior', 'experience_consistency',
            'economic_activity', 'innovation_problem_solving', 'collaboration_community',
            'offline_capability', 'digital_presence', 'learning_hours', 'projects'
        ]
        features = [signals.get(f, 50) for f in feature_names]

        # ── Model prediction ──
        if model_state.get('active') and model_state.get('skill_model'):
            predicted_score = float(model_state['skill_model'].predict([features])[0])
            predicted_score = max(0, min(100, predicted_score))
            confidence = model_state.get('training_score', 75)
        else:
            predicted_score = sum(features) / len(features)
            confidence = 50

        # ── Anomaly detection ──
        is_anomaly = False
        if model_state.get('anomaly_model'):
            is_anomaly = bool(model_state['anomaly_model'].predict([features])[0] == -1)
            if is_anomaly:
                confidence = max(30, confidence - 20)

        # ── Explainability ──
        explanations = PredictionService._explain(model_state, features, feature_names)

        # ── Workforce assessment ──
        workforce = {
            'work_capacity': 'High' if predicted_score > 75 else 'Moderate' if predicted_score > 45 else 'Low',
            'growth_potential': 'High' if signals.get('learning_behavior', 0) > 60 else 'Moderate' if signals.get('learning_behavior', 0) > 30 else 'Low',
            'risk_level': 'Low' if predicted_score > 70 else 'Moderate' if predicted_score > 40 else 'High'
        }

        # ── Recommendations ──
        recommendations = PredictionService._build_recommendations(predicted_score, signals)

        # ── Opportunities ──
        opportunities = PredictionService._build_opportunities(predicted_score, signals, domain)

        # ── Trust metadata ──
        trust = {
            'data_source': 'Self-reported structured inputs',
            'confidence_level': 'Medium' if confidence > 50 else 'Low',
            'note': 'Future versions will integrate government and digital data sources.'
        }

        return {
            'score': round(predicted_score, 1),
            'level': 'Expert' if predicted_score > 80 else 'Advanced' if predicted_score > 60 else 'Intermediate',
            'confidence': round(confidence, 1),
            'is_anomaly': is_anomaly,
            'workforce_assessment': workforce,
            'recommendations': recommendations,
            'opportunities': opportunities,
            'trust': trust,
            'explanations': explanations
        }

    @staticmethod
    def _explain(model_state, features, feature_names):
        """Generate top positive/negative factor explanations."""
        if not model_state.get('skill_model') or not hasattr(model_state['skill_model'], 'feature_importances_'):
            return {'top_positive': [], 'top_negative': []}

        importances = model_state['skill_model'].feature_importances_
        contributions = []
        for i, name in enumerate(feature_names):
            impact = float(importances[i]) * (features[i] - 50)
            contributions.append({'feature': name, 'value': features[i], 'impact': round(impact, 2)})

        contributions.sort(key=lambda x: x['impact'], reverse=True)
        return {
            'top_positive': [c for c in contributions if c['impact'] > 0][:3],
            'top_negative': [c for c in contributions if c['impact'] < 0][-3:]
        }

    @staticmethod
    def _build_recommendations(score, signals):
        """Context-aware action recommendations."""
        recs = []
        digital = signals.get('digital_presence', 50)
        economic = signals.get('economic_activity', 50)

        if score < 50:
            recs.append({'action': 'Join a skill training program in your domain', 'category': 'training', 'priority': 'high'})
        if digital < 40:
            recs.append({'action': 'Start accepting digital payments (UPI)', 'category': 'digital', 'priority': 'high'})
            recs.append({'action': 'Create a WhatsApp Business profile', 'category': 'digital', 'priority': 'medium'})
        if economic < 40:
            recs.append({'action': 'Explore gig work platforms for additional income', 'category': 'income', 'priority': 'medium'})
        if score > 70:
            recs.append({'action': 'Mentor others and expand customer reach', 'category': 'growth', 'priority': 'low'})
        if not recs:
            recs.append({'action': 'Keep building consistency — you\'re on track', 'category': 'growth', 'priority': 'low'})
        return recs

    @staticmethod
    def _build_opportunities(score, signals, domain):
        """Domain-aware growth opportunities."""
        opps = {'training': [], 'government_schemes': [], 'platforms': [], 'digital_growth': []}

        if score < 60:
            opps['training'].extend(['NSDC Skill India courses (free)', 'State-level skill programs'])
        opps['training'].append('Industry-specific certification courses')

        if signals.get('economic_activity', 50) < 50:
            opps['government_schemes'].extend([
                'Mudra Loan (up to ₹10 lakh)', 'PMEGP', 'State skill development missions'
            ])

        platform_map = {
            'Retail & Sales': ['Meesho', 'Flipkart Seller Hub', 'Amazon Easy'],
            'Service Industry': ['Urban Company', 'Housejoy'],
            'Logistics & Delivery': ['Swiggy', 'Zomato', 'Porter'],
            'Agriculture & Allied': ['DeHaat', 'AgroStar'],
            'Creative & Media': ['Fiverr', '99designs'],
            'Entrepreneurship': ['IndiaMART', 'GeM Portal'],
        }
        opps['platforms'] = platform_map.get(domain, ['Explore online marketplaces'])

        if signals.get('digital_presence', 50) < 50:
            opps['digital_growth'].extend(['Set up UPI payments', 'Create WhatsApp Business'])
        opps['digital_growth'].append('Build an online presence for your work')

        return opps
