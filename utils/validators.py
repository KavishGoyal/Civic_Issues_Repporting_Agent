from typing import Optional
import re

def validate_location(location: str) -> bool:
    """Validate location string"""
    if not location or len(location) < 5:
        return False
    return True

def validate_coordinates(lat: Optional[float], lon: Optional[float]) -> bool:
    """Validate GPS coordinates"""
    if lat is None or lon is None:
        return True  # Optional
    
    if not (-90 <= lat <= 90):
        return False
    if not (-180 <= lon <= 180):
        return False
    
    return True

def validate_phone(phone: str) -> bool:
    """Validate phone number"""
    pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    return bool(re.match(pattern, phone))

def validate_email(email: str) -> bool:
    """Validate email address"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))