class ConsoleView:
    def show_hero(self, hero):
        print(f"\n{hero.name} — {hero.hero_class}, уровень {hero.level}")
        print(f"здоровье: {hero.health}/{hero.max_health}; золото: {hero.gold}; опыт: {hero.experience}")
        print("достижения: " + (", ".join(hero.achievements) if hero.achievements else "пока нет"))

    def show_battle(self, report, enemy_name, location_name, tactic_name):
        print(f"\n{location_name}: противник — {enemy_name}; тактика — {tactic_name}")
        for line in report["log"]:
            print(line)
        print("победа!" if report["victory"] else "поражение")
