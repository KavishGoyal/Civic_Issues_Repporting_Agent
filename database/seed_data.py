from models import Agency, SessionLocal, init_db

def seed_agencies():
    db = SessionLocal()
    
    agencies = [
        {
            "name": "Municipal Water Department",
            "department": "Water Management",
            "email": "water@municipality.gov",
            "phone": "+91-141-2345678",
            "issue_types": ["water_leak", "water_wastage", "broken_pipe"]
        },
        {
            "name": "Waste Management Corporation",
            "department": "Sanitation",
            "email": "waste@municipality.gov",
            "phone": "+91-141-2345679",
            "issue_types": ["garbage", "unpicked_garbage", "littering"]
        },
        {
            "name": "Public Works Department",
            "department": "Infrastructure",
            "email": "pwd@municipality.gov",
            "phone": "+91-141-2345680",
            "issue_types": ["pothole", "road_damage", "dirt_on_road"]
        },
        {
            "name": "Police Department",
            "department": "Law Enforcement",
            "email": "police@municipality.gov",
            "phone": "100",
            "issue_types": ["criminal_activity", "violence", "suspicious_activity"]
        }
    ]
    
    for agency_data in agencies:
        existing = db.query(Agency).filter(Agency.name == agency_data["name"]).first()
        if not existing:
            agency = Agency(**agency_data)
            db.add(agency)
    
    db.commit()
    db.close()
    print("Agencies seeded successfully!")

if __name__ == "__main__":
    init_db()
    seed_agencies()