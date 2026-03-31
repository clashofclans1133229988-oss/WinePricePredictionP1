# =====================================================================
# 🔹 FLASK APPLICATION FOR WINE PRICE PREDICTION MODEL
# =====================================================================
# This Flask app loads a trained Machine Learning model (stored as a pickle file)
# and creates a web API that can receive data and return price predictions
# =====================================================================

# Import required libraries - STEP 1: IMPORT ALL NECESSARY MODULES
# =====================================================================

# Flask: Main web framework to create the backend server
# - Flask('__name__') creates a new Flask application instance
# - Think of it as creating a new Express server in Node.js
from flask import Flask, render_template, request, jsonify

# jsonify: Converts Python dictionaries to JSON format
# - JSON is the standard format for sending data over the internet
# Why do we need jsonify?
# When Postman sends us data, it's in JSON format (like {"price": 5.5})
# When we send back responses, we need to convert them to JSON too

# render_template: Loads HTML files from a 'templates' folder
# - It finds .html files and sends them to the browser
# - Example: render_template('home.html') loads templates/home.html

# request: Gives us access to incoming data from Postman or the browser
# - request.json gets data sent in JSON format
# - request.method tells us if it's GET, POST, PUT, DELETE, etc.

# pickle: Used to load the trained ML model we saved earlier
# - pickle stores Python objects (like our trained RandomForest model) as binary files
import pickle
import numpy as np
import pandas as pd

# =====================================================================
# STEP 2: CREATE FLASK APPLICATION INSTANCE
# =====================================================================

# Create a Flask application object
# '__name__' = current Python module name (helps Flask locate resources)
app = Flask(__name__)

# =====================================================================
# STEP 3: LOAD THE TRAINED MODEL FROM PICKLE FILE
# =====================================================================

# Open the pickle file in READ BINARY mode ('rb' = read binary)
# This file contains our trained RandomForest model saved earlier
with open('randomforest_model.pkl', 'rb') as model_file:
    # pickle.load() deserializes the binary file back into a Python object
    # Now we have our trained model ready to make predictions!
    trained_model = pickle.load(model_file)

# =====================================================================
# STEP 4: LOAD THE FEATURE NAMES (IMPORTANT!)
# =====================================================================

# Load the feature names that were saved during training
# Why is this important?
# The model was trained with features in a SPECIFIC ORDER
# We must send features to the model in the SAME ORDER
# Otherwise, the model will make wrong predictions!
# Example: If we trained with [Alcohol, pH, Acidity]
# and send [pH, Acidity, Alcohol], predictions will be wrong!

with open('rf_features.pkl', 'rb') as features_file:
    feature_names = pickle.load(features_file)

print(f"✅ Model loaded successfully!")
print(f"✅ Feature names loaded: {feature_names}")

# =====================================================================
# STEP 5: CREATE ROUTES (URLs THAT HANDLE REQUESTS)
# =====================================================================

# What is a Route?
# A route is a URL endpoint that performs a specific action
# Example: /predict is a route, /home is another route
# When a user visits that URL, Flask runs the function below it

# =====================================================================
# ROUTE 1: HOME PAGE (RENDERS HTML)
# =====================================================================

# @app.route('/') means: when someone visits http://localhost:5000/
# the function below will run
@app.route('/')
def home():
    """
    This function handles requests to the home page
    GET request: Browser asks for a page to display
    Response: We render home.html (the HTML file)
    """
    # render_template('home.html') does the following:
    # 1. Looks for a file called 'home.html' in the 'templates' folder
    # 2. Reads the HTML file
    # 3. Sends it to your browser to display
    return render_template('home.html')

# =====================================================================
# ROUTE 2: API ENDPOINT FOR PREDICTIONS (RECEIVES JSON DATA)
# =====================================================================

# @app.route('/predict_api', methods=['POST']) means:
# - When someone sends a POST request to http://localhost:5000/predict_api
# - The function below will run
# - methods=['POST'] = only accept POST requests (not GET, PUT, etc.)
#
# What is a POST request?
# POST sends data TO the server (unlike GET which requests data FROM server)
# When you use Postman to send data for predictions, you use POST
#
# Why POST and not GET?
# GET attaches data to the URL: http://site.com/?alcohol=12&ph=3.2&acid=0.5
# POST sends data in the request BODY (safer, can send more data)
# This is the professional, secure way to handle sensitive data

@app.route('/predict_api', methods=['POST'])
def predict_api():
    """
    This function handles prediction requests from Postman or frontend
    
    Process:
    1. Receive JSON data from Postman
    2. Validate the data
    3. Format data in the correct order for the model
    4. Use the model to make a prediction
    5. Send back the predicted price as JSON response
    """
    
    try:
        # Get the JSON data sent by Postman
        # request.json retrieves data that was sent as JSON
        # Example Postman sends: {"Alcohol_log": 2.5, "pH": 3.2, ...}
        data = request.json
        
        print(f"\n📨 Received data from Postman: {data}")
        
        # ===== DATA VALIDATION =====
        # Check if we received any data at all
        if not data:
            # If no data was sent, return an error message
            # jsonify converts Python dict to JSON response
            # status code 400 = Bad Request (client sent invalid data)
            return jsonify({
                "error": "❌ No data received. Please send JSON data."
            }), 400
        
        # ===== EXTRACT FEATURES IN CORRECT ORDER =====
        # This is CRITICAL! The model expects features in a specific order
        # We load feature_names which tells us the correct order
        
        # Create a list to hold feature values in the correct order
        features_list = []
        
        # Loop through each feature name in the correct order
        for feature in feature_names:
            # Check if this feature exists in the data we received
            if feature not in data:
                # If a required feature is missing, return an error
                return jsonify({
                    "error": f"❌ Missing feature: {feature}",
                    "required_features": feature_names
                }), 400
            
            # If the feature exists, add its value to our list
            features_list.append(data[feature])
        
        print(f"📋 Feature values in correct order: {features_list}")
        
        # ===== PREPARE DATA FOR MODEL =====
        # Convert the list to a NumPy array (the format our model expects)
        # reshape(1, -1) means:
        # - 1 = we have 1 sample (1 wine to predict for)
        # - -1 = "figure out the number of columns automatically"
        # The model was trained on (80, num_features) = 80 rows of data
        # For prediction, we need (1, num_features) = 1 row of data
        features_array = np.array(features_list).reshape(1, -1)
        
        print(f"🔢 Array shape before prediction: {features_array.shape}")
        
        # ===== MAKE PREDICTION =====
        # Use the trained model to predict the price
        # trained_model.predict() returns an array with 1 value (the predicted price)
        # We use [0] to extract just the number from the array
        predicted_price = trained_model.predict(features_array)[0]
        
        print(f"🎯 Predicted price: ${predicted_price:.2f}")
        
        # ===== PREPARE RESPONSE =====
        # Create a response dictionary with the prediction
        response = {
            "success": True,
            "message": "✅ Prediction successful!",
            "input_features": data,
            "predicted_price": float(predicted_price),
            "price_formatted": f"${predicted_price:.2f}"
        }
        
        # Return the response as JSON with status code 200 (OK)
        return jsonify(response), 200
    
    # ===== ERROR HANDLING =====
    # If anything goes wrong, catch the exception and return error details
    except Exception as error:
        print(f"\n❌ Error occurred: {str(error)}")
        
        # Return an error response with status code 500 (Internal Server Error)
        return jsonify({
            "success": False,
            "error": f"❌ Error processing request: {str(error)}"
        }), 500

# =====================================================================
# STEP 6: RUN THE FLASK SERVER
# =====================================================================

# This code only runs if you execute this file directly
# (not if you import it from another file)
if __name__ == '__main__':
    """
    Start the Flask development server
    
    Parameters explained:
    
    host='0.0.0.0' means:
    - The server listens on all network interfaces
    - You can access it from:
      - http://localhost:5000 (from your computer)
      - http://127.0.0.1:5000 (same as localhost)
      - http://<your-ip>:5000 (from other computers on the network)
    
    port=5000 means:
    - The server runs on port 5000
    - Think of ports like apartment numbers on a building
    - Each port can host one service
    - Common ports: 80 (HTTP), 443 (HTTPS), 3000, 8000, 5000
    
    debug=True means:
    - Show detailed error messages if something breaks
    - Auto-restart the server when you change code
    - This is ONLY for development!
    - In production, use debug=False for security
    """
    
    print("\n" + "="*70)
    print("🚀 FLASK SERVER STARTING...")
    print("="*70)
    print("📍 Server running at: http://localhost:5000")
    print("🏠 Visit home page at: http://localhost:5000/")
    print("🔮 Send predictions to: http://localhost:5000/predict_api")
    print("⚠️  Use POST method in Postman to send JSON data")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)