"""Quick verification test for the 4 new real-data endpoints."""
import sys
import os
import importlib.util

# Load app.py explicitly to avoid conflict with app/ package
spec = importlib.util.spec_from_file_location(
    "main_app",
    os.path.join(os.path.dirname(__file__), "app.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
app = mod.app

def main():
    client = app.test_client()
    passed = 0
    failed = 0

    def check(label, cond, detail=""):
        nonlocal passed, failed
        if cond:
            print(f"  PASS  {label} {detail}")
            passed += 1
        else:
            print(f"  FAIL  {label} {detail}")
            failed += 1

    print("\n=== SkillGenome X - Real Data Endpoint Tests ===\n")

    # 1. /api/model-status (initial state)
    r = client.get('/api/model-status')
    d = r.get_json()
    check("GET /api/model-status returns 200", r.status_code == 200)
    check("model-status has 'trained' key", 'trained' in d)
    check("model-status has 'features' key", 'features' in d and len(d['features']) > 0)
    print(f"     trained={d.get('trained')}, source={d.get('data_source')}")

    # 2. /api/train-model
    r = client.post('/api/train-model', json={})
    d = r.get_json()
    check("POST /api/train-model returns 200", r.status_code == 200)
    check("train-model status=success", d.get('status') == 'success')
    check("train-model has r2_score", isinstance(d.get('r2_score'), (int, float)))
    check("train-model has feature_importances", bool(d.get('feature_importances')))
    check("train-model has dataset_rows > 0", (d.get('dataset_rows') or 0) > 0)
    print(f"     r2={d.get('r2_display')}, rows={d.get('dataset_rows')}")

    # 3. /api/predict-skill-risk (after training)
    payload = {
        'literacy_rate': 80.0,
        'internet_penetration': 60.0,
        'workforce_participation': 58.0,
        'urban_population': 40.0,
        'per_capita_income': 180000,
        'skill_training_count': 75000
    }
    r = client.post('/api/predict-skill-risk', json=payload)
    d = r.get_json()
    check("POST /api/predict-skill-risk returns 200", r.status_code == 200)
    check("predict has predicted_unemployment", 'predicted_unemployment' in d)
    check("predict has risk_level", d.get('risk_level') in ('Low', 'Moderate', 'High'))
    check("predict has feature_contributions", bool(d.get('feature_contributions')))
    check("predict skill_risk_score 0-100", 0 <= (d.get('skill_risk_score') or 0) <= 100)
    print(f"     unemployment={d.get('predicted_unemployment')}%, risk={d.get('risk_level')}, score={d.get('skill_risk_score')}")

    # 4. /api/model-status post-training
    r = client.get('/api/model-status')
    d = r.get_json()
    check("model-status trained=True after training", d.get('trained') == True)
    check("model-status r2_score > 0 after training", (d.get('r2_score') or 0) > 0)
    print(f"     trained={d.get('trained')}, r2={d.get('r2_display')}, rows={d.get('dataset_rows')}")

    # 5. /api/health still works
    r = client.get('/api/health')
    check("GET /api/health still works", r.status_code == 200)

    # 6. /api/predict still works (original endpoint)
    r = client.post('/api/predict', json={
        'context': {'domain': 'Technology', 'opportunity_level': 'High'},
        'signals': {'creation_output': 80, 'digital_presence': 80, 'projects': 5}
    })
    check("POST /api/predict (legacy) still works", r.status_code == 200)

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    if failed > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
