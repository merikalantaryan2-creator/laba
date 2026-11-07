import json
from pathlib import Path


class FileHeroRepository:
    def __init__(self, path):
        self.path = Path(path)

    def find_all(self):
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return data

    def save_data(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class CachingHeroRepository:
    # заместитель добавляет ленивый кэш к файловому хранилищу
    def __init__(self, target):
        self.target = target
        self._cache = None

    def find_all(self):
        if self._cache is None:
            self._cache = self.target.find_all()
        return self._cache

    def save_data(self, data):
        self.target.save_data(data)
        self._cache = data
