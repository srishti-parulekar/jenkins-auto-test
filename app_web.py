from flask import Flask, render_template, request, jsonify
from app import SmartCalc

app = Flask(__name__)
calc = SmartCalc()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    operation = data['operation']
    a = float(data['a'])
    b = float(data.get('b', 0))
    
    try:
        if operation == 'add':
            result = calc.add(a, b)
        elif operation == 'subtract':
            result = calc.subtract(a, b)
        elif operation == 'multiply':
            result = calc.multiply(a, b)
        elif operation == 'divide':
            result = calc.divide(a, b)
        elif operation == 'power':
            result = calc.power(a, b)
        elif operation == 'sqrt':
            result = calc.sqrt(a)
        else:
            return jsonify({'error': 'Invalid operation'}), 400
            
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)