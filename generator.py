import secrets
import string
import re

class PasswordGenerator:
    """Генератор паролей с категориями"""
    
    PATTERNS = {
        'стандартный': {
            'length': 16,
            'digits': True,
            'symbols': True,
            'uppercase': True,
            'lowercase': True
        },
        'супер-безопасный': {
            'length': 24,
            'digits': True,
            'symbols': True,
            'uppercase': True,
            'lowercase': True,
            'exclude_ambiguous': True
        },
        'легкий': {
            'length': 10,
            'digits': True,
            'symbols': False,
            'uppercase': True,
            'lowercase': True
        },
        'только-цифры': {
            'length': 6,
            'digits': True,
            'symbols': False,
            'uppercase': False,
            'lowercase': False
        },
        'парольная-фраза': {
            'length': 20,
            'digits': False,
            'symbols': False,
            'uppercase': True,
            'lowercase': True,
            'words': True
        }
    }
    
    WORDS = ['кошка', 'собака', 'солнце', 'луна', 'звезда', 'облако', 
             'дождь', 'ветер', 'огонь', 'вода', 'земля', 'небо']
    
    @staticmethod
    def generate(length=16, use_digits=True, use_symbols=True, 
                 use_uppercase=True, use_lowercase=True, 
                 exclude_ambiguous=False, use_words=False):
        """Генерация пароля с расширенными настройками"""
        
        if use_words:
            # Генерация из слов
            words = secrets.choice(PasswordGenerator.WORDS) 
            for _ in range(length // 5):
                words += secrets.choice(['.', '-', '_', '']) + secrets.choice(PasswordGenerator.WORDS)
            return words[:length]
        
        chars = ''
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += string.punctuation
            
        if exclude_ambiguous:
            ambiguous = 'il1Lo0O'
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        if not chars:
            raise ValueError("Выберите хотя бы один тип символов")
        
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    @staticmethod
    def check_strength(password):
        """Оценка сложности (0-100)"""
        score = 0
        length = len(password)
        
        # Длина
        if length >= 8: score += 20
        if length >= 12: score += 10
        if length >= 16: score += 10
        if length >= 24: score += 10
        
        # Разнообразие символов
        if re.search(r'[a-z]', password): score += 10
        if re.search(r'[A-Z]', password): score += 10
        if re.search(r'\d', password): score += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 10
        if re.search(r'[^a-zA-Z0-9]', password): score += 10
        
        # Штраф за повторения
        if len(set(password)) < length * 0.7:
            score -= 10
        
        return min(100, max(0, score))
    
    @staticmethod
    def get_strength_label(score):
        if score >= 80: return ('Отличный', '#34c759')
        elif score >= 60: return ('Хороший', '#ff9500')
        elif score >= 40: return ('Средний', '#ffcc00')
        elif score >= 20: return ('Слабый', '#ff3b30')
        return ('Очень слабый', '#ff3b30')
    
    @classmethod
    def generate_by_category(cls, category):
        """Генерация по категории"""
        if category not in cls.PATTERNS:
            raise ValueError(f"Неизвестная категория: {category}")
        
        params = cls.PATTERNS[category]
        return cls.generate(**params)