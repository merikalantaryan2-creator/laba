from abc import ABC, abstractmethod

# 1. Замена интерфейса Pet (Абстрактный класс с сигнатурами методов)
class Pet(ABC):
    @abstractmethod
    def express(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_age(self):
        pass

    @abstractmethod
    def get_age_in_human_years(self):
        pass

# 2. Абстрактный класс Animal (реализует общий контракт Pet)
class Animal(Pet):
    def __init__(self, name, age):
        self._name = name
        self._age = age

    def happy_birthday(self):
        self._age += 1

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    @abstractmethod
    def express(self):
        pass

    @abstractmethod
    def get_age_in_human_years(self):
        pass

# 3. Класс Turtle (с переопределенными методами)
class Turtle(Animal):
    def get_age_in_human_years(self):
        if self.get_age() <= 0:
            return 0
        return 15 + (self.get_age() - 1) * 2

    def express(self):
        print("""  _     ____
 /      \\  |  o |
|        |/ ___\\|
|_____/
|_|_| |_|_|""")

# 4. Класс Parrot (с переопределенными методами)
class Parrot(Animal):
    def get_age_in_human_years(self):
        return self.get_age() * 5

    def express(self):
        print(f'{self.get_name()}: "Hello!"')
        print("""   \\
   (o>
\\\\_//)
 \\_/_)
  _|_""")

# 5. Класс Person
class Person:
    def __init__(self, name, pet=None):
        self._name = name
        self._pet = pet

    def set_pet(self, pet):
        self._pet = pet

    # Метод вывода информации о питомце
    def get_pet_info(self):
        print("-" * 20)
        if self._pet is None:
            print(f"{self._name} has no pet yet")
            print("-" * 20)
            return

        print(f"Pet for {self._name} is named {self._pet.get_name()}")
        print(f"Age: {self._pet.get_age()} year(s), about {self._pet.get_age_in_human_years()} human years")
        print("And it expresses itself like this:")
        self._pet.express()
        print("-" * 20)

# ОСНОВНАЯ ПРОГРАММА
if __name__ == "__main__":
    
    kesha = Parrot("Kesha", 2)
    zavala = Turtle("Zavala", 4)
    
    kesha.happy_birthday()
 
    jack = Person("Jack", kesha)
    john = Person("John")

    jack.get_pet_info()
    
    print("-" * 20)
    john.get_pet_info()
    print("-" * 20)
   
    john.set_pet(zavala)
    john.get_pet_info()