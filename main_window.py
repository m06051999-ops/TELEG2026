import asyncio

from channel_manager import get_channels

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout
)


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Telegram Channel Manager"
        )

        self.resize(700, 500)

        self.create_widgets()
        self.create_layout()


    def create_widgets(self):

        self.title = QLabel(
            "Telegram Channel Manager"
        )

        self.status = QLabel(
            "Статус: Авторизован"
        )


        self.channels_button = QPushButton(
            "Мои каналы"
        )
        self.channels_button.clicked.connect(
            self.load_channels
        )

        self.excel_button = QPushButton(
            "Импорт Excel"
        )

        self.create_button = QPushButton(
            "Создать каналы"
        )


        self.log = QTextEdit()

        self.log.setReadOnly(True)

        self.log.append(
            "Главное окно запущено."
        )


    def create_layout(self):

        layout = QVBoxLayout()


        layout.addWidget(self.title)

        layout.addWidget(self.status)

        layout.addWidget(
            self.channels_button
        )

        layout.addWidget(
            self.excel_button
        )

        layout.addWidget(
            self.create_button
        )

        layout.addWidget(
            self.log
        )


        self.setLayout(layout)
    def load_channels(self):

        self.log.append("")
        self.log.append(
            "Получение каналов..."
        )

        try:

            channels = asyncio.run(
                get_channels()
            )


            self.log.append(
                f"Найдено каналов: {len(channels)}"
            )


            for channel in channels:

                self.log.append(
                    f"{channel['title']} | ID: {channel['id']}"
                )


        except Exception as e:

            self.log.append(
                f"Ошибка: {e}"
            )