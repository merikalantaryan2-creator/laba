from unittest.mock import create_autospec

from labs.lab3.storage.repository import CachingHeroRepository, FileHeroRepository

HEROES = [{"name": "Артур", "hero_class": "Воин", "level": 1}]


def make_storage(data=None):
    storage = create_autospec(FileHeroRepository, instance=True)
    if data is not None:
        storage.find_all.return_value = data
    return storage


class TestCachingHeroRepository:
    """Proxy: проверяем кеширование, подменив настоящее хранилище моком."""

    def test_loads_lazily(self):
        storage = make_storage()
        CachingHeroRepository(storage)
        assert storage.mock_calls == []

    def test_reads_storage_only_once(self):
        storage = make_storage(HEROES)
        cache = CachingHeroRepository(storage)

        first = cache.find_all()
        second = cache.find_all()

        assert first is HEROES
        assert second is first
        storage.find_all.assert_called_once_with()

    def test_caches_empty_storage(self):
        storage = make_storage([])
        cache = CachingHeroRepository(storage)

        assert cache.find_all() == []
        assert cache.find_all() == []
        storage.find_all.assert_called_once_with()

    def test_save_goes_to_storage_and_updates_cache(self):
        storage = make_storage(HEROES)
        cache = CachingHeroRepository(storage)
        cache.find_all()
        updated = [{"name": "Артур", "hero_class": "Воин", "level": 2}]

        cache.save_data(updated)

        storage.save_data.assert_called_once_with(updated)
        assert cache.find_all() is updated
        storage.find_all.assert_called_once_with()

    def test_save_before_read_fills_cache_without_reading_storage(self):
        storage = make_storage()
        cache = CachingHeroRepository(storage)
        data = [{"name": "Мерлин"}]

        cache.save_data(data)

        assert cache.find_all() is data
        storage.find_all.assert_not_called()
