from typing import Any


class MockFirebaseClient:
    def __init__(self) -> None:
        pass

    def collection(self, collection_name: str) -> "MockFirebaseClient":
        return self

    def document(self, document_name: str) -> "MockFirebaseClient":
        return self

    def set(self, data: dict[str, Any]) -> None:
        pass
