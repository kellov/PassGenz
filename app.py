from flask import Flask, render_template, request, jsonify
from generator import PasswordGenerator

app = Flask(__name__)

@app.route('/')
def index():
    categories = list(PasswordGenerator.PATTERNS.keys())
    return render_template('index.html', categories=categories)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    category = data.get('category')
    
    try:
        if category and category in PasswordGenerator.PATTERNS:
            password = PasswordGenerator.generate_by_category(category)
        else:
            # Кастомные параметры
            password = PasswordGenerator.generate(
                length=int(data.get('length', 16)),
                use_digits=data.get('digits', True),
                use_symbols=data.get('symbols', True),
                use_uppercase=data.get('uppercase', True),
                use_lowercase=data.get('lowercase', True),
                exclude_ambiguous=data.get('exclude_ambiguous', False),
                use_words=data.get('use_words', False)
            )
        
        score = PasswordGenerator.check_strength(password)
        label, color = PasswordGenerator.get_strength_label(score)
        
        return jsonify({
            'password': password,
            'strength': label,
            'strength_color': color,
            'strength_score': score,
            'length': len(password)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)