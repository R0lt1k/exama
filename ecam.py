import re
import sqlite3
from openpyxl import Workbook

class TicketOffice:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.booking_data = []

    def display_movies(self):
        self.cursor.execute("SELECT * FROM movie")
        movies = self.cursor.fetchall()
        print("Доступные фильмы:")
        for movie in movies:
            print(f"{movie[0]}. {movie[1]} ({movie[3]})")

    def display_showtimes(self, movie_id):
        self.cursor.execute("SELECT * FROM afisha WHERE movie_id = ?", (movie_id,))
        showtimes = self.cursor.fetchall()
        print("Доступное время сеансов:")
        for showtime in showtimes:
            print(f"{showtime[0]}. {showtime[4]} {showtime[5]}")

    def select_ticket_type(self):
        while True:
            ticket_type = input("Выберите тип билета (взрослый/детский/студенческий): ").lower()
            if ticket_type in ['взрослый', 'детский', 'студенческий']:
                self.booking_data.append(ticket_type)
                return ticket_type
            else:
                print("Неверный тип билета. Пожалуйста, выберите из предложенных вариантов.")

    def validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Неверный формат email. Пожалуйста, введите действительный email.")
            return False
        return True

    def validate_password(self, password):
        if len(password) < 8:
            print("Пароль должен содержать минимум 8 символов.")
            return False
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$", password):
            print("Пароль должен содержать как минимум одну букву, одну цифру и один специальный символ.")
            return False
        return True

    def signup(self):
        email = input("Введите email: ")
        if not self.validate_email(email):
            return False
        pwd = input("Введите пароль: ")
        if not self.validate_password(pwd):
            return False
        conf_pwd = input("Подтвердите пароль: ")
        if conf_pwd == pwd:
            with open("credentials.txt", "a") as f:
                f.write(email + "\n")
                f.write(pwd + "\n")
            print("Регистрация прошла успешно!")
            return True
        else:
            print("Пароли не совпадают.")
            return False

    def login(self):
        email = input("Введите email: ")
        pwd = input("Введите пароль: ")
        with open("credentials.txt", "r") as f:
            lines = f.readlines()
            stored_credentials = [line.strip() for line in lines]
        for i in range(0, len(stored_credentials), 2):
            stored_email = stored_credentials[i]
            stored_pwd = stored_credentials[i + 1]
            if email == stored_email and pwd == stored_pwd:
                print("Вход выполнен успешно!")
                return True
        print("Ошибка входа!")
        return False

    def process_payment(self):
        name = input("Введите имя: ")
    while True:
        card_number = input("Введите номер карты (XXXX XXXX XXXX XXXX): ")
        if re.match(r"^(\d{4}\s){3}\d{4}$", card_number):
            break
        else:
            print("Неверный формат номера карты. Пожалуйста, введите в формате 'XXXX XXXX XXXX XXXX'.")
    
    while True:
        expiry_date = input("Введите срок действия карты (мм/гг): ")
        if re.match(r"^\d{2}/\d{2}$", expiry_date):
            break
        else:
            print("Неверный формат срока действия карты. Пожалуйста, введите в формате 'мм/гг'.")

    cvv = input("Введите CVV код: ")
    # Здесь будет процесс оплаты
    print("Оплата прошла успешно!")

    def book_ticket(self):
        wb = Workbook()
        sheet = wb.active
        sheet.append(["Фильм", "Сеанс", "Тип билета", "Имя", "Номер карты", "Срок действия карты"])

        movie_id = int(input("Выберите фильм по номеру: "))
        self.display_showtimes(movie_id)
        showtime_id = int(input("Выберите время сеанса по номеру: "))
        ticket_type = self.select_ticket_type()

        sheet.append([movie_id, showtime_id, ticket_type])

        self.booking_data.extend([movie_id, showtime_id, ticket_type])
        self.process_payment()
        print("Билет успешно забронирован!")

if __name__ == '__main__':
    ticket_office = TicketOffice()
    logged_in = False
    while not logged_in:
        print("1.Регистрация")
        print("2. Вход")
        choice = input("Выберите действие: ")
        if choice == "1":
            ticket_office.signup()
        elif choice == "2":
            ticket_office.login()
            logged_in = True
        else:
            print("Неверный выбор. Пожалуйста, выберите '1' или '2'.")

    ticket_office.display_movies()
    ticket_office.book_ticket()
