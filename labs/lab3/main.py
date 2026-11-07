from .game.facade import GameFacade
from .console_view import ConsoleView


def main():
    game = GameFacade()
    view = ConsoleView()
    print("=== Лабораторная 4: RPG ===")
    name = input("Имя героя: ").strip()
    if name in game.heroes:
        hero = game.heroes[name]
        print("загружено сохранение")
    else:
        hero_class = input("Класс (Воин/Маг): ").strip() or "Воин"
        hero = game.create_hero(name or "Артур", hero_class)
    while True:
        view.show_hero(hero)
        print("1 — экспедиция, 2 — журнал, 0 — выход")
        choice = input("> ").strip()
        if choice == "1":
            print("Локации:")
            for i, location in enumerate(game.locations, 1):
                print(f"{i}. {location.name}")
            try:
                location_index = int(input("номер локации: ")) - 1
                if not 0 <= location_index < len(game.locations):
                    print("нет такой локации")
                    continue
                print("Тактики:")
                for i, tactic in enumerate(game.tactics, 1):
                    print(f"{i}. {tactic.name}")
                tactic_index = int(input("номер тактики: ")) - 1
                if not 0 <= tactic_index < len(game.tactics):
                    print("нет такой тактики")
                    continue
                report, enemy_name, location_name, tactic_name = game.explore(name or "Артур", location_index, tactic_index)
                view.show_battle(report, enemy_name, location_name, tactic_name)
            except ValueError:
                print("введи номер")
        elif choice == "2":
            for entry in game.journal.entries:
                print(entry)
            if not game.journal.entries:
                print("журнал пока пуст")
        elif choice == "0":
            game.save(hero)
            print("прогресс сохранен")
            break
        else:
            print("нет такого пункта")


if __name__ == "__main__":
    main()
