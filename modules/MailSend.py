import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSend:
    def __init__(self, mail_body: str, file_path: str = "../settings.conf"):
        self.mail_sender_login = ''
        self.mail_sender_password = ''
        self.mail_receiver_address = ''
        self.mail_subject = ''
        self.mail_body = mail_body

        self.settings = {}
        self.settings_loaded = False

        self.file_path = os.path.join(os.path.dirname(__file__), file_path)

        print("MailSend - Загружаем конфиг из:", self.file_path)

        # Вызов __call__ при инициализации
        self()

    def __load_settings(self) -> None:
        """
        Описание:
        Загружает данные из конфига в словарь settings
        Если данные уже загружены мы их НЕ загружаем повторно

        Параметры:
        Нет

        Возвращает:
        None
        """
        with open(self.file_path, 'r') as file:
            for line in file:
                # Удаляем лишние пробелы и символы перевода строки
                line = line.strip()

                # Пропускаем пустые строки и комментарии
                if line and not line.startswith('#'):
                    # Разделяем ключ и значение
                    key, value = line.split('=')

                    # Удаляем лишние пробелы
                    key = key.strip()
                    value = value.strip()

                    self.settings[key] = value

            print('MailSend - Данные успешно загружены из файла')

    def __apply_settings(self) -> None:
        """
        Описание:
        Применяет настройки, считывая их из словаря self.settings.
        Присваивает значения переменным объекта на основе полученных ключей.

        Устанавливает флаг self.settings_loaded в True, чтобы указать, что
        настройки успешно загружены.

        Параметры:
        Нет

        Возвращает:
        None
        Метод устанавливает значения переменным объекта, а не возвращает данные.
        """
        self.mail_sender_login = self.settings.get('mail_sender_login')
        self.mail_sender_password = self.settings.get('mail_sender_password')
        self.mail_receiver_address = self.settings.get('mail_receiver_address')
        self.mail_subject = self.settings.get('mail_subject')
        self.settings_loaded = True
        print('MailSend - Данные успешно применены')

    def __send_email(self, email_details: dict) -> None:
        """
        Описание:
        Отправляет электронное письмо через SMTP-сервер Gmail.

        Параметры:
        email_details (dict): Словарь с ключами:
        sender_email (str): Адрес электронной почты отправителя.
        sender_password (str): Пароль от электронной почты отправителя.
        receiver_email (str): Адрес электронной почты получателя.
        subject (str): Тема письма.
        body (str): Текстовое содержимое письма.

        Возвращает:
        None
        """

        sender_email = email_details['sender_email']
        sender_password = email_details['sender_password']
        receiver_email = email_details['receiver_email']
        subject = email_details['subject']
        body = email_details['body']

        try:
            # Создание объекта MIMEText
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Добавление текста письма в объект MIMEText
            # где plain - текст, html - html
            msg.attach(MIMEText(body, 'html'))

            # Установка соединения с SMTP-сервером
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            # Авторизация на сервере
            server.login(sender_email, sender_password)

            # Отправка письма
            server.sendmail(sender_email, receiver_email, msg.as_string())

            # Закрытие соединения с сервером
            server.quit()
            print('Письмо успешно отправлено!')
        except Exception as e:
            print('Ошибка при отправке письма:', e)

    def __call__(self) -> None:
        """
        Описание:
        Выполняет основной функционал, связанный с загрузкой настроек и
        отправкой электронного письма.

        Параметры:
        Нет

        Возвращает:
        None
        """

        if not self.settings_loaded:
            self.__load_settings()
            self.__apply_settings()

        email_details = {
            'sender_email': self.mail_sender_login,
            'sender_password': self.mail_sender_password,
            'receiver_email': self.mail_receiver_address,
            'subject': self.mail_subject,
            'body': self.mail_body
        }

        self.__send_email(email_details)
