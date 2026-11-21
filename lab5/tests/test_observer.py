from unittest.mock import call, create_autospec

from labs.lab3.event.observer import (
    AchievementTracker, EventType, ExpeditionJournal, GameEvent, GameEventPublisher)
from labs.lab3.hero.hero import Hero


def listener():
    return create_autospec(ExpeditionJournal, instance=True)


class TestGameEventPublisher:
    """Observer: издатель оповещает всех подписчиков нужного типа события."""

    def test_notifies_every_subscriber_once(self):
        publisher = GameEventPublisher()
        first, second = listener(), listener()
        publisher.subscribe(EventType.VICTORY, first)
        publisher.subscribe(EventType.VICTORY, second)
        event = GameEvent(EventType.VICTORY, Hero("Артур"), "победа")

        publisher.publish(event)

        first.on_event.assert_called_once_with(event)
        second.on_event.assert_called_once_with(event)

    def test_ignores_subscribers_of_other_event_types(self):
        publisher = GameEventPublisher()
        defeat_listener = listener()
        publisher.subscribe(EventType.DEFEAT, defeat_listener)

        publisher.publish(GameEvent(EventType.VICTORY, Hero("Артур"), "победа"))

        defeat_listener.on_event.assert_not_called()

    def test_same_listener_can_follow_several_event_types(self):
        publisher = GameEventPublisher()
        journal = listener()
        publisher.subscribe(EventType.VICTORY, journal)
        publisher.subscribe(EventType.DEFEAT, journal)
        hero = Hero("Артур")
        win = GameEvent(EventType.VICTORY, hero, "win")
        lose = GameEvent(EventType.DEFEAT, hero, "lose")

        publisher.publish(win)
        publisher.publish(lose)

        assert journal.on_event.call_args_list == [call(win), call(lose)]

    def test_publish_without_subscribers_is_safe(self):
        GameEventPublisher().publish(GameEvent(EventType.LOOT, Hero("Артур"), "лут"))


class TestObservers:
    def test_journal_records_descriptions(self):
        journal = ExpeditionJournal()
        hero = Hero("Артур")
        journal.on_event(GameEvent(EventType.VICTORY, hero, "первая запись"))
        journal.on_event(GameEvent(EventType.DEFEAT, hero, "вторая запись"))
        assert journal.entries == ["первая запись", "вторая запись"]

    def test_first_victory_gives_achievement_only_once(self):
        tracker, hero = AchievementTracker(), Hero("Артур")
        event = GameEvent(EventType.VICTORY, hero, "победа")

        tracker.on_event(event)
        tracker.on_event(event)

        assert hero.achievements == ["Первая кровь"]

    def test_defeat_gives_no_first_blood(self):
        tracker, hero = AchievementTracker(), Hero("Артур")
        tracker.on_event(GameEvent(EventType.DEFEAT, hero, "поражение"))
        assert hero.achievements == []

    def test_level_five_gives_veteran(self):
        tracker, hero = AchievementTracker(), Hero("Артур")
        hero.level = 5
        tracker.on_event(GameEvent(EventType.VICTORY, hero, "победа"))
        assert "Ветеран" in hero.achievements
