M_IN_KM = 1000


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 LEN_STEP: float = 0.65
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = LEN_STEP

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__, self.duration,
            self.get_distance(), self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        CALORIES_MEAN_SPEED_MULTIPLIER = 18
        CALORIES_MEAN_SPEED_SHIFT = 1.79

        # (18 * средняя_скорость + 1.79) * вес_спортсмена
        # / M_IN_KM * время_тренировки_в_минутах
        return ((CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed()
                + CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        WEIGHT_MULTIPLICATOR_1 = 0.035
        WEIGHT_MULTIPLICATOR_2 = 0.035

        # ((0.035 * вес + (средняя_скорость_в_метрах_в_секунду**2
        # / рост_в_метрах) * 0.029 * вес) * время_тренировки_в_минутах)
        return ((WEIGHT_MULTIPLICATOR_1 * self.weight
                 + (super().get_mean_speed()**2 / self.height)
                 * WEIGHT_MULTIPLICATOR_2 * self.weight) * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        # Переопределяем расстояние за 1 гребок
        self.LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        SPEED_MULTIPLICATOR_1 = 1.1
        SPEED_MULTIPLICATOR_2 = 2

        # (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        return ((super().get_mean_speed() * SPEED_MULTIPLICATOR_1)
                * SPEED_MULTIPLICATOR_2
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    training = training_types[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
