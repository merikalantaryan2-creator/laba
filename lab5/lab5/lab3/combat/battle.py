from .combatant import Combatant


class Battle:
    def __init__(self, hero: Combatant, enemy: Combatant, tactic):
        self.hero = hero
        self.enemy = enemy
        self.tactic = tactic

    def run(self):
        round_number = 0
        log = []
        while self.hero.is_alive() and self.enemy.is_alive() and round_number < 30:
            round_number += 1
            multiplier = self.tactic.choose_action(self.hero, self.enemy, round_number)
            hero_hit = self.hero.roll_damage()
            damage = round(hero_hit.damage * multiplier)
            result = self.enemy.receive_hit(damage)
            log.append(f"раунд {round_number}: герой наносит {result.amount} урона")
            if not self.enemy.is_alive():
                break
            enemy_hit = self.enemy.roll_damage()
            received = self.hero.receive_hit(enemy_hit.damage)
            log.append(f"враг наносит {received.amount} урона")
        victory = self.hero.is_alive() and not self.enemy.is_alive()
        return {"victory": victory, "log": log, "rounds": round_number}
