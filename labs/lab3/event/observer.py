from dataclasses import dataclass
from enum import Enum, auto


class EventType(Enum):
    VICTORY = auto()
    DEFEAT = auto()
    LOOT = auto()


@dataclass
class GameEvent:
    type: EventType
    hero: object
    description: str


class GameEventPublisher:
    # издатель уведомляет всех подписчиков о событии
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, listener):
        self._listeners.setdefault(event_type, []).append(listener)

    def publish(self, event):
        for listener in self._listeners.get(event.type, []):
            listener.on_event(event)


class AchievementTracker:
    def on_event(self, event):
        if event.type == EventType.VICTORY and "Первая кровь" not in event.hero.achievements:
            event.hero.achievements.append("Первая кровь")
        if event.hero.level >= 5 and "Ветеран" not in event.hero.achievements:
            event.hero.achievements.append("Ветеран")


class ExpeditionJournal:
    def __init__(self):
        self.entries = []

    def on_event(self, event):
        self.entries.append(event.description)
