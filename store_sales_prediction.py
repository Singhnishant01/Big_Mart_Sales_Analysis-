# -*- coding: utf-8 -*-
"""Store_Sales_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gJDx-I5koLRYmmydI4ZUjKD0qJ16FuCg
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor # Changed sGBRegressor to XGBRegressor
from sklearn import metrics

"""Data collection and analysis"""

# loading the dataset from csv file to a pandas dataframe
big_mart_data = pd.read_csv('Train.csv')

# first 5 rows of the dataframe
big_mart_data.head()

# Number of data points & number of features
big_mart_data.shape

# Getting some information about the dataset
big_mart_data.info()

"""Categorical features:
  - item_identifier
  - item_fat_content
  - item_type
  - outlet_identifier
  - outlet_size
  - outlet_location_type
  - outlet_type

"""

# Checkinf for missing values
big_mart_data.isnull().sum()

"""Handlin Missing value

-Mean --> average value- It is used for the missing value in the numerical column
-Mode --> Most repeated value- It is used for the missing value in the categorical column
"""

# Mean value of the "Item_weight" column
big_mart_data['Item_Weight'].mean()

# Filling the missing values in "Item_weight" column with "mean" value
big_mart_data['Item_Weight'].fillna(big_mart_data['Item_Weight'].mean(), inplace=True)

# Checking for missing column
big_mart_data.isnull().sum()

"""Replacing the missing values in "Outlet_size" with mode"""

# Replacing the missing values in "Outlet_size" with mode
mode_of_outlet_size = big_mart_data.pivot_table(values='Outlet_Size', columns='Outlet_Type', aggfunc=(lambda x: x.mode()[0])) # Changed 'Outlet_size' to 'Outlet_Size'

print(mode_of_outlet_size)

missing_values = big_mart_data['Outlet_Size'].isnull()
print(missing_values)

big_mart_data.loc[missing_values, 'Outlet_Size'] = big_mart_data.loc[missing_values,'Outlet_Type'].apply(lambda x: mode_of_outlet_size[x])

# Checking for missing values
big_mart_data.isnull().sum()

# Statistical measures about the data
big_mart_data.describe()

"""Numerical Features"""

sns.set()

# Item_Weight distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Weight'])
plt.show()

# Item_Visibility distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Visibility'])
plt.show()

# Item_MRP distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_MRP'])
plt.show()

# Item_Outlet_Sales distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Outlet_Sales'])
plt.show()

# Outlet_Establishment_Year
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Establishment_Year', data=big_mart_data)
plt.show()

# Item_Fat_Content column
plt.figure(figsize=(6,6))
sns.countplot(x='Item_Fat_Content', data=big_mart_data)
plt.show()

# Item_Type column
plt.figure(figsize=(30,6))
sns.countplot(x='Item_Type', data=big_mart_data)
plt.show()

# Outlet_Size column
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Size', data=big_mart_data)
plt.show()

"""Date Pre_processing"""

big_mart_data.head()

big_mart_data['Item_Fat_Content'].value_counts()

big_mart_data.replace({'Item_Fat_Content': {'low fat':'Low Fat','LF':'Low Fat', 'reg':'Regular'}}, inplace=True)



big_mart_data['Item_Fat_Content'].value_counts()

"""Label Encoding"""

encoder = LabelEncoder()

big_mart_data['Item_Identifier'] = encoder.fit_transform(big_mart_data['Item_Identifier'])

big_mart_data['Item_Fat_Content'] = encoder.fit_transform(big_mart_data['Item_Fat_Content'])
big_mart_data['Item_Type'] = encoder.fit_transform(big_mart_data['Item_Type'])
big_mart_data['Outlet_Identifier'] = encoder.fit_transform(big_mart_data['Outlet_Identifier'])
big_mart_data['Outlet_Size'] = encoder.fit_transform(big_mart_data['Outlet_Size'])
big_mart_data['Outlet_Location_Type'] = encoder.fit_transform(big_mart_data['Outlet_Location_Type'])
big_mart_data['Outlet_Type'] = encoder.fit_transform(big_mart_data['Outlet_Type'])

"""ADD derived Features"""

# 1. Years since outlet established
df_encoded = big_mart_data.copy() # Create a copy of big_mart_data
df_encoded['Outlet_Years'] = 2025 - df_encoded['Outlet_Establishment_Year'] # Use df_encoded instead of df

# 2. Item Category from Item Identifier (first two letters)
df_encoded['Item_Category'] = df_encoded['Item_Identifier'].apply(lambda x: str(x)[:2]) # Convert to string before slicing
df_encoded['Item_Category'] = df_encoded['Item_Category'].replace({
    'FD': 'Food',
    'NC': 'Non-Consumable',
    'DR': 'Drinks'
})

# One-hot encode Item_Category
df_encoded = pd.get_dummies(df_encoded, columns=['Item_Category'])

df_encoded.drop(['Item_Identifier', 'Outlet_Establishment_Year'], axis=1, inplace=True)

print("Shape after feature engineering:", df_encoded.shape)
df_encoded.head()



"""Splitting features and Target"""

x = big_mart_data.drop(columns='Item_Outlet_Sales', axis=1)
y = big_mart_data['Item_Outlet_Sales']

print(x)

print(y)

"""Splitting the data into training and testing data"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

print(x.shape, x_train.shape, x_test.shape)

"""Machine Learning model training

XGBoost Regressor
"""

regressor = XGBRegressor()

regressor.fit(x_train, y_train)

#prediction on training data

regressor.fit(x_train, y_train) # This line is added to fix the error

training_data_prediction = regressor.predict(x_train)

# R squared value
r2_train = metrics.r2_score(y_train, training_data_prediction)

print('R Squared value = ', r2_train)

#prediction on test data
test_data_prediction = regressor.predict(x_test)

# r squared value
metrics.r2_score(y_test, test_data_prediction)

"""Time-Based Cross-Validation (backtesting)
This simulates the idea: "train on past, test on future."
"""

from sklearn.model_selection import TimeSeriesSplit

# ... (Your existing code) ...

# Assuming 'big_mart_data' is your DataFrame and 'Date' is a datetime column
big_mart_data = big_mart_data.sort_values('Outlet_Establishment_Year')  # Sort by time

# Time-Based Cross-Validation
tscv = TimeSeriesSplit(n_splits=5) # Adjust n_splits as needed

results = []
for train_index, test_index in tscv.split(x):
    x_train, x_test = x.iloc[train_index], x.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    regressor.fit(x_train, y_train)
    predictions = regressor.predict(x_test)

    results.extend(list(zip(y_test.values, predictions)))  # Store actual and predicted

# Create results DataFrame
results_df = pd.DataFrame(results, columns=['Actual Sales', 'Predicted Sales'])


# ... (Your plotting code) ...

# Import necessary functions from sklearn.metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error

# calculate Evaluation metrics (RMSE, MAE, MAPE)
# MAE
mae = mean_absolute_error(results_df['Actual Sales'], results_df['Predicted Sales'])
print("MAE:", mae)

# RMSE
rmse = np.sqrt(mean_squared_error(results_df['Actual Sales'], results_df['Predicted Sales']))
print("RMSE:", rmse)

# MAPE
mape = np.mean(np.abs((results_df['Actual Sales'] - results_df['Predicted Sales']) / results_df['Actual Sales'])) * 100
print("MAPE:", mape)

# Line plot:-  actual vs predicted
plt.figure(figsize=(14, 6))
plt.plot(results_df['Actual Sales'].values[:100], label='Actual Sales', marker='o')
plt.plot(results_df['Predicted Sales'].values[:100], label='Predicted Sales', marker='x')
plt.title('Actual vs Predicted Sales (First 100 Records)')
plt.xlabel('Index')
plt.ylabel('Sales')
plt.legend()
plt.tight_layout()
plt.show()

#Scatter plot:- actual vs predicted
plt.figure(figsize=(8, 6))
sns.scatterplot(x=results_df['Actual Sales'], y=results_df['Predicted Sales'], alpha=0.6)
plt.plot([results_df['Actual Sales'].min(), results_df['Actual Sales'].max()],
         [results_df['Actual Sales'].min(), results_df['Actual Sales'].max()],
         color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Sales')
plt.ylabel('Predicted Sales')
plt.title('Actual vs Predicted Sales (Scatter Plot)')
plt.tight_layout()
plt.show()

# Baseline model performance
# Baseline model: predict mean of training sales
mean_sales = y_train.mean()

# Predicting mean for the test set
baseline_predictions = [mean_sales] * len(y_test)

# Evaluation
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# Metrics for baseline
baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_predictions))
baseline_mae = mean_absolute_error(y_test, baseline_predictions)
baseline_mape = np.mean(np.abs((y_test - baseline_predictions) / y_test)) * 100
baseline_r2 = r2_score(y_test, baseline_predictions)

# Display results
print("🔹 Baseline Model Performance:")
print("R² Score:", baseline_r2)
print("RMSE:", baseline_rmse)
print("MAE:", baseline_mae)
print("MAPE:", baseline_mape)

errors = results_df['Actual Sales'] - results_df['Predicted Sales']
plt.figure(figsize=(10, 5))
sns.histplot(errors, bins=30, kde=True, color='purple')
plt.title('Distribution of Prediction Errors')
plt.xlabel('Error (Actual - Predicted)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

import pandas as pd
from google.cloud import storage, bigquery
import requests
from datetime import datetime

# Step 1: Ingest Sales Data (could be a CSV, database, or API call)
def fetch_sales_data():
    # Example: Fetching sales data from an API or file
    sales_url = "https://api.example.com/daily_sales"
    sales_data = requests.get(sales_url).json()
    sales_df = pd.DataFrame(sales_data)
    return sales_df

# Step 2: Ingest External Data (e.g., weather, promotions)
def fetch_external_data():
    # Example: Fetching weather data or promotional events
    weather_url = "https://api.example.com/weather"
    weather_data = requests.get(weather_url).json()
    weather_df = pd.DataFrame(weather_data)
    return weather_df

# Step 3: Process Data (merge sales and external data, handle missing values, etc.)
def process_data(sales_df, weather_df):
    # Merge the sales and external data on a common column like date
    df = pd.merge(sales_df, weather_df, on="date", how="left")

    # Handle missing values or data transformations
    df['sales'] = df['sales'].fillna(0)
    df['temperature'] = df['temperature'].fillna(df['temperature'].mean())  # Example for weather data

    # Return processed dataframe
    return df

# Step 4: Store Data in Cloud (e.g., Google Cloud Storage, BigQuery)
def store_data_in_gcs(df):
    # Convert DataFrame to CSV for storage
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"daily_sales_{today}.csv"
    csv_buffer = df.to_csv(index=False)

    # Google Cloud Storage bucket
    client = storage.Client()
    bucket = client.bucket('your-bucket-name')
    blob = bucket.blob(f"sales_data/{filename}")

    # Upload CSV to Cloud Storage
    blob.upload_from_string(csv_buffer, content_type="text/csv")
    print(f"Uploaded {filename} to Google Cloud Storage.")

def store_data_in_bigquery(df):
    # Google BigQuery setup
    client = bigquery.Client()
    dataset_ref = client.dataset('your_dataset')
    table_ref = dataset_ref.table('daily_sales')

    # Load data into BigQuery
    job = client.load_table_from_dataframe(df, table_ref)
    job.result()  # Wait for the job to complete
    print(f"Data loaded into BigQuery: {table_ref.path}")

# Step 5: Automate with Cloud Functions or Scheduled Jobs (e.g., cron job, cloud scheduler)
def daily_pipeline(event, context):
    sales_data = fetch_sales_data()
    external_data = fetch_external_data()
    processed_data = process_data(sales_data, external_data)

    # Store processed data in cloud storage and BigQuery
    store_data_in_gcs(processed_data)
    store_data_in_bigquery(processed_data)

    return "Pipeline execution completed successfully"

# If you're deploying this as a Google Cloud Function, you would trigger this function daily via Cloud Scheduler

!pip install flask ngrok

import xgboost as xgb
import numpy as np
import pandas as pd
import joblib

# Example: Train a simple XGBoost model
X = np.random.rand(100, 5)  # Random data for illustration
y = np.random.rand(100)  # Random target variable
model = xgb.XGBRegressor(objective='reg:squarederror')
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'model.pkl')

!pip install gradio

import gradio as gr

def predict_sales(store_id, day_of_week, promo):
    # Dummy function for demo
    return f"Predicted sales for store {store_id} on day {day_of_week} (Promo: {promo}): 1234 units"

demo = gr.Interface(
    fn=predict_sales,
    inputs=[
        gr.Number(label="Store ID"),
        gr.Number(label="Day of Week"),
        gr.Checkbox(label="Promo Active?")
    ],
    outputs="text"
)

demo.launch()

from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('model.pkl')

app = Flask(__name__)

@app.route('/forecast', methods=['POST'])
def forecast():
    try:
        # Get the input data from the request
        input_data = request.get_json()

        # Convert the input data to a pandas DataFrame
        data = pd.DataFrame(input_data)

        # Preprocess the input if necessary (e.g., feature selection, scaling, etc.)
        features = data[['feature1', 'feature2', 'feature3', 'feature4', 'feature5']]  # Modify based on model features

        # Make predictions
        predictions = model.predict(features)

        # Return the predictions as a JSON response
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

from flask import Flask, request, jsonify
from pyngrok import ngrok # pyngrok module is now available

# Open a port for ngrok
public_url = ngrok.connect(5000)
print('Public URL:', public_url)

# Start the Flask app
!flask run --host=0.0.0.0 --port=5000

import requests

# Replace the ngrok URL with the one printed above
url = 'http://<ngrok_subdomain>.ngrok.io/forecast'

# Example input data
data = {
    "feature1": [0.1, 0.2],
    "feature2": [0.3, 0.4],
    "feature3": [0.5, 0.6],
    "feature4": [0.7, 0.8],
    "feature5": [0.9, 1.0]
}

# Send the POST request
response = requests.post(url, json=data)

if response.status_code == 200:
    print("Predictions:", response.json())
else:
    print("Error:", response.status_code, response.text)