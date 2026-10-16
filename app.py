import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the model from naive.pkl
with open('naive.pkl', 'rb') as f:
  model = pickle.load(f)

# HTML template with embedded modern CSS layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insurance Cost Prediction</title>
    <style>
        :root {
            --primary-color: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-color: #1f2937;
            --border-color: #d1d5db;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: var(--card-bg);
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            width: 100%;
            max-width: 500px;
        }
        h2 {
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 25px;
        }
        .form-group {
            margin-bottom: 16px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 14px;
        }
        input, select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 14px;
            box-sizing: border-box;
            transition: border-color 0.2s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        button {
            width: 100%;
            background-color: var(--primary-color);
            color: white;
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 10px;
        }
        button:hover {
            background-color: var(--primary-hover);
        }
        .result {
            margin-top: 25px;
            padding: 15px;
            background-color: #e0e7ff;
            border-left: 4px solid var(--primary-color);
            border-radius: 6px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #312e81;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Insurance Prediction Portal</h2>
        <form method="POST">
            <div class="form-group">
                <label for="age">Age:</label>
                <input type="number" id="age" name="age" required min="0" max="120" placeholder="e.g., 30">
            </div>
            
            <div class="form-group">
                <label for="sex">Sex:</label>
                <select id="sex" name="sex" required>
                    <option value="1">Male</option>
                    <option value="0">Female</option>
                </select>
            </div>

            <div class="form-group">
                <label for="bmi">BMI:</label>
                <input type="number" step="0.1" id="bmi" name="bmi" required placeholder="e.g., 25.4">
            </div>

            <div class="form-group">
                <label for="children">Children:</label>
                <input type="number" id="children" name="children" required min="0" max="10" placeholder="e.g., 1">
            </div>

            <div class="form-group">
                <label for="smoker">Smoker:</label>
                <select id="smoker" name="smoker" required>
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                </select>
            </div>

            <div class="form-group">
                <label for="region">Region:</label>
                <select id="region" name="region" required>
                    <option value="0">Northeast</option>
                    <option value="1">Northwest</option>
                    <option value="2">Southeast</option>
                    <option value="3">Southwest</option>
                </select>
            </div>

            <button type="submit">Predict Cost</button>
        </form>

        {% if prediction_text %}
            <div class="result">
                {{ prediction_text }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def home():
  prediction_text = ''
  if request.method == 'POST':
    try:
      # Extract inputs mapped to features: age, sex, bmi, children, smoker, region[cite: 1]
      age = float(request.form['age'])
      sex = float(request.form['sex'])
      bmi = float(request.form['bmi'])
      children = float(request.form['children'])
      smoker = float(request.form['smoker'])
      region = float(request.form['region'])

      features = np.array([[age, sex, bmi, children, smoker, region]])
      prediction = model.predict(features)[0]
      prediction_text = f'Estimated Insurance Cost: ${prediction:,.2f}'
    except Exception as e:
      prediction_text = f'Error in prediction: {str(e)}'

  return render_template_string(
      HTML_TEMPLATE, prediction_text=prediction_text
  )


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
