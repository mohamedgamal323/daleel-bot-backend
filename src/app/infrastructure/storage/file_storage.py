class FileStorage:
    def save(self, data: bytes, filename: str) -> str:
        # pretend to save and return path
        return f"/tmp/{filename}"
