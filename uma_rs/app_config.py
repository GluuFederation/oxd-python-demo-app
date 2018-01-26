SECRET_KEY = 'some-secret-key-text'
SERVER_NAME = 'localhost:8085'
DEBUG = True

RESOURCES = {
    "photos": {
        "content": [{'id': 1, 'filename': 'https://example.com/photo1.jpg'}],
        "protected": True,
        "scope_map": {"GET": ["view", "all"], "POST": ["add","all"]}
    },
    "docs": {
        "content": [{'id': 1, 'filename': 'https://example.com/document1.pdf'}],
        "protected": False
    }
}
