import pytest
from labs.lab3.enemy.enemies import Enemy
from labs.lab3.game.facade import GameFacade
from labs.lab3.hero.hero import Hero


class TestGameFacade:
    """Интеграция: фасад + кэширующий заместитель + файл + герой + события."""

    def test_created_hero_survives_restart(self, tmp_path):
        save = tmp_path / "heroes.json"
        game = GameFacade(save)
        hero = game.create_hero("Артур", "Маг")
        hero.gold = 120
        game.save(hero)

        reloaded = GameFacade(save)

        restored = reloaded.heroes["Артур"]
        assert restored is not hero
        assert restored.hero_class == "Маг"
        assert restored.gold == 120
        assert restored.max_health == 85

    def test_rejects_blank_and_duplicate_names(self, tmp_path):
        game = GameFacade(tmp_path / "heroes.json")
        game.create_hero("Артур", "Воин")

        with pytest.raises(ValueError, match="пустым"):
            game.create_hero("   ", "Воин")
        with pytest.raises(ValueError, match="уже существует"):
            game.create_hero("Артур", "Воин")

    def test_victory_updates_hero_journal_and_save(self, tmp_path, monkeypatch):
        save = tmp_path / "heroes.json"
        game = GameFacade(save)
        game.create_hero("Артур", "Воин")
        # слабый враг гарантирует победу: удар героя не меньше 10
        monkeypatch.setattr(game.locations[0], "create_enemy",
                            lambda: Enemy("Крыса", 1, (1, 1), 40))

        report, enemy_name, location_name, tactic_name = game.explore("Артур", 0, 0)

        hero = game.heroes["Артур"]
        assert report["victory"] is True
        assert (enemy_name, location_name, tactic_name) == ("Крыса", "Мистический лес", "Баланс")
        assert hero.experience == 40
        assert hero.gold == 50 + 20
        assert "Первая кровь" in hero.achievements
        assert game.journal.entries == ["Мистический лес: победа над Крыса"]
        assert GameFacade(save).heroes["Артур"].gold == 70

    def test_defeat_halves_gold(self, tmp_path, monkeypatch):
        game = GameFacade(tmp_path / "heroes.json")
        hero = game.create_hero("Артур", "Воин")
        monkeypatch.setattr(game.locations[0], "create_enemy",
                            lambda: Enemy("Титан", 100_000, (10_000, 10_000), 1))

        report, *_ = game.explore("Артур", 0, 0)

        assert report["victory"] is False
        assert hero.gold == 25
        assert game.journal.entries == ["Мистический лес: поражение от Титан"]


class TestHero:
    def test_level_up_restores_health_and_grows_max_health(self):
        hero = Hero("Артур")
        hero.gain_experience(150)
        assert (hero.level, hero.experience) == (2, 50)
        assert hero.max_health == 115
        assert hero.health == 115

    def test_class_defines_max_health(self):
        assert Hero("А", "Воин").max_health == 100
        assert Hero("Б", "Маг").max_health == 85
