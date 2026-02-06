from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog,
    QTabWidget, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("SVN Sync Tool")
        self.resize(900, 600)

        self.init_ui()
        self.load_revision_info()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()

        # Пути
        self.main_path_edit = QLineEdit()
        self.out_path_edit = QLineEdit()

        main_btn = QPushButton("Обзор MAIN")
        main_btn.clicked.connect(self.select_main)

        out_btn = QPushButton("Обзор OUTSOURCE")
        out_btn.clicked.connect(self.select_out)

        layout.addWidget(QLabel("Рабочая копия MAIN"))
        layout.addWidget(self.main_path_edit)
        layout.addWidget(main_btn)

        layout.addWidget(QLabel("Рабочая копия OUTSOURCE"))
        layout.addWidget(self.out_path_edit)
        layout.addWidget(out_btn)

        # Ревизии
        self.rev_label = QLabel("")
        layout.addWidget(self.rev_label)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(QWidget(), "Без конфликтов")
        self.tabs.addTab(QWidget(), "Конфликты")
        layout.addWidget(self.tabs)

        # Commit message
        layout.addWidget(QLabel("Сообщение для коммита"))
        self.commit_edit = QTextEdit()
        layout.addWidget(self.commit_edit)

        # Кнопки
        self.scan_btn = QPushButton("Проверить изменения")
        layout.addWidget(self.scan_btn)

        self.apply_btn = QPushButton("Применить изменения")
        layout.addWidget(self.apply_btn)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def select_main(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите рабочую копию MAIN")
        if path:
            self.main_path_edit.setText(path)

    def select_out(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите рабочую копию OUTSOURCE")
        if path:
            self.out_path_edit.setText(path)

    def load_revision_info(self):
        try:
            main_rev, out_rev = self.controller.get_head_info()
            self.rev_label.setText(
                f"MAIN: r{main_rev} | OUTSOURCE: r{out_rev}"
            )
        except Exception:
            self.rev_label.setText("Не удалось получить ревизии.")
