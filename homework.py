from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = self.get_distance() / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    """Тренировка: бег."""
    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                    / self.M_IN_KM * self.duration * self.MIN_IN_H)
        return calories


class SportsWalking(Training):

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        calories = (self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                    + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                       / (self.height / self.CM_IN_M))
                    * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                    * self.weight) * self.duration * self.MIN_IN_H
        return calories


class Swimming(Training):
    LEN_STEP: float = 1.38
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.CALORIES_WEIGHT_MULTIPLIER
                    * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {"SWM": Swimming,
                                                 "RUN": Running,
                                                 "WLK": SportsWalking}
    if workout_type in training_types:
        return training_types[workout_type](*data)
    else:
        raise AttributeError('Неверный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    sample = training.show_training_info()
    print(sample.get_message())


if __name__ == '__main__':
    packages: Dict[str, int] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
