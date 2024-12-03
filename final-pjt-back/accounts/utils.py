import random
from django.contrib.auth import get_user_model


def generate_nickname():
    financial_terms = [
        "존버하는", "적금붓는", "파이어족", "투자하는", "주식사는",
        "부자가 될", "저축하는", "이자받는", "자산쌓는", "떡상한"
    ]
    animals = [
        "북극곰", "북극여우", "루돌프", "산타클로스", "순록", "교수님",
        "흰올빼미", "독도새우", "황제펭귄", "남극개미", "북극개미",
    ]
    term = random.choice(financial_terms)
    animal = random.choice(animals)
    number = random.randint(1000, 9999)
    
    return f"{term} {animal} {number}"


