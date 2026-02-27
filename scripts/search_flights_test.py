import json

from tools.search_flights import search_flights

if __name__ == "__main__":

    flights = search_flights(
        {
            "origin": "ORD",
            "destination": "DFW",
            "dateDepart": "2025-09-20",
            "dateReturn": "2025-09-22",
        }
    )
    print(json.dumps(flights, indent=2))