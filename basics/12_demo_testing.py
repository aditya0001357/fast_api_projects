from fastapi.testclient import TestClient
# from  import app

client = TestClient(app)

def test_home():
    response = client.get('/todos')
    assert response.status_code == 200

    assert response.json() == {'message': 'Hello World'}
