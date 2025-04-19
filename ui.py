
import os
import uuid
import joblib
import datetime
import numpy as np
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvas

from PyQt5.QtWidgets import (
    QFrame, QLabel, QPushButton, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QMainWindow, QStyle, QTabBar, QRadioButton, QStyleOptionTab, 
    QLineEdit, QWidget, QFileDialog, QSizePolicy, QGridLayout, 
    QScrollArea, QTextEdit, QDialog, QButtonGroup,
)
from PyQt5.QtGui import QIcon, QPixmap, QFontMetrics
from PyQt5.QtCore import Qt, QSize

from logic import *
from config import *

def apply_theme(self, theme_key:str) -> None:
    '''
    Применяет указанную тему к приложению
            Параметры:
                    theme_key(str): ключ темы
    '''

    theme_style = THEMES[theme_key]
    combined_style = COMMON_STYLES + theme_style
    self.setStyleSheet(combined_style)


class ModelCard(QFrame):
    '''Карточка модели в разделе "Модели"'''

    def __init__(self, model_id, model_data, parent):
        super().__init__()
        self.setObjectName("modelCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.model_id = model_id
        self.model_data = model_data
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        self.setFixedSize(MODEL_CARD_WIDTH, MODEL_CARD_HEIGHT)
        layout = QVBoxLayout(self)

        # Имя модели
        header_layout = QHBoxLayout()
        self.name_label = QLabel(self.model_data["name"])
        self.name_label.setObjectName("modelNameLabel")
        self.name_label.setWordWrap(True)
        header_layout.addWidget(self.name_label)  

        # Добавляем растягивающийся элемент между именем и иконкой
        header_layout.addStretch(1)  

        # Добавляем иконки только для нестандартных моделей

        if self.model_id != STANDARD_MODEL_ID:

            # Изменить имя или описание
            change_name_button = HoverButton(CHANGE_ICON_PATH, CHANGE_ICON_HOVER_PATH)
            change_name_button.setObjectName("changeNameButton")
            change_name_button.setIcon(QIcon(CHANGE_ICON_PATH))
            change_name_button.clicked.connect(self.parent.get_command_change_name(self.model_id))
            header_layout.addWidget(change_name_button)  

            # Удалить модель
            delete_button = HoverButton(TRASH_ICON_PATH, TRASH_ICON_HOVER_PATH)
            delete_button.setObjectName("deleteIconButton")
            delete_button.setIcon(QIcon(TRASH_ICON_PATH))
            delete_button.clicked.connect(self.parent.get_command_delete_button(self.model_id))
            header_layout.addWidget(delete_button)

        layout.addLayout(header_layout)

        # Описание модели
        self.desc_label = QLabel(self.model_data.get("description", DEFAULT_DESCRIPTION))
        self.desc_label.setObjectName("modelDescLabel")
        self.desc_label.setWordWrap(True)
        self.desc_label.setMaximumHeight(50)
        layout.addWidget(self.desc_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10) 

        # Кнопка "Обучить модель"
        train_button = QPushButton(TRAIN_BUTTON_TEXT)
        train_button.setObjectName("trainModelButton")
        train_button.clicked.connect(self.parent.get_command_train_button(self.model_id))
        buttons_layout.addWidget(train_button)

        # Кнопка "Предсказать"
        predict_button = QPushButton(PREDICT_BUTTON_TEXT)
        predict_button.setObjectName("predictModelButton")
        predict_button.clicked.connect(self.parent.get_command_predict(self.model_id))
        buttons_layout.addWidget(predict_button)

        layout.addLayout(buttons_layout)


class ModelTab(QWidget):
    '''Вкладка модели'''

    def __init__(self, model_id, model_data, parent, is_training):
        super().__init__()
        self.model_id = model_id
        self.model_data = model_data
        self.parent = parent
        self.init_params(is_training)

    def init_params(self, is_training=None):
        self.is_training = is_training
        self.is_prediction = not is_training
        if is_training:
            self.training_data = {"epochs": [], "loss":[], "mae": -1, "mse": -1}

    def init_ui(self, predict_year:int=None):
        # Очистка предыдущего layout
        if self.layout() is not None:
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    while item.layout().count():
                        sub_item = item.layout().takeAt(0)
                        if sub_item.widget():
                            sub_item.widget().deleteLater()
        else:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(40, 20, 40, 20)
            self.setLayout(layout)

        layout = self.layout()

        header_layout = QHBoxLayout()

        title_label = QLabel(self.model_data["name"])
        title_label.setObjectName("modelTitleLabel")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        header_layout.setSpacing(5)

        layout.addLayout(header_layout)

        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container) 

        if self.is_training:
            self.show_training_results(content_layout)
        elif self.is_prediction:
            self.show_prediction_results(content_layout, predict_year)

        layout.addWidget(self.content_container)

        layout.addStretch()

    def show_training_results(self, layout):
        '''Показывает график обучения (x - эпоха, y - потери)'''

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        loss_container = QWidget()
        
        content_layout.addWidget(loss_container)

        train_done_label = QLabel(TRAIN_DONE_LABEL_TEXT)
        train_done_label.setObjectName("trainDoneLabel")
        layout.addWidget(train_done_label)

        fig = Figure(dpi=100, facecolor="none")
        ax = fig.add_subplot(111, facecolor="none")
        
        ax.plot(self.training_data["epochs"], self.training_data["loss"], color=WHITE_COLOR_DIAGRAMS)
        ax.set_xlabel("График потерь", color=WHITE_COLOR_DIAGRAMS) 
        ax.tick_params(axis="x", rotation=45, colors=WHITE_COLOR_DIAGRAMS)
        ax.tick_params(axis="y", colors=WHITE_COLOR_DIAGRAMS)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=10))
        
        fig.subplots_adjust(left=0.15, bottom=0.3, right=0.95, top=1)
        
        for spine in ax.spines.values():
            spine.set_color(WHITE_COLOR_DIAGRAMS)
        
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(loss_container.sizeHint().height())
        canvas.setStyleSheet("background-color: transparent;")
        
        content_layout.addWidget(canvas)
        content_layout.addStretch()

        layout.addWidget(content_widget)

        mean_errors_label = QLabel(EVALUATE_RESULT_TEXT.format(self.training_data["mae"], self.training_data["mse"]))
        mean_errors_label.setObjectName("meanErrorsLabel")
        layout.addWidget(mean_errors_label)

        mean_errors_label.setMargin(10)

        save_training_button = QPushButton(SAVE_BUTTON_TEXT)
        save_training_button.setObjectName("SaveTrainingDataButton")

        save_training_button.clicked.connect(self.parent.get_command_save_button(self.model_id))
        layout.addWidget(save_training_button)

    def start_training(self, filename, epochs):
        '''Запускает процесс обучения модели'''

        history, model, evaluate_res, scalers = train_model(self.model_id, filename, epochs, verbose=1)

        self.training_data["loss"] = history.history["loss"]
        self.training_data["epochs"] = [i for i in range(1, epochs+1)] 
        self.training_data["mae"], self.training_data["mse"] = evaluate_res["mae"], evaluate_res["mse"]

        model_path = os.path.join(MODELS_DIRECTORY_PATH, self.model_id + ".keras")
        scaler_X_path = os.path.join(MODELS_DIRECTORY_PATH, "scaler_X" + self.model_id + ".keras")
        scaler_Y_path = os.path.join(MODELS_DIRECTORY_PATH, "scaler_Y" + self.model_id + ".keras")

        if os.path.exists(model_path):
            os.remove(model_path)
        model.save(model_path)
        joblib.dump(scalers["scaler_X"], scaler_X_path)
        joblib.dump(scalers["scaler_Y"], scaler_Y_path)
        
        self.init_ui()

    def show_prediction_results(self, layout, predict_year:int):
        '''Показывает результаты предсказания температуры'''

        model, scaler_X, scaler_Y = get_model(self.model_id)
        if model is None:
            error_label = QLabel(ERROR_LABEL_TEXT)
            error_label.setObjectName("errorLabel")
            layout.addWidget(error_label, alignment=Qt.AlignCenter)
            return
        
        if predict_year == -1:
            # [?] Выделить в отдельную функцию
            for i in range(self.parent.tab_view.count()):
                if i == 0:
                    continue
                tab = self.parent.tab_view.widget(i)
                if tab.model_id == self.model_id:
                    self.parent.close_tab(i)
                    return
            
            return

        test_years = [predict_year] * 12
        test_months = list(range(1, 13))
        test_input = np.column_stack((test_years, test_months))
        test_input_scaled = test_input if scaler_X is None else scaler_X.transform(test_input)
        test_input_scaled = np.array(test_input_scaled, dtype=np.float32)

        predicted_temperature_scaled = model.predict(test_input_scaled, verbose=0)
        predicted_temperature = (
            predicted_temperature_scaled.reshape(12)
            if scaler_Y is None
            else scaler_Y.inverse_transform(predicted_temperature_scaled).reshape(12)
        )

        predict_subtitle = QLabel(PREDICT_WINDOW_SUBTITLE_TEMPLATE.format(predict_year))
        predict_subtitle.setStyleSheet("font-size: 14px; padding: 5px; font-weight: 500;")
        predict_subtitle.setAlignment(Qt.AlignHCenter)
        layout.addWidget(predict_subtitle)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        temp_container = QWidget()
        temp_layout = QVBoxLayout(temp_container)
        temp_layout.setSpacing(5) 
        
        for month, temp in zip(MONTHS_NAME, predicted_temperature):
            month_label = QLabel(f"{month}: {temp:.1f}°C")
            month_label.setObjectName("monthLabel")
            month_label.setFixedHeight(20) 
            temp_layout.addWidget(month_label)
        
        temp_layout.addStretch()
        content_layout.addWidget(temp_container)

        fig = Figure(figsize=(6, 4), dpi=100, facecolor="none")
        ax = fig.add_subplot(111, facecolor="none")
        
        ax.bar(MONTHS_NAME, predicted_temperature, color=WHITE_COLOR_DIAGRAMS, width=0.6)
        ax.set_ylabel(PREDICTED_TEMPERATURE_YLABEL, color=WHITE_COLOR_DIAGRAMS) 
        ax.tick_params(axis="x", rotation=45, colors=WHITE_COLOR_DIAGRAMS)
        ax.tick_params(axis="y", colors=WHITE_COLOR_DIAGRAMS)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=10)) # Количество делений
        
        fig.subplots_adjust(left=0.15, bottom=0.3, right=0.95, top=0.95)
        
        for spine in ax.spines.values():
            spine.set_color(WHITE_COLOR_DIAGRAMS)
        
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(temp_container.sizeHint().height())
        canvas.setStyleSheet("background-color: transparent;")
        
        content_layout.addWidget(canvas)

        layout.addWidget(content_widget)

        save_result_button = QPushButton(SAVE_RESULT_BUTTON)
        save_result_button.setObjectName("save_result_button")

        def save_result():
            path, _ = QFileDialog.getSaveFileName(None, SAVE_RESULT_WINDOW_TITLE, ".", "Txt/Csv (*.txt, *.csv)")

            if path:
                if (not str.endswith(path, ".txt")) and (not str.endswith(path, ".csv")):
                    new_filename += ".txt"

                with open(path,'w') as f:
                    f.write('Месяц;Температура\n')
                    for month in range(0, 12):
                        transfer = "" if month == 12 else "\n"
                        f.write(f'{MONTHS_NAME[month]};{predicted_temperature[month]:.3f}{transfer}')

        save_result_button.clicked.connect(save_result)

        layout.addWidget(save_result_button)

    def open_year_dialog(self):
        '''Открывает диалог для выбора года.
           Возвращает выбранный год'''

        dialog = YearInputDialog(self)
        dialog.setStyleSheet(self.parent.current_theme_style)
        self.parent.open_dialogs.append(dialog)
        dialog.finished.connect(lambda: self.parent.open_dialogs.remove(dialog))
        if dialog.exec():
            year = dialog.textValue()
            if year.isdigit():
                return year

            
        return -1


class ResizableApp(QMainWindow):
    # [?] Надо выделить отдельное ResizableApp и окно с перетаскивание, потому что другие диалоги тоже с перетаскиванием работают 
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_WINDOW_TITLE)
        self.setGeometry(0, 0, WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint)

        border_widget = QWidget()
        border_widget.setObjectName("borderWidget")
        self.border_layout = QVBoxLayout(border_widget)
        self.border_layout.setContentsMargins(2, 2, 2, 2)

        self.border_widget = border_widget

        self.old_pos = None
        self.resize_direction = 0
        self.is_resizing = False
        self.resize_margin = RESIZE_MARGIN
        self.min_width = WINDOW_MIN_WIDTH
        self.min_height = WINDOW_MIN_HEIGHT

        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 5, 20, 5)

        title_label = QLabel(APP_WINDOW_TITLE)
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        minimize_button = QPushButton("━")
        minimize_button.setObjectName("minimizeButton")
        minimize_button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        minimize_button.clicked.connect(self.showMinimized)
        header_layout.addWidget(minimize_button)

        close_button = QPushButton("Х")
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        close_button.clicked.connect(self.close)
        header_layout.addWidget(close_button)

        self.border_layout.addWidget(header_widget)

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        '''
        Нажатие мыши для перемещения или изменения размера
        '''

        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
            pos = event.pos()
            left = pos.x() <= self.resize_margin
            right = pos.x() >= self.width() - self.resize_margin
            top = pos.y() <= self.resize_margin
            bottom = pos.y() >= self.height() - self.resize_margin

            if left and top:
                self.resize_direction = 5
            elif right and top:
                self.resize_direction = 6
            elif left and bottom:
                self.resize_direction = 7
            elif right and bottom:
                self.resize_direction = 8
            elif left:
                self.resize_direction = 1
            elif right:
                self.resize_direction = 2
            elif top:
                self.resize_direction = 3
            elif bottom:
                self.resize_direction = 4
            else:
                self.resize_direction = 0

            self.is_resizing = self.resize_direction != 0

    def mouseMoveEvent(self, event):
        '''
        Перемещение мыши для изменения размера или перемещения окна
        '''

        pos = event.pos()
        left = pos.x() <= self.resize_margin
        right = pos.x() >= self.width() - self.resize_margin
        top = pos.y() <= self.resize_margin
        bottom = pos.y() >= self.height() - self.resize_margin

        if (left and top) or (right and bottom):
            self.setCursor(Qt.SizeFDiagCursor)
        elif (right and top) or (left and bottom):
            self.setCursor(Qt.SizeBDiagCursor)
        elif left or right:
            self.setCursor(Qt.SizeHorCursor)
        elif top or bottom:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            if self.is_resizing:
                x, y, w, h = self.x(), self.y(), self.width(), self.height()
                if self.resize_direction == 1:
                    new_width = max(self.min_width, w - delta.x())
                    self.setGeometry(x + delta.x(), y, new_width, h)
                elif self.resize_direction == 2:
                    new_width = max(self.min_width, w + delta.x())
                    self.resize(new_width, h)
                elif self.resize_direction == 3:
                    new_height = max(self.min_height, h - delta.y())
                    self.setGeometry(x, y + delta.y(), w, new_height)
                elif self.resize_direction == 4:
                    new_height = max(self.min_height, h + delta.y())
                    self.resize(w, new_height)
                elif self.resize_direction == 5:
                    new_width = max(self.min_width, w - delta.x())
                    new_height = max(self.min_height, h - delta.y())
                    self.setGeometry(x + delta.x(), y + delta.y(), new_width, new_height)
                elif self.resize_direction == 6:
                    new_width = max(self.min_width, w + delta.x())
                    new_height = max(self.min_height, h - delta.y())
                    self.setGeometry(x, y + delta.y(), w, new_height)
                elif self.resize_direction == 7:
                    new_width = max(self.min_width, w - delta.x())
                    new_height = max(self.min_height, h + delta.y())
                    self.setGeometry(x + delta.x(), y, new_width, new_height)
                elif self.resize_direction == 8:
                    new_width = max(self.min_width, w + delta.x())
                    new_height = max(self.min_height, h + delta.y())
                    self.resize(new_width, new_height)
            else:
                self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        '''
        [?] Лишний параметр?
        Обрабатывает отпускание мыши для завершения перемещения или изменения размера
        '''
        self.old_pos = None
        self.is_resizing = False
        self.resize_direction = 0
        self.setCursor(Qt.ArrowCursor)


class HoverButton(QPushButton):
    '''Кнопка, которая изменяет иконку при наведении'''

    def __init__(self, normal_icon_path, hover_icon_path, parent=None):
        super().__init__(parent)
        self.normal_icon_path = normal_icon_path
        self.hover_icon_path = hover_icon_path
        self.setIcon(QIcon(self.normal_icon_path))

    def enterEvent(self, event):
        self.setIcon(QIcon(self.hover_icon_path))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(QIcon(self.normal_icon_path))
        super().leaveEvent(event)


class MovableDialog(QDialog):
    '''Свой класс для диалогов, в которых можно перетаскивать файлы мышью'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.old_pos = None

    def mousePressEvent(self, event):
        '''Начало перемещения'''
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        '''Перемещение'''

        if self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        '''Отпускание мыши'''
        self.old_pos = None


class TrainDialog(MovableDialog):
    '''Диалог обученя модели'''

    def __init__(self, parent, model_id):
        super().__init__(parent)
        self.model_id = model_id
        self.setWindowTitle(TRAIN_MODE_WINDOW_TITLE)
        self.setFixedSize(380, 290)
        self.init_ui()
        if parent and hasattr(parent, "current_theme_style"):
            self.setStyleSheet(parent.current_theme_style)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Шапка
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("Обучение модели")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        close_button = QPushButton("Х")
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(self.reject)
        header_layout.addWidget(close_button)

        main_layout.addWidget(header_widget)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # Предупреждение
        self.warning_label = QLabel(TRAIN_MODE_QUESTION)
        self.warning_label.setObjectName("dialogLabel")
        self.warning_label.setWordWrap(True)
        content_layout.addWidget(self.warning_label)

        # Выбор вариантов
        self.mode_group = QButtonGroup(self)
        standard_radio = QRadioButton(STANDARD_TRAIN_MODE_TITLE)
        standard_radio.setObjectName("trainModeRadio")

        file_radio = QRadioButton(FILE_TRAIN_MODE_TITLE)
        file_radio.setObjectName("trainModeRadio")
        self.mode_group.addButton(standard_radio, 1)
        self.mode_group.addButton(file_radio, 2)
        standard_radio.setChecked(True)

        content_layout.addWidget(standard_radio)
        content_layout.addWidget(file_radio)

        # Ввод количества эпох
        epochs_layout = QHBoxLayout()
        epochs_label = QLabel(EPOCH_INPUT_TITLE)
        epochs_label.setObjectName("epochsLabel")
        self.epochs_input = QLineEdit(str(EPOCHS_DEFAULT_VALUE))
        self.epochs_input.setObjectName("epochsInput")
        epochs_layout.addWidget(epochs_label)
        epochs_layout.addWidget(self.epochs_input)
        content_layout.addLayout(epochs_layout)
        content_layout.setSpacing(10)

        self.start_button = QPushButton(START_TRAIN_BUTTON_TEXT)
        self.start_button.setObjectName("startTrainButton")
        self.start_button.clicked.connect(self.push_train_button)
        content_layout.addWidget(self.start_button)

        content_layout.addStretch()
        main_layout.addWidget(content_widget)

    def push_train_button(self):
        '''Запускает процесс обучения модели после нажатия на кнопку'''

        mode = self.mode_group.checkedId()
        filename = STANDARD_TRAIN_DATA_PATH if mode == 1 else None

        if mode == 2:
            file_dialog = OpenModelDialog(self)
            file_dialog.setWindowTitle(TRAIN_FILE_WINDOW_TITLE)
            file_dialog.setNameFilter("Text or CSV (*.txt *.csv);;All Files (*)")
            file_dialog.setStyleSheet(self.parent().current_theme_style)
            self.parent().open_dialogs.append(file_dialog)
            file_dialog.finished.connect(lambda: self.parent().open_dialogs.remove(file_dialog))
            if file_dialog.exec():
                filename = file_dialog.selectedFiles()[0]
        if not filename:
            self.reject()
            return

        for i in range(self.parent().tab_view.count()):
            if i == 0:
                continue
            tab = self.parent().tab_view.widget(i)
            if tab.model_id == self.model_id:
                tab.start_training(filename, int(self.epochs_input.text()) if self.epochs_input.text().isdigit() else 200)
                break
        self.accept()


class CustomInputDialog(MovableDialog):
    '''Диалог добавления модели и используется как основа формы ввода года предсказания '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.old_pos = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 10)
        main_layout.setSpacing(0)

        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 10, 0)
        header_layout.setSpacing(0)

        self.title_label = QLabel("Введите данные")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setContentsMargins(20, 10, 0, 10)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        close_button = QPushButton("Х")
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        close_button.clicked.connect(self.reject)
        header_layout.addWidget(close_button)

        main_layout.addWidget(header_widget)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # Имя модели
        self.label = QLabel("")
        self.label.setObjectName("dialogLabel")
        content_layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setObjectName("dialogInput")
        self.input_field.setPlaceholderText(ADD_MODEL_NAME_PLACEHOLDER)
        content_layout.addWidget(self.input_field)

        # Описание модели
        self.desc_label = QLabel(ADD_MODEL_DESCRIPTION_TITLE)
        self.desc_label.setObjectName("dialogLabel")
        content_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setObjectName("dialogDescInput")
        self.desc_input.setPlaceholderText(ADD_MODEL_DESCRIPTION_PLACEHOLDER)
        self.desc_input.setMaximumHeight(100)
        content_layout.addWidget(self.desc_input)

        # Кнопки "Ок" и "Отмена"
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        ok_button = QPushButton(OK_BUTTON_TEXT)
        ok_button.setObjectName("dialogOkButton")
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton(CANCEL_BUTTON_TEXT)
        cancel_button.setObjectName("dialogCancelButton")
        cancel_button.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addStretch()
        content_layout.addLayout(buttons_layout)

        main_layout.addWidget(content_widget)
        self.adjustSize()

    def setWindowTitle(self, title):
        super().setWindowTitle(title)
        self.title_label.setText(title)

    def setLabelText(self, text):
        self.label.setText(text)

    def setTextValue(self, text):
        self.input_field.setText(text)

    def textValue(self):
        return self.input_field.text()

    def setDescValue(self, text):
        self.desc_input.setPlainText(text)

    def descValue(self):
        return self.desc_input.toPlainText()


class YearInputDialog(CustomInputDialog):
    '''Диалог для ввода года'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор года")
        self.setFixedSize(300, 170)
        self.init_ui()

    def init_ui(self):
        # Очищаем существующую компоновку, чтобы избежать конфликта
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 10)
        main_layout.setSpacing(0)

        # Кастомная шапка
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 10, 0)
        header_layout.setSpacing(0)

        self.title_label = QLabel(INPUT_YEAR_WINDOW_TITLE)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setContentsMargins(20, 10, 0, 10)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        close_button = QPushButton("Х")
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        close_button.clicked.connect(self.reject)
        header_layout.addWidget(close_button)

        main_layout.addWidget(header_widget)

        # Основное содержимое
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel(INPUT_YEAR_TITLE.
                        format(INPUT_YEAR_VALUE_FROM, INPUT_YEAR_VALUE_TO))
        self.label.setObjectName("dialogLabel")

        content_layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setObjectName("dialogInput")
        self.input_field.setPlaceholderText(INPUT_YEAR_PLACEHOLDER)
        content_layout.addWidget(self.input_field)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        ok_button = QPushButton("ОК")
        ok_button.setObjectName("dialogOkButton")
        ok_button.clicked.connect(self.push_OK)

        cancel_button = QPushButton("Отмена")
        cancel_button.setObjectName("dialogCancelButton")
        cancel_button.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addStretch()
        content_layout.addLayout(buttons_layout)

        main_layout.addWidget(content_widget)
        self.adjustSize()

    def push_OK(self):
        year = self.input_field.text()
        if year.isdigit() and int(year) >= INPUT_YEAR_VALUE_FROM and int(year) <= INPUT_YEAR_VALUE_TO:
            self.accept()


class OpenModelDialog(QFileDialog):
    '''Диалог выбора модели'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setNameFilter("Keras Model (*.keras);;All Files (*)")
        self.setWindowTitle(ADD_MODEL_WINDOW_TITLE)

    def mousePressEvent(self, event):
        '''Обрабатывает нажатие мыши для начала перемещения'''

        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        '''Обрабатывает перемещение мыши для перемещения окна'''

        if hasattr(self, 'old_pos') and self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        '''Обрабатывает отпускание мыши для завершения перемещения'''
        self.old_pos = None


class CustomTabBar(QTabBar):
    '''Панель вкладок с изменяющейся шириной табов'''

    def tabSizeHint(self, index):
        '''Вычисляет размер вкладки'''

        text = self.tabText(index)
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.horizontalAdvance(text)
        text_width += 10
        padding = 18
        close_button_width = 0
        if self.tabsClosable() and index > 0:
            opt = QStyleOptionTab()
            self.initStyleOption(opt, index)
            close_button_width = self.style().pixelMetric(
                QStyle.PM_TabCloseIndicatorWidth, opt, self
            )
            close_button_width += 24
        total_width = text_width + padding + close_button_width
        total_width += 20
        height = super().tabSizeHint(index).height()
        return QSize(total_width, height)

    def minimumTabSizeHint(self, index):
        '''Возвращает минимальный размер вкладки. Переопределение'''
        
        return self.tabSizeHint(index)

    def tabButton(self, index, position):
        '''Отключает кнопку закрытия для вкладки с индексом 0. Переопределение'''

        if index == 0 and position == QTabBar.RightSide:
            return None
        return super().tabButton(index, position)


class App(ResizableApp):

    def __init__(self):
        super().__init__()

        self.current_theme = "misty_sunrise"
        self.current_theme_style = None
        self.open_dialogs = []

        self.setMaximumSize(WINDOW_MAX_WIDTH, WINDOW_MAX_HEIGHT)

        self.update_background()

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        self.sidebar_frame.setFixedWidth(SIDEBAR_WIDTH)
        sidebar_layout = QVBoxLayout(self.sidebar_frame)

        # Лого
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setSpacing(10) 
        logo_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        logo_pixmap = QPixmap(LOGO_IMAGE_PATH).scaled(
            LOGO_SIZE, LOGO_SIZE, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.logo = QLabel()
        self.logo.setPixmap(logo_pixmap)
        self.logo.setAlignment(Qt.AlignHCenter) 
        self.logo.setFixedSize(LOGO_SIZE, LOGO_SIZE) 

        logo_layout.addWidget(self.logo)
        sidebar_layout.addWidget(
            logo_container, 
            alignment=Qt.AlignHCenter | Qt.AlignTop
        )

        # Погода за текущий месяц
        self.weather_summary_label = QLabel(LOADING_LABEL_TEMPLATE)
        self.weather_summary_label.setStyleSheet("font-size: 14px; padding: 5px; font-weight: 500;")
        self.weather_summary_label.setWordWrap(True)
        self.weather_summary_label.setAlignment(Qt.AlignHCenter)
        sidebar_layout.addWidget(self.weather_summary_label)

        temp_container = QWidget()
        temp_layout = QHBoxLayout(temp_container)
        temp_layout.setAlignment(Qt.AlignCenter)
        temp_layout.setContentsMargins(0, 0, 0, 0)
        temp_layout.setSpacing(10)

        # Иконка температуры
        self.temp_icon = QLabel()
        temp_icon_pixmap = QPixmap(TEMPERATURE_ICON_PATH).scaled(
            TEMP_ICON_SIZE, TEMP_ICON_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.temp_icon.setPixmap(temp_icon_pixmap)
        self.temp_icon.setAlignment(Qt.AlignCenter)
        temp_layout.addWidget(self.temp_icon)

        # Сама сводка о температуре
        self.temp_value_label = QLabel("0.0°C")
        self.temp_value_label.setObjectName("tempValueLabel")
        self.temp_value_label.setAlignment(Qt.AlignCenter)
        temp_layout.addWidget(self.temp_value_label)

        sidebar_layout.addWidget(temp_container, alignment=Qt.AlignCenter)
        sidebar_layout.addStretch()

        # Карусель тем
        self.theme_label = QLabel("Тема")
        self.theme_label.setObjectName("themeLabel")
        self.theme_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.theme_label, alignment=Qt.AlignCenter)

        theme_carousel_widget = QWidget()
        theme_carousel_layout = QHBoxLayout(theme_carousel_widget)
        theme_carousel_layout.setContentsMargins(0, 0, 0, 0)
        theme_carousel_layout.setSpacing(5)

        self.prev_theme_button = QPushButton("◄")
        self.prev_theme_button.setObjectName("prevThemeButton")
        self.prev_theme_button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.prev_theme_button.clicked.connect(self.prev_theme)
        theme_carousel_layout.addWidget(self.prev_theme_button)

        theme_name_container = QWidget()
        theme_name_container.setObjectName("themeNameContainer")
        name_layout = QVBoxLayout(theme_name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setAlignment(Qt.AlignCenter) 

        self.theme_name_label = QLabel(THEMES[self.current_theme][0])
        self.theme_name_label.setObjectName("themeNameLabel")
        self.theme_name_label.setAlignment(Qt.AlignCenter)
        self.theme_name_label.setWordWrap(True)
        theme_carousel_layout.addWidget(self.theme_name_label)

        theme_carousel_layout.addWidget(theme_name_container)

        self.next_theme_button = QPushButton("►")
        self.next_theme_button.setObjectName("nextThemeButton")
        self.next_theme_button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.next_theme_button.clicked.connect(self.next_theme)
        theme_carousel_layout.addWidget(self.next_theme_button)

        sidebar_layout.addWidget(theme_carousel_widget, alignment=Qt.AlignCenter)

        content_layout.addWidget(self.sidebar_frame)

        # Вкладки
        self.tab_view = QTabWidget()
        self.tab_view.setTabBar(CustomTabBar())
        self.tab_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setTabBarAutoHide(False)
        self.tab_view.tabCloseRequested.connect(self.close_tab)
        self.tab_view.tabBar().setUsesScrollButtons(True)
        self.tab_view.tabBar().setElideMode(Qt.ElideNone)
        content_layout.addWidget(self.tab_view)

        # Устанавливаем минимальную ширину для вкладки "Модели"
        min_tab_width = (MODEL_CARD_WIDTH * 3) + 90
        self.tab_view.setMinimumWidth(min_tab_width)

        # Вкладка "Модели"
        models_tab = QWidget()
        models_tab.setObjectName("modelsTab")
        models_layout = QVBoxLayout(models_tab)
        models_layout.setContentsMargins(0, 0, 0, 0)

        # Карточки моделей
        self.cards_widget = QWidget()
        self.cards_widget.setObjectName("cardsWidget")
        self.cards_layout = QGridLayout(self.cards_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.cards_widget)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        models_layout.addWidget(self.scroll_area)

        # Кнопка "Добавить модель"
        self.add_model_button = QPushButton(LOAD_MODEL_WINDOW_TITLE)
        self.add_model_button.setObjectName("addModelButton")
        self.add_model_button.clicked.connect(self.add_model)
        models_layout.addWidget(self.add_model_button)

        self.tab_view.addTab(models_tab, MODELS_TAB_NAME)
        self.tab_view.setTabEnabled(0, True)
        self.tab_view.tabBar().setTabButton(0, QTabBar.RightSide, None)

        self.border_layout.addWidget(content_widget)
        main_layout.addWidget(self.border_widget)

        # Добавляем старым моделям описание по умолчанию, если его не было
        self.models = get_models()
        for model_id, model_data in self.models.items():
            if model_id != STANDARD_MODEL_ID and "description" not in model_data:
                model_data["description"] = DEFAULT_DESCRIPTION
        save_models_metadata(self.models)

        self.current_theme = "misty_sunrise"
        self.update_background()
        self.draw_models_cards()
        self.update_weather_summary()

    def update_weather_summary(self):
        '''
        Обновляет температуру на боковой панели
        '''

        current_month = datetime.datetime.now().month
        model, scaler_X, scaler_Y = get_model(STANDARD_MODEL_ID)
        if model is None:
            self.weather_summary_label.setText(
                WEATHER_SUMMARY_CANT_DISPLAY
            )
            self.temp_value_label.setText("N/A")
            return

        test_year = 2025
        test_input = np.array([[test_year, current_month]], dtype=np.float32)
        test_input_scaled = test_input if scaler_X is None else scaler_X.transform(test_input)
        predicted_temperature_scaled = model.predict(test_input_scaled, verbose=0)
        predicted_temperature = (
            predicted_temperature_scaled[0][0]
            if scaler_Y is None
            else scaler_Y.inverse_transform(predicted_temperature_scaled)[0][0]
        )

        month_name = MONTHS_NAME[current_month - 1]
        self.weather_summary_label.setText(
            WEATHER_SUMMARY_LABEL_TEMPLATE.format(month_name)
        )
        self.temp_value_label.setText(f"{predicted_temperature:.1f}°C")

    def update_background(self):
        '''Обновляет фон и применяет текущую тему'''

        theme_style = THEMES.get(self.current_theme, THEMES["pink_dawn"])[1]
        self.current_theme_style = COMMON_STYLES + theme_style  # Объединяем стили
        self.setStyleSheet(self.current_theme_style)

        # Применяем объединённые стили ко всем открытым диалогам
        for dialog in self.open_dialogs:
            if dialog.isVisible():
                dialog.setStyleSheet(self.current_theme_style)

    def prev_theme(self):
        themes = list(THEMES.keys())
        current_index = themes.index(self.current_theme)
        next_index = (current_index - 1) % len(themes)
        self.current_theme = themes[next_index]
        self.theme_name_label.setText(THEMES[self.current_theme][0])
        self.update_background()
        self.draw_models_cards()

    def next_theme(self):
        themes = list(THEMES.keys())
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.current_theme = themes[next_index]
        self.theme_name_label.setText(THEMES[self.current_theme][0])
        self.update_background()
        self.draw_models_cards()

    def draw_models_cards(self):
        '''Рисует карточки'''

        # Удаляем все карточки
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Вычисляем динамические отступы
        container_width = self.width() 
        container_height = self.height() 
        num_cols = 3  # [?] Возможно стоит сделать количество колонок динамическим
        num_rows = (len(self.models) + num_cols - 1) // num_cols

        spacing = min(container_width // (num_cols + 1), container_height // (num_rows + 1)) // 5 # Считаем отступы
        spacing = max(5, min(spacing, 20))  # Отступы будут от 5 до 20 пикселей

        self.cards_layout.setHorizontalSpacing(spacing)
        self.cards_layout.setVerticalSpacing(spacing)
        self.cards_layout.setContentsMargins(spacing, spacing, spacing, spacing)

        for row, (model_id, model_data) in enumerate(self.models.items()):
            card = ModelCard(model_id, model_data, self)
            col = row % num_cols
            row = row // num_cols
            self.cards_layout.addWidget(card, row, col)

    def open_model_tab(self, model_id, is_training=True):
        '''Открывает вкладку модели'''

        def open_tab():

            # Если открыта вкладка, то просто обновляем параметры
            for i in range(self.tab_view.count()):
                if i == 0:
                    continue
                tab = self.tab_view.widget(i)
                if tab.model_id == model_id:
                    tab.init_params(is_training)
                    self.tab_view.setCurrentIndex(i)
                    return

            # Если нет, то создаем новую вкладку
            tab = ModelTab(model_id, self.models[model_id], self, is_training)
            self.tab_view.addTab(tab, self.models[model_id]["name"])
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)

        return open_tab

    def close_tab(self, index):
        '''Закрывает вкладку'''

        if index != 0:
            self.tab_view.removeTab(index)

    def get_command_change_name(self, model_id):
        '''Возвращает команду для изменения имени модели'''

        def push_change_name():
            dialog = CustomInputDialog(self)
            dialog.setWindowTitle(CHANGE_NAME_WINDOW_TITLE)
            dialog.setLabelText(CHANGE_NAME_WINDOW_TEXT)
            dialog.setTextValue(self.models[model_id]["name"])
            dialog.setDescValue(self.models[model_id]["description"])
            dialog.setStyleSheet(self.current_theme_style)
            self.open_dialogs.append(dialog)
            dialog.finished.connect(lambda: self.open_dialogs.remove(dialog))

            if dialog.exec():
                new_name = dialog.textValue()
                new_desc = dialog.descValue()
                if new_name:
                    self.models[model_id]["name"] = new_name
                    self.models[model_id]["description"] = new_desc if new_desc else DEFAULT_DESCRIPTION
                    self.draw_models_cards()
                    for i in range(self.tab_view.count()):
                        if i == 0:
                            continue
                        tab = self.tab_view.widget(i)
                        if tab.model_id == model_id:
                            self.tab_view.setTabText(i, new_name)
                            tab.model_data["name"] = new_name
                            tab.model_data["description"] = new_desc if new_desc else DEFAULT_DESCRIPTION
                            tab.init_ui()
                            break
                    save_models_metadata(self.models)

        return push_change_name

    def get_command_train_button(self, model_id):
        '''Возвращает команду для запуска обучения модели'''

        def push_train():
            self.open_model_tab(model_id)()
            dialog = TrainDialog(self, model_id)
            self.open_dialogs.append(dialog)
            dialog.finished.connect(lambda: self.open_dialogs.remove(dialog))
            if not dialog.exec_():
                # [?] Выделить в отдельную функцию
                for i in range(self.tab_view.count()):
                    if i == 0:
                        continue
                    tab = self.tab_view.widget(i)
                    if tab.model_id == model_id:
                        self.close_tab(i)
                        return

        return push_train

    def get_command_predict(self, model_id):
        '''Возвращает команду для предсказания по модели'''

        def predict():

            self.open_model_tab(model_id, False)()
            for i in range(self.tab_view.count()):
                if i == 0:
                    continue
                tab = self.tab_view.widget(i)
                if tab.model_id == model_id:
                    year = tab.open_year_dialog()
                    tab.init_ui(year)
                    break

        return predict

    def get_command_delete_button(self, model_id):
        '''Возвращает команду для удаления модели'''

        def push_delete():
            del self.models[model_id]
            for path in [
                os.path.join(MODELS_DIRECTORY_PATH, model_id + ".keras"),
                os.path.join(MODELS_DIRECTORY_PATH, "scaler_X" + model_id + ".keras"),
                os.path.join(MODELS_DIRECTORY_PATH, "scaler_Y" + model_id + ".keras"),
            ]:
                if os.path.exists(path):
                    os.remove(path)

            for i in range(self.tab_view.count()):
                if i == 0:
                    continue
                tab = self.tab_view.widget(i)
                if tab.model_id == model_id:
                    self.tab_view.removeTab(i)
                    break

            self.draw_models_cards()
            save_models_metadata(self.models)

        return push_delete
    
    def get_command_save_button(self, model_id):

        '''
        Возвращает функцию, которая открывает диалог сохранения модели
                Параметры:
                        model_id: модель, которую нужно будет сохранить по нажатию на кнопку
                Возвращаемое значение:
                        push_save_model (function): функция
        '''

        def push_save_model():

            path, _ = QFileDialog.getSaveFileName(None, SAVE_MODEL_WINDOW_TITLE, ".", "models (*.keras);;All Files (*)")

            if path:
                model, scaler_X, scaler_Y = get_model(model_id)

                dirname, fname = os.path.split(path)

                if not str.endswith(fname, ".keras"):
                    fname += ".keras"
                model.save(os.path.join(dirname, fname))   
                joblib.dump(scaler_X, os.path.join(dirname, "Scaler_X" + fname))   
                joblib.dump(scaler_Y, os.path.join(dirname, "Scaler_Y" + fname))        
        
        return push_save_model

    def add_model(self):
        '''Добавляет новую модель через выбор файла'''

        file_dialog = OpenModelDialog(self)
        file_dialog.setStyleSheet(self.current_theme_style)  # Применяем текущую тему

        if file_dialog.exec():  # Открываем диалог и ждём выбора
            filename = file_dialog.selectedFiles()[0]
            if filename:
                try:
                    # Загружаем модель
                    model = load_model(filename)
                    new_id = str(uuid.uuid4())
                    model.save(os.path.join(MODELS_DIRECTORY_PATH, new_id + ".keras"))

                    # Запрашиваем имя модели
                    name_dialog = CustomInputDialog(self)
                    name_dialog.setWindowTitle(ADD_MODEL_WINDOW_TITLE)
                    name_dialog.setLabelText(ADD_MODEL_NAME_TITLE)
                    name_dialog.setStyleSheet(self.current_theme_style)

                    if name_dialog.exec():
                        new_name = name_dialog.textValue() or DEFAULT_MODEL_NAME
                        new_desc = name_dialog.descValue() or DEFAULT_DESCRIPTION
                    else:
                        return

                    # Сохраняем модель в словаре
                    self.models[new_id] = {
                        "name": new_name, 
                        "description": new_desc
                    }

                    self.draw_models_cards()
                    save_models_metadata(self.models)

                except Exception as e:
                    print(f"Ошибка при загрузке модели: {e}")
