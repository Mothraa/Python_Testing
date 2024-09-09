# memo : pas besoin d'importer les fixtures présentes dans conftest, pytest s'en charge !

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'GUDLFT Registration' in response.data
