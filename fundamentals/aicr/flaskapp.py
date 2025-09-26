from flask import Flask, render_template, request
import pandas as pd
import requests
import base64
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file_data = request.form.get('file')
        # Decode the Base64 encoded CSV file content
        decoded_file = base64.b64decode(file_data.split(',')[1])
        # Read CSV content into a DataFrame
        df = pd.read_csv(io.StringIO(decoded_file.decode('utf-8')))

        # Separate the 'claim_id' column if it exists
        if 'claim_id' in df.columns:
            claim_ids = df['claim_id']
            df = df.drop(columns=['claim_id'])
        else:
            claim_ids = None

        # Prepare the DataFrame for the BentoML service by converting it to a
        # JSON object with 'columns' and 'data' keys, which is the expected format.
        data_payload = {
            "columns": df.columns.tolist(),
            "data": df.values.tolist()
        }

        # Send the correctly formatted payload to the BentoML service
        response = requests.post(
            'http://127.0.0.1:3000/predict',  # BentoML endpoint
            json=data_payload
        )

        # Check for a successful response from the BentoML service
        response.raise_for_status()

        # Retrieve predictions from the response
        predictions = response.json()['predictions']
        df['Prediction'] = predictions

        # Reattach the 'claim_id' column if it was present
        if claim_ids is not None:
            df['claim_id'] = claim_ids

        # Reorder columns to have 'claim_id' first
        if 'claim_id' in df.columns:
            df = df[['claim_id'] + [col for col in df.columns if col != 'claim_id']]
            
        # Render the results in the results.html template
        return render_template('result.html', tables=[df.to_html(classes='data')])

    except requests.exceptions.RequestException as e:
        # Handle connection errors or bad responses from BentoML
        return f"Error connecting to BentoML service: {e}", 500
    except KeyError:
        # Handle cases where the BentoML response is not in the expected format
        return f"Invalid response from BentoML service. Response: {response.text}", 500
    except Exception as e:
        # Catch any other unexpected errors
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(port=5005, debug=True)
