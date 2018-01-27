from random import choice

vehicles = [
    ('نیسان زامیاد', 2800),
    ('خاور', 4000),
    ('کامیون ۶ چرخ', 10000),
    ('کامیون ۱۰ چرخ', 15000),
    ('تریلی', 22000)
]

def get_vehicle(license_plate):
    return choice(vehicles)
