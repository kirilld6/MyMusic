import app

if __name__ == '__main__':
    app.db.create_all()  # создание таблиц базы данных
    app.app.run()  # запуск приложения
