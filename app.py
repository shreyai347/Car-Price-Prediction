from flask import Flask, render_template, request
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and the cleaned car data
model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
car = pd.read_csv('Cleaned_Car_data.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get unique values for dropdowns
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel_types = car['fuel_type'].unique()

    # Insert a placeholder option in the companies dropdown
    companies.insert(0, 'Select Company')
    return render_template('index.html', companies=companies, car_models=car_models, years=years, fuel_types=fuel_types)

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    # Get the form data
    company = request.form.get('company')
    car_model = request.form.get('car_models')
    year = request.form.get('year')
    fuel_type = request.form.get('fuel_type')
    driven = request.form.get('kilo_driven')

    # Create a DataFrame for prediction
    prediction_data = pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                                   data=np.array([car_model, company, year, driven, fuel_type]).reshape(1, 5))
    
    # Make prediction
    prediction = model.predict(prediction_data)
    predicted_price = np.round(prediction[0], 2)

    # Render prediction page with details
    return render_template('prediction.html', 
                           predicted_price=predicted_price,
                           company=company,
                           car_model=car_model,
                           year=year,
                           fuel_type=fuel_type,
                           kilo_driven=driven)

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development
