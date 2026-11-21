from pathlib import Path
from ..hero.hero import Hero
from ..world.locations import Forest, Crypt, DragonLair, HauntedManor
from ..tactic.strategies import BalancedTactic, AggressiveTactic, CautiousTactic
from ..combat.battle import Battle
from ..storage.repository import FileHeroRepository, CachingHeroRepository
from ..event.observer import GameEventPublisher, EventType, GameEvent, AchievementTracker, ExpeditionJournal


class GameFacade:
    # фасад объединяет игровые подсистемы и дает простой интерфейс
    def __init__(self, save_path=Path("saves/heroes.json")):
        self.repository = CachingHeroRepository(FileHeroRepository(save_path))
        self.events = GameEventPublisher()
        self.journal = ExpeditionJournal()
        self.events.subscribe(EventType.VICTORY, AchievementTracker())
        self.events.subscribe(EventType.DEFEAT, self.journal)
        self.events.subscribe(EventType.VICTORY, self.journal)
        self.locations = [Forest(), Crypt(), HauntedManor(), DragonLair()]
        self.tactics = [BalancedTactic(), AggressiveTactic(), CautiousTactic()]
        self.heroes = {}
        for data in self.repository.find_all():
            hero = Hero(data["name"], data["hero_class"])
            hero.level = data["level"]
            hero.experience = data["experience"]
            hero.gold = data["gold"]
            hero.achievements = data["achievements"]
            hero._health = data["health"]
            self.heroes[hero.name] = hero

    def create_hero(self, name, hero_class):
        if not name.strip():
            raise ValueError("Имя не должно быть пустым")
        if name in self.heroes:
            raise ValueError("Герой с таким именем уже существует")
        hero = Hero(name, hero_class)
        self.heroes[name] = hero
        self.save(hero)
        return hero

    def save(self, hero):
        data = [{"name": h.name, "hero_class": h.hero_class, "level": h.level,
                 "experience": h.experience, "gold": h.gold, "health": h.health,
                 "achievements": h.achievements} for h in self.heroes.values()]
        self.repository.save_data(data)

    def explore(self, hero_name, location_index, tactic_index):
        hero = self.heroes[hero_name]
        location = self.locations[location_index]
        tactic = self.tactics[tactic_index]
        hero.rest()
        enemy = location.create_enemy()
        report = Battle(hero, enemy, tactic).run()
        if report["victory"]:
            hero.gain_experience(enemy.experience_reward)
            hero.gold += enemy.experience_reward // 2
            event = GameEvent(EventType.VICTORY, hero, f"{location.name}: победа над {enemy.name}")
        else:
            hero.gold //= 2
            event = GameEvent(EventType.DEFEAT, hero, f"{location.name}: поражение от {enemy.name}")
        self.events.publish(event)
        self.save(hero)
        return report, enemy.name, location.name, tactic.name
