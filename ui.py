from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from main_window import MainWindow as ChannelWindow
from telegram_client import create_client, send_code, sign_in
from config import save_config, load_config


class MainWindow(QWidget):
    channel_window = None
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Telegram Channel Manager")
        self.resize(700, 500)

        self.create_widgets()
        self.create_layout()
        self.load_settings()
        self.connect_signals()
        self.check_session()
    def check_session(self):

        import asyncio
        from telegram_client import check_authorized

        try:

            result = asyncio.run(
    check_authorized(
            self.api_id.text(),
            self.api_hash.text()
        )
    )

            if result:

                self.log.append("Сессия найдена!")
                self.log.append("Пользователь уже авторизован.")
                self.open_channel_window()

            else:

                self.log.append("Сессия не найдена.")

        except Exception as e:

            self.log.append(f"Ошибка проверки: {e}")
    def open_channel_window(self):

        self.channel_window = ChannelWindow()
        self.channel_window.show()

        self.close()

    def create_widgets(self):

        self.title = QLabel("Telegram Channel Manager")

        self.title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        self.api_id = QLineEdit()
        self.api_id.setPlaceholderText("API ID")

        self.api_hash = QLineEdit()
        self.api_hash.setPlaceholderText("API HASH")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("+7XXXXXXXXXX")
        self.code = QLineEdit()
        self.code.setPlaceholderText("Код из Telegram")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль Telegram 2FA")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Войти в Telegram")
        self.code_button = QPushButton("Получить код")

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        self.log.append("Программа запущена...")
        self.log.append("Проверка сохраненной сессии...")

    def create_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(self.title)
        layout.addWidget(self.api_id)
        layout.addWidget(self.api_hash)
        layout.addWidget(self.phone)
        layout.addWidget(self.code)
        layout.addWidget(self.password)
        layout.addWidget(self.code_button)
        layout.addWidget(self.login_button)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def load_settings(self):

        api_id, api_hash, phone = load_config()

        self.api_id.setText(api_id)
        self.api_hash.setText(api_hash)
        self.phone.setText(phone)

    def connect_signals(self):

        self.login_button.clicked.connect(self.login)
        self.code_button.clicked.connect(self.get_code)

    def login(self):

        self.log.append("")
        self.log.append("Подготовка подключения...")

        try:

            save_config(
                self.api_id.text(),
                self.api_hash.text(),
                self.phone.text()
            )

            create_client(
                self.api_id.text(),
                self.api_hash.text()
            )

            import asyncio

            asyncio.run(
                sign_in(
                    self.phone.text(),
                    self.code.text(),
                    self.password.text()
                )
            )

            self.log.append("Авторизация успешна!")
            self.log.append("Сессия сохранена.")

            #print("Переход в главное окно")

            #print("ШАГ 1: создаем главное окно")

            #MainWindow.channel_window = ChannelWindow()

            #print("ШАГ 2: окно создано")

            #MainWindow.channel_window.show()

            #print("ШАГ 3: команда show выполнена")

            #self.close()

        except Exception as e:

            self.log.append(f"Ошибка: {e}")

    def get_code(self):

        self.log.append("")
        self.log.append("Отправляем запрос к Telegram...")

        try:

            create_client(
                self.api_id.text(),
                self.api_hash.text()
            )

            import asyncio

            asyncio.run(
                send_code(
                    self.phone.text()
                )
            )

            self.log.append("Код отправлен в Telegram!")

        except Exception as e:

            self.log.append(f"Ошибка: {e}")