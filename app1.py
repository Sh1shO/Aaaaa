from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QWidget, QTableWidgetItem, QHBoxLayout, QLabel, QLineEdit, QPushButton
from db import get_session, Car, CarModel, Client, Rental

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setGeometry(200,200,800,600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        search_layout = QHBoxLayout()
        search_label = QLabel("Search")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term")
        self.search_input.textChanged.connect(self.search_cars)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.load_cars_data()

    def load_cars_data(self):
        session = get_session()
        self.all_cars = session.query(Car).all()
        print(f"Загружено {len(self.all_cars)} автомобилей")
        self.display_cars(self.all_cars)

    def display_cars(self, cars):
        self.table.setRowCount(len(cars))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Модель", "Номер", "Цвет", 
            "Год выпуска", "Стоимость страховки"
        ])

        for row, car in enumerate(cars):
            self.table.setItem(row, 0, QTableWidgetItem(str(car.id)))
            self.table.setItem(row, 1, QTableWidgetItem(car.fk_model_id.name))
            self.table.setItem(row, 2, QTableWidgetItem(car.number))
            self.table.setItem(row, 3, QTableWidgetItem(car.color))
            self.table.setItem(row, 4, QTableWidgetItem(str(car.release_year)))
            self.table.setItem(row, 5, QTableWidgetItem(str(car.insurence_cost)))

        self.table.resizeColumnsToContents()

    def search_cars(self, search_text):
        print(f"Поиск: {search_text}")
        
        if not search_text:
            self.display_cars(self.all_cars)
            return

        filtered_cars = []
        search_text = search_text.lower()
        
        for car in self.all_cars:
            print(f"Проверка автомобиля: {car.fk_model_id.name} {car.number}")
            if (
                search_text in str(car.id).lower() or
                search_text in car.fk_model_id.name.lower() or
                search_text in car.number.lower() or
                search_text in car.color.lower() or
                search_text in str(car.release_year).lower() or
                search_text in str(car.insurence_cost).lower()
            ):
                filtered_cars.append(car)

        print(f"Найдено {len(filtered_cars)} автомобилей")
        self.display_cars(filtered_cars)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
