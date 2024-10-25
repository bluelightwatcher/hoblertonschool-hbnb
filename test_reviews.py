import unittest
from flask import Flask
from flask_restx import Api
from app.api.reviews import api as reviews_api  # Assurez-vous d'importer correctement votre module d'API

# Mock du module facade pour éviter de toucher à la base de données réelle
from unittest.mock import patch

app = Flask(__name__)
app.config['TESTING'] = True  # Activer le mode test pour Flask
api = Api(app)
api.add_namespace(reviews_api, path='/reviews')

class TestReviewAPI(unittest.TestCase):

    def setUp(self):
        """Initialisation des tests, configurer le client de test Flask."""
        self.client = app.test_client()
        
    @patch('app.services.facade.create_review')  # Mock la fonction create_review
    def test_create_review(self, mock_create_review):
        # Configurer le mock pour qu'il retourne une réponse simulée
        mock_create_review.return_value = {
            'id': "2fa85f64-5717-4562-b3fc-2c963f66afa6",
            'text': "Great place to stay!",
            'rating': 5,
            'user_id': "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            'place_id': "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
        # Envoyer une requête POST au endpoint
        response = self.client.post('/reviews/', json={
            'text': "Great place to stay!",
            'rating': 5,
            'user_id': "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            'place_id': "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        # Vérifier la réponse
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    @patch('app.services.facade.get_all_reviews')
    def test_get_all_reviews(self, mock_get_all_reviews):
        # Mock pour simuler les données de retour
        mock_get_all_reviews.return_value = [
            {'id': '1', 'text': 'Great!', 'rating': 4, 'user_id': 'user1', 'place_id': 'place1'},
            {'id': '2', 'text': 'Not bad', 'rating': 3, 'user_id': 'user2', 'place_id': 'place1'}
        ]
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    # Ajoutez ici d'autres tests pour les autres endpoints (PUT, DELETE, etc.)

if __name__ == '__main__':
    unittest.main()
