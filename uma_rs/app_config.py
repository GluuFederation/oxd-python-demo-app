SECRET_KEY = 'some-secret-key-text'
SERVER_NAME = 'localhost:8085'
DEBUG = True

RESOURCES = {
    "photos": {
        "content": [{'id': 1, 'filename': 'https://example.com/photo1.jpg'}],
        "protected": True
    },
    "docs": {
        "content": [{'id': 1, 'filename': 'https://example.com/document1.pdf'}],
        "protected": False
    }
}
SCOPE_MAP = {
    "GET": ["https://resource.example.com/uma/scope/view",
            "https://resource.example.com/uma/scope/all"],
    "POST": ["https://resource.example.com/uma/scope/add",
            "https://resource.example.com/uma/scope/all"],
}