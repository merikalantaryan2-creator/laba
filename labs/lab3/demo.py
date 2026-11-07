from pathlib import Path
from tempfile import TemporaryDirectory
from .game.facade import GameFacade
from .hero.hero import Hero
from .enemy.enemies import Enemy, Dragon, HauntedWeapon
from .enemy.decorators import LegendaryEnemy, WindfuryEnemy, ArmoredEnemy
from .tactic.strategies import BalancedTactic, AggressiveTactic, CautiousTactic
from .defense.damage import Damage
from .defense.handlers import EvasionHandler, ArmorHandler, BarrierHandler


def main():
    print("=== Decorator ===")
    enemy = ArmoredEnemy(LegendaryEnemy(WindfuryEnemy(Enemy())))
    print(enemy.name, "урон:", enemy.roll_damage().damage)
    print("=== Adapter ===")
    weapon_enemy = HauntedWeapon({"name": "Эльфийский лук", "damage": 14, "price": 90})
    print(weapon_enemy.name, weapon_enemy.health)
    print("=== Strategy ===")
    hero = Hero("Артур")
    for tactic in (BalancedTactic(), AggressiveTactic(), CautiousTactic()):
        print(tactic.name, "множитель:", tactic.choose_action(hero, enemy, 2))
    print("=== Chain of Responsibility ===")
    chain = EvasionHandler(0.0)
    chain.set_next(ArmorHandler(0.3)).set_next(BarrierHandler(10))
    damage = chain.handle(Damage(30))
    print("получено:", damage.amount, "поглощено:", damage.absorbed)
    print("=== Observer + Proxy + Facade ===")
    with TemporaryDirectory() as folder:
        game = GameFacade(Path(folder) / "heroes.json")
        hero = game.create_hero("Демо", "Воин")
        print("фасад создал героя:", hero.name)
        print("кэш заместителя и json-хранилище готовы")
        print("подписчики событий:", len(game.events._listeners))


if __name__ == "__main__":
    main()
