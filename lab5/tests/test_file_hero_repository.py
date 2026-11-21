from labs.lab3.storage.repository import CachingHeroRepository, FileHeroRepository

HEROES = [{"name": "Артур", "hero_class": "Воин", "level": 2, "experience": 35,
           "gold": 175, "health": 90, "achievements": ["Первая кровь"]}]


class TestFileHeroRepository:
    """Интеграция: настоящий репозиторий + JSON + файловая система (без моков)."""

    def test_restores_data_through_new_repository(self, tmp_path):
        file = tmp_path / "heroes.json"
        FileHeroRepository(file).save_data(HEROES)

        restored = FileHeroRepository(file).find_all()

        assert restored == HEROES
        assert restored is not HEROES

    def test_missing_file_means_empty_storage(self, tmp_path):
        assert FileHeroRepository(tmp_path / "missing.json").find_all() == []

    def test_save_creates_missing_directories(self, tmp_path):
        file = tmp_path / "saves" / "nested" / "heroes.json"
        FileHeroRepository(file).save_data(HEROES)
        assert file.exists()

    def test_file_keeps_cyrillic_readable(self, tmp_path):
        file = tmp_path / "heroes.json"
        FileHeroRepository(file).save_data(HEROES)
        assert "Артур" in file.read_text(encoding="utf-8")

    def test_proxy_over_real_file_repository(self, tmp_path):
        file = tmp_path / "heroes.json"
        cache = CachingHeroRepository(FileHeroRepository(file))

        cache.save_data(HEROES)

        assert FileHeroRepository(file).find_all() == HEROES
        assert cache.find_all() == HEROES
