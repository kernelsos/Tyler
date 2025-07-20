from flask import Flask, request , jsonify
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return "Currency Converter Flask App is running."
    elif request.method == 'POST':
        data = request.get_json()
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        cf = fetch_conversion_factor(source_currency, target_currency)
        final_amount = round(amount * cf)

        response = {
            'fulfillmentText': f"{amount} {source_currency} is {final_amount} {target_currency}"
        }
        return jsonify(response)


def fetch_conversion_factor(source, target):
    url = "https://api.freecurrencyapi.com/v1/latest?apikey=[]"
    response = requests.get(url)
    data = response.json()
    print(data) 
    rates = data['data']
    if source == "USD":
        cf = rates[target]
    elif target == "USD":
        cf = 1 / rates[source]
    else:
        cf = rates[target] / rates[source]
    
    return cf


if __name__ == "__main__":
    app.run(debug=True)
