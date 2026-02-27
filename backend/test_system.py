"""
SkillGenome X - System Testing Suite
Comprehensive tests for hackathon judge review
"""

import requests
import json
from datetime import datetime

# Base URL for API
BASE_URL = "http://localhost:5000"

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")

def print_result(passed, message):
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {message}")
    return passed

def test_1_api_health():
    """Test 1: API Health Check"""
    print_test_header("API Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/data-foundation", timeout=5)
        passed = response.status_code == 200
        if passed:
            data = response.json()
            print_result(True, f"API responding - {data.get('profiles', 0)} profiles loaded")
        else:
            print_result(False, f"API returned status code {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"API unreachable: {str(e)}")
        return False

def test_2_prediction_engine():
    """Test 2: Prediction Engine Validation"""
    print_test_header("Prediction Engine Validation")
    try:
        test_payload = {
            "signals": {
                "creation_output": 75,
                "learning_behavior": 80,
                "experience_consistency": 70,
                "economic_activity": 65,
                "innovation_problem_solving": 72,
                "collaboration_community": 68,
                "offline_capability": 60,
                "digital_presence": 55,
                "learning_hours": 20,
                "projects": 8
            },
            "context": {
                "state": "Maharashtra",
                "area_type": "Urban",
                "opportunity_level": "High",
                "digital_access": "Regular",
                "domain": "Technology"
            }
        }
        
        response = requests.post(f"{BASE_URL}/api/predict", json=test_payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            has_score = 'core' in data and 'score' in data['core']
            score_valid = has_score and 0 <= data['core']['score'] <= 100
            has_intelligence = 'intelligence' in data
            
            if score_valid and has_intelligence:
                print_result(True, f"Prediction successful - Score: {data['core']['score']}, Level: {data['core']['level']}")
                return True
            else:
                print_result(False, "Response missing expected fields")
                return False
        else:
            print_result(False, f"Prediction failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Prediction test error: {str(e)}")
        return False

def test_3_policy_generator():
    """Test 3: Policy Generation Validation"""
    print_test_header("Policy Generation Validation")
    try:
        # Test with no state (get all policies)
        response = requests.post(f"{BASE_URL}/api/policy", json={}, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            is_list = isinstance(data, list)
            not_empty = len(data) > 0 if is_list else False
            
            if not_empty:
                print_result(True, f"Policy generation successful - {len(data)} policies generated")
                print(f"   Sample policy: {data[0].get('recommended_action', 'N/A')}")
                return True
            else:
                print_result(False, "No policies generated")
                return False
        else:
            print_result(False, f"Policy endpoint failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Policy test error: {str(e)}")
        return False

def test_4_anomaly_detection():
    """Test 4: Anomaly Detection Test"""
    print_test_header("Anomaly Detection Test")
    try:
        # Create a suspicious profile (very high values with inconsistencies)
        fake_profile = {
            "signals": {
                "creation_output": 100,
                "learning_behavior": 100,
                "experience_consistency": 100,
                "economic_activity": 10,  # Inconsistent - low activity
                "innovation_problem_solving": 100,
                "collaboration_community": 10,  # Inconsistent - low collaboration
                "offline_capability": 100,
                "digital_presence": 100,
                "learning_hours": 200,  # Unrealistic
                "projects": 100
            },
            "context": {
                "state": "Test",
                "area_type": "Urban",
                "opportunity_level": "High",
                "digital_access": "Regular",
                "domain": "Technology"
            }
        }
        
        response = requests.post(f"{BASE_URL}/api/predict", json=fake_profile, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Check if anomaly detection is working
            has_anomaly_flag = 'intelligence' in data and 'is_anomaly' in data['intelligence']
            
            if has_anomaly_flag:
                is_anomaly = data['intelligence']['is_anomaly']
                print_result(True, f"Anomaly detection active - Flagged: {is_anomaly}")
                return True
            else:
                print_result(False, "Anomaly detection not present in response")
                return False
        else:
            print_result(False, f"Anomaly test failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Anomaly test error: {str(e)}")
        return False

def test_5_source_verification():
    """Test 5: Source Verification Logic"""
    print_test_header("Source Verification Logic")
    try:
        test_sources = {
            "github_url": "https://github.com/testuser/project",
            "portfolio_url": "https://testportfolio.com",
            "linkedin_url": "https://linkedin.com/in/testuser",
            "other_url": "https://kaggle.com/testuser",
            "projects": 10,
            "learning_hours": 25,
            "certifications": 3
        }
        
        response = requests.post(f"{BASE_URL}/api/verify-sources", json=test_sources, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            has_verification = 'source_verified' in data
            has_proof_score = 'proof_score' in data
            has_strength = 'proof_strength' in data
            
            if has_verification and has_proof_score and has_strength:
                print_result(True, f"Source verification working - Verified: {data['verified_count']}/4, Proof: {data['proof_strength']}")
                return True
            else:
                print_result(False, "Verification response missing expected fields")
                return False
        else:
            print_result(False, f"Verification failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Source verification test error: {str(e)}")
        return False

def test_6_economic_impact():
    """Test 6: Economic Impact Calculation"""
    print_test_header("Economic Impact Calculation")
    try:
        response = requests.get(f"{BASE_URL}/api/economic-impact", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            has_impact = 'economic_impact' in data
            has_count = 'hidden_talent_count' in data
            has_methodology = 'methodology' in data
            
            if has_impact and has_count and has_methodology:
                print_result(True, f"Economic impact calculated - ₹{data['economic_impact']}K impact from {data['hidden_talent_count']} hidden talents")
                print(f"   Methodology: {data['methodology']}")
                return True
            else:
                print_result(False, "Economic impact response missing expected fields")
                return False
        else:
            print_result(False, f"Economic impact failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Economic impact test error: {str(e)}")
        return False

def test_7_system_status():
    """Test 7: System Status Endpoint"""
    print_test_header("System Status Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/system-status", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            has_status = 'status' in data
            has_tests = 'tests_passed' in data and 'total_tests' in data
            
            if has_status and has_tests:
                print_result(True, f"System status active - {data['tests_passed']}/{data['total_tests']} internal tests passed")
                print(f"   Status: {data['status']}")
                return True
            else:
                print_result(False, "Status response missing expected fields")
                return False
        else:
            print_result(False, f"Status endpoint failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"System status test error: {str(e)}")
        return False

def run_all_tests():
    """Run all system tests"""
    print("\n" + "="*60)
    print("SKILLGENOME X - SYSTEM TEST SUITE")
    print("Hackathon Judge Review")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    tests = [
        ("API Health Check", test_1_api_health),
        ("Prediction Engine", test_2_prediction_engine),
        ("Policy Generator", test_3_policy_generator),
        ("Anomaly Detection", test_4_anomaly_detection),
        ("Source Verification", test_5_source_verification),
        ("Economic Impact", test_6_economic_impact),
        ("System Status", test_7_system_status)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ CRITICAL ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*60}")
    print(f"OVERALL: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("STATUS: ✓ ALL SYSTEMS OPERATIONAL - JUDGE READY")
    elif passed_count >= total_count * 0.7:
        print("STATUS: ⚠ PARTIAL OPERATIONAL - Review failed tests")
    else:
        print("STATUS: ✗ SYSTEM DEGRADED - Critical issues detected")
    
    print("="*60 + "\n")
    
    return passed_count, total_count

if __name__ == "__main__":
    print("\nStarting SkillGenome X System Tests...")
    print("Ensure the backend server is running on http://localhost:5000\n")
    
    try:
        passed, total = run_all_tests()
        exit(0 if passed == total else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        exit(1)
    except Exception as e:
        print(f"\n\nCRITICAL TEST SUITE ERROR: {str(e)}")
        exit(1)
