import requests
import json

BASE_URL = "http://localhost:5001"

print("🧪 DSS Matching Engine Test\n")

print("1. Testing /match/api endpoint...")

test_payload = {
    "student_id": "STU_00000"
}

try:
    response = requests.post(f"{BASE_URL}/match/api", json=test_payload)

    if response.status_code == 200:
        data = response.json()

        print(f"\n✅ Match API Response:")
        print(f"   Student ID: {data.get('student_id')}")
        print(f"   Processing Time: {data.get('processing_time_ms')} ms")
        print(f"\n📊 Summary:")
        summary = data.get('summary', {})
        print(f"   Total Scholarships: {summary.get('total_scholarships_analyzed')}")
        print(f"   Matched: {summary.get('matched_count')}")
        print(f"   Rejected: {summary.get('rejected_count')}")
        print(f"   Match Rate: {summary.get('match_rate_percent')}%")
        print(f"   Avg Score: {summary.get('average_match_score')}")
        print(f"   Top Score: {summary.get('top_match_score')}")

        print(f"\n🎯 Top 3 Matches:")
        matched = data.get('matched', [])
        for i, match in enumerate(matched[:3], 1):
            print(f"\n   {i}. {match['scholarship_name']}")
            print(f"      Provider: {match['provider']}")
            print(f"      Amount: €{match['amount']}")
            print(f"      Score: {match['score']:.3f}")
            print(f"      Recommendation: {match['recommendation']}")

            print(f"\n      Met Criteria:")
            for criteria in match['reasons']['met_criteria'][:3]:
                print(f"        {criteria}")

        print(f"\n❌ Sample Rejection:")
        rejected = data.get('rejected', [])
        if rejected:
            reject = rejected[0]
            print(f"   {reject['scholarship_name']}")
            print(f"   Failed Criteria:")
            for criteria in reject['reasons']['failed_criteria']:
                print(f"     {criteria}")

    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to Flask app. Make sure it's running:")
    print("   python run.py")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("Test complete!")
