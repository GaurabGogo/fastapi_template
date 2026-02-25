import httpx
import sys

BASE_URL = "http://localhost:8000/api"

def test_session_lifecycle():
    with httpx.Client(base_url=BASE_URL) as client:
        # 1. Start Session
        print("Starting session...")
        response = client.post("/sessions/start")
        if response.status_code != 201:
            print(f"Failed to start session: {response.text}")
            sys.exit(1)
        
        session_id = response.json()["data"]["id"]
        print(f"Session started: {session_id}")

        # 2. Add Valid Location
        print("Adding valid location...")
        response = client.post(f"/sessions/{session_id}/location", json={"latitude": 45.0, "longitude": 90.0})
        if response.status_code != 201:
            print(f"Failed to add location: {response.text}")
            sys.exit(1)
        print("Location added successfully")

        # 3. Add Invalid Location (Latitude out of range)
        print("Adding invalid location (Expecting 422)...")
        response = client.post(f"/sessions/{session_id}/location", json={"latitude": 100.0, "longitude": 90.0})
        if response.status_code == 422:
            print("Successfully rejected invalid latitude")
        else:
            print(f"Expected 422 for invalid latitude, got {response.status_code}")
            sys.exit(1)

        # 4. Get Session Details
        print("Getting session details...")
        response = client.get(f"/sessions/{session_id}")
        data = response.json()["data"]
        if len(data["locations"]) != 1:
            print(f"Expected 1 location, found {len(data['locations'])}")
            sys.exit(1)
        print("Session details verified")

        # 5. End Session
        print("Ending session...")
        response = client.post(f"/sessions/{session_id}/end")
        if response.status_code != 200:
            print(f"Failed to end session: {response.text}")
            sys.exit(1)
        print("Session ended")

        # 6. Add Location to Ended Session (Expecting 400)
        print("Adding location to ended session (Expecting 400)...")
        response = client.post(f"/sessions/{session_id}/location", json={"latitude": 10.0, "longitude": 10.0})
        if response.status_code == 400:
            print("Successfully rejected location for ended session")
        else:
            print(f"Expected 400 for ended session, got {response.status_code}")
            sys.exit(1)

        print("\nAll tests passed successfully! ✅")

if __name__ == "__main__":
    test_session_lifecycle()
