SECRET_KEY = 'some-secret-key-text'
SERVER_NAME = 'localhost:8085'
DEBUG = True

RESOURCES = {
    "photos": {
        "protected": True,
        "content": [{'id': 1, 'filename': 'https://example.com/photo1.jpg'}],
        "scope_map": {"GET": ["view", "all"], "POST": ["add","all"]}
    },
    "docs": {
        "protected": False,
        "content": [{'id': 2, 'filename': 'https://example.com/document1.pdf'}]
    }
}
