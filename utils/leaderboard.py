import json
import os

class Leaderboard:
    def __init__(self, filename='leaderboard.json'):
        self.filename = filename
        self.scores = []
        self.max_scores = 10  # Guardamos los 10 mejores puntajes
        self.load()
        
    def load(self):
        """Carga los puntajes del archivo"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.scores = json.load(f)
        except:
            self.scores = []
            
    def save(self):
        """Guarda los puntajes en el archivo"""
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f)
            
    def add_score(self, name, score, nivel):
        """Agrega un nuevo puntaje y mantiene solo los mejores"""
        self.scores.append({
            'name': name,
            'score': score,
            'nivel': nivel,
            'fecha': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        # Ordenar por puntaje, de mayor a menor
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        # Mantener solo los mejores
        self.scores = self.scores[:self.max_scores]
        self.save()
        
    def get_position(self, score):
        """Obtiene la posición que tendría un puntaje"""
        position = 1
        for s in self.scores:
            if score > s['score']:
                return position
            position += 1
        return position if position <= self.max_scores else None
        
    def is_high_score(self, score):
        """Verifica si un puntaje califica para el leaderboard"""
        if len(self.scores) < self.max_scores:
            return True
        return score > self.scores[-1]['score'] 