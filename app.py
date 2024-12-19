from flask import Flask, render_template, request, flash, jsonify
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'house_price_predictor_2024'

# Price factors database (in a real app, this would be in a database)
LOCATION_MULTIPLIERS = {
    'mumbai': 3.0,
    'delhi': 2.8,
    'bangalore': 2.5,
    'hyderabad': 2.2,
    'pune': 2.0,
    'chennai': 2.1,
    'kolkata': 1.9,
    'ahmedabad': 1.8,
    'noida': 2.0,
    'gurgaon': 2.3,
    'dwarka': 3.1,
    'default': 1.5
}

AMENITIES_IMPACT = {
    'pool': 1.1,
    'garage': 1.08,
    'garden': 1.05,
    'security': 1.03,
    'smart_home': 1.04
}

@app.route('/')
def index():
    return render_template('index.html', 
                         locations=sorted(LOCATION_MULTIPLIERS.keys()),
                         amenities=AMENITIES_IMPACT.keys())

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        location = request.form['location'].lower()
        square_footage = float(request.form['square_footage'])
        bedrooms = int(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])
        year_built = int(request.form['year_built'])
        amenities = request.form.getlist('amenities')

        # Calculate base price
        base_price = calculate_price(
            location, square_footage, bedrooms, 
            bathrooms, year_built, amenities
        )

        # Generate market insights
        insights = {
            'market_trend': np.random.choice([
                'Rising market - good time to invest',
                'Stable market conditions',
                'High demand in this area',
                'Competitive market pricing'
            ]),
            'similar_properties': [
                format_indian_currency(base_price * factor)
                for factor in np.random.normal(1, 0.1, 3)
            ],
            'price_confidence': f"{np.random.randint(85, 99)}%"
        }
        
        return render_template('result.html',
                             predicted_price=format_indian_currency(base_price),
                             location=location.title(),
                             square_footage="{:,}".format(int(square_footage)),
                             price_per_sqft=f"₹{base_price/square_footage:,.2f}/sq.ft",
                             bedrooms=bedrooms,
                             bathrooms=bathrooms,
                             year_built=year_built,
                             amenities=amenities,
                             insights=insights)

    except ValueError as e:
        flash('Please check your input values', 'error')
        return render_template('index.html')
    except Exception as e:
        flash('An unexpected error occurred', 'error')
        return render_template('index.html')

def calculate_price(location, sqft, beds, baths, year, amenities):
    """Calculate house price based on various factors"""
    # Base calculation (₹4000 per sq ft as base price)
    location_multiplier = LOCATION_MULTIPLIERS.get(location, LOCATION_MULTIPLIERS['default'])
    base_price = sqft * 4000 * location_multiplier
    
    # Age impact
    age_factor = max(0.7, 1 - (datetime.now().year - year) * 0.01)
    
    # Rooms impact
    rooms_factor = 1 + (beds * 0.05) + (baths * 0.05)
    
    # Amenities impact
    amenities_factor = 1.0
    for amenity in amenities:
        amenities_factor *= AMENITIES_IMPACT.get(amenity, 1.0)

    return base_price * age_factor * rooms_factor * amenities_factor

def format_indian_currency(amount):
    """Format amount in Indian currency style (with lakhs and crores)"""
    if amount >= 10000000:  # 1 crore or more
        crores = amount / 10000000
        return f"₹{crores:.2f} Crore"
    elif amount >= 100000:  # 1 lakh or more
        lakhs = amount / 100000
        return f"₹{lakhs:.2f} Lakh"
    else:
        return f"₹{amount:,.2f}"

def generate_market_insights(price, location):
    """Generate market analysis insights"""
    return {
        'market_trend': np.random.choice([
            'Rising market - good time to invest',
            'Stable market conditions',
            'High demand in this area',
            'Competitive market pricing'
        ]),
        'similar_properties': [
            format_indian_currency(price * factor)
            for factor in np.random.normal(1, 0.1, 3)
        ],
        'price_confidence': f"{np.random.randint(85, 99)}%"
    }

if __name__ == '__main__':
    print("🏠 House Price Predictor starting...")
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True) 