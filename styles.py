
COMMON_STYLES = """
/* ==========================================================================
   Общие стили для всего приложения
   ========================================================================== */
QWidget#centralWidget,
QWidget#borderWidget,
QWidget#cardsWidget,
QWidget#modelsTab,
QScrollArea {
    background-color: transparent;
}

QMessageBox,
QLabel#epochsLabel,
QLabel#errorLabel,
QLabel#themeLabel,
QLabel#tempValueLabel,
TrainDialog QLineEdit#epochsInput,
TrainDialog QButtonGroup#trainModeRadio,
TrainDialog QRadioButton#trainModeRadio,
ErrorDialog QLabel#dialogLabel,
CustomInputDialog QLabel#dialogLabel {
    font-weight: 500;
}

/* Стили для вертикальной полосы прокрутки */
QScrollBar:vertical {
    width: 10px;  
    border-top-right-radius: 5px; 
}

QScrollBar::handle:vertical {
    border-radius: 5px;  
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;  /* Убираем стрелки */
    background: none;
    border-top-right-radius: 5px; 
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    border-top-right-radius: 5px;
}

/* ==========================================================================
   Стили для окна
   ========================================================================== */
/* Шапка в главном окне */
QMainWindow QWidget#headerWidget {
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

/* Шапка в диалоговых окнах */
QDialog QWidget#headerWidget {
    border-top-left-radius: 10px; 
    border-top-right-radius: 10px;
}

QWidget#borderWidget {
    border: 2px solid; /* Цвет границы будет задан в темах */
}

/* ==========================================================================
   Стили для боковой панели
   ========================================================================== */
QFrame#sidebarFrame {
    border: none;
    border-radius: 10px;
    margin: 5px;
}

/* ==========================================================================
   Стили для вкладок
   ========================================================================== */
QTabBar {
   border: none;
}

QTabWidget::pane {
    border: 1px solid; /* Цвет границы будет задан в темах */
    border-top-right-radius: 10px; 
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}

QTabBar::tab {
    padding: 8px 10px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 2px;
    font-size: 14px;
    font-weight: 500;
    min-width: 0;
    max-width: none;
    color: #E0E7FF; /* Единый цвет текста для вкладок */
}

QTabBar::tab:selected {
    border-bottom: 3px solid; /* Цвет будет задан в темах */
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}

/* ==========================================================================
   Стили для кнопок
   ========================================================================== */
QPushButton {
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #E0E7FF; /* Единый цвет текста для кнопок */
}

QPushButton#startTrainButton,
QPushButton#addModelButton {
    padding: 8px;
}

QPushButton#themeToggleButton,
QPushButton#changeNameButton,
QPushButton#deleteIconButton {
    background: transparent;
    border: none;
    padding: 1px;
    icon-size: 25px;
}

QPushButton#prevThemeButton,
QPushButton#nextThemeButton,
QTabBar QToolButton {
    font-size: 16px;
    padding: 5px;
    border: none;
    border-radius: 5px;
    color: #E0E7FF;
    width: 20px;
    height: 20px;
}

QPushButton#minimizeButton,
QPushButton#maximizeButton,
QPushButton#closeButton {
    background: transparent;
    border: none;
    padding: 5px;
    font-size: 14px;
    font-weight: 600;
    border-radius: 5px;
    color: #E0E7FF;
}

QPushButton:disabled {
    color: #E0E7FF;
}

QPushButton#predictModelButton,
QPushButton#trainModelButton {
    font-size: 12px;
    padding: 10px;
}

/* ==========================================================================
   Стили для меток
   ========================================================================== */
QLabel {
    font-size: 14px;
    font-weight: 400;
    color: #E0E7FF;
}

QLabel#titleLabel {
    font-size: 16px;
    font-weight: 600;
}

QLabel#themeLabel {
    font-size: 14px;
}

QLabel#tempValueLabel {
    font-size: 24px;
    font-weight: 600;
}

QLabel#modelNameLabel {
    font-size: 16px;
    font-weight: 500;
}

QLabel#modelTitleLabel {
    font-size: 20px;
    font-weight: 600;
}

QLabel#modelSubtitleLabel {
    font-size: 16px;
    font-weight: 500;
}

QLabel#monthLabel {
    font-size: 14px;
    font-weight: bold;
}

QLabel#untrainedLabel {
    font-size: 20px;  
    font-weight: 400;
    text-align: center;
    max-width: 600px; 
    margin: 0 auto;
}

QLabel#errorLabel {
    font-size: 16px;
    color: #E0E7FF;
}

QLabel#progressLabel {
    font-size: 16px;
    font-weight: 400;
}

QLabel#savingLabel {
    font-size: 16px;
    font-style: italic;
}

/* ==========================================================================
   Стили для карточек моделей
   ========================================================================== */
QFrame#modelCard {
    border: 1px solid;
    border-radius: 15px; 
}

ModelCard QLabel#modelDescLabel {
    line-height: 4;
}

/* ==========================================================================
   Стили для полей ввода
   ========================================================================== */
CustomInputDialog QLineEdit#dialogInput,
CustomInputDialog QTextEdit#dialogDescInput {
    border: 1px solid;
    border-radius: 5px;
    padding: 5px;
    color: #E0E7FF;
    font-weight: 400;
    font-size: 14px;

}

QLineEdit#epochsInput {
    width: 60px;
    border: 1px solid;
    border-radius: 5px;
    padding: 5px;
    color: #E0E7FF;
}

/* ==========================================================================
   Стили для радио-кнопок
   ========================================================================== */
QRadioButton#trainModeRadio {
    font-size: 12px;
    color: #E0E7FF;
}

QRadioButton#trainModeRadio::indicator {
    width: 16px;
    height: 16px;
}

QRadioButton#trainModeRadio::indicator:checked {
    border: 2px solid;
    border-radius: 8px;
}

QRadioButton#trainModeRadio::indicator:unchecked {
    border: 2px solid;
    border-radius: 8px;
}

/* ==========================================================================
   Стили для индикатора прогресса
   ========================================================================== */
QProgressBar#progressBar {
    border: 1px solid;
    border-radius: 5px;
    font-size: 14px;
}

ModelTab QLabel#progressLabel {
    font-size: 16px;
    font-weight: 400;
}

/* ==========================================================================
   Стили для диалоговых окон
   ========================================================================== */
QDialog, 
QMessageBox,
QInputDialog, 
QFileDialog {
    border: 1px solid;
    border-radius: 10px;
}

QDialog QLabel, 
QInputDialog QLabel, 
QFileDialog QLabel {
    font-size: 14px;
    font-weight: 400;
    color: #E0E7FF;
}

QDialog QPushButton, 
QInputDialog QPushButton, 
QFileDialog QPushButton {
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #E0E7FF;
}

QDialog QLineEdit, 
QInputDialog QLineEdit, 
QFileDialog QLineEdit {
    border: 1px solid;
    border-radius: 5px;
    padding: 5px;
    color: #E0E7FF;
}
"""

MISTY_SUNRISE_THEME = """
/* ==========================================================================
   Цветовая палитра (для справки)
   --primary-color: #2A3A4A  Основной цвет для кнопок и фона
   --hover-color: #3A5A7A  Цвет при наведении и для активных состояний
   --accent-color: #2C488F  Акцентный цвет для активных элементов
   --accent-hover: #4C6DC2  Светлый оттенок акцента для наведений
   --background: rgba(42, 58, 74, 0.3)  Прозрачная подложка
   --disabled-color: #5A7A9A  Цвет для отключенных элементов
   --dark-background: #1A2A3A  Темный фон для прогресс-бара
   ========================================================================== */

/* ==========================================================================
   Общие стили для всего приложения
   ========================================================================== */
QMainWindow {
    background-image: url("./src/assets/misty_sunrise_background.png");
}

/* Стили для вертикальной полосы прокрутки */
QScrollBar:vertical {
    background: rgba(42, 58, 74, 0.3);
}

QScrollBar::handle:vertical {
    background: #3A5A7A;  
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: rgba(42, 58, 74, 0.3);
}

/* ==========================================================================
   Стили для рамки окна
   ========================================================================== */
QWidget#borderWidget {
    border-color: #2A3A4A;
}

/* ==========================================================================
   Стили для боковой панели
   ========================================================================== */
QFrame#sidebarFrame {
    background-color: rgba(42, 58, 74, 0.4);
}

/* ==========================================================================
   Стили для заголовка окна
   ========================================================================== */
QWidget#headerWidget {
    background: #2A3A4A;
}

/* ==========================================================================
   Стили для вкладок
   ========================================================================== */
QTabWidget::pane {
    background-color: rgba(42, 58, 74, 0.4);
    border-color: #3A5A7A;
}

QTabBar::tab {
    background-color: #2A3A4A;
}

QTabBar::tab:selected {
    background-color: #3A5A7A;
    border-bottom-color: #2C488F;
}

/* ==========================================================================
   Стили для кнопок
   ========================================================================== */
QPushButton {
    background-color: #2A3A4A;
}

QPushButton:hover {
    background-color: #3A5A7A;
}

QPushButton:disabled {
    background: #5A7A9A;
}

QPushButton#selectModelButton {
    background-color: #2A3A4A;
}

QPushButton#startTrainButton,
QPushButton#addModelButton {
    background-color: #2A3A4A;
}

QPushButton#selectModelButton:hover,
QPushButton#startTrainButton:hover,
QPushButton#addModelButton:hover {
    background-color: #3A5A7A;
}

QPushButton#prevThemeButton,
QPushButton#nextThemeButton,
QTabBar QToolButton {
    background-color: #2A3A4A;
}

QPushButton#prevThemeButton:hover,
QPushButton#nextThemeButton:hover,
QTabBar QToolButton:hover {
    background-color: #3A5A7A;
}

QPushButton#minimizeButton:hover,
QPushButton#maximizeButton:hover {
    background: #3A5A7A;
}

QPushButton#closeButton:hover {
    background: #4C6DC2;
}

QPushButton#deleteButton {
    background-color: #2C488F;
}

QPushButton#deleteButton:hover {
    background-color: #4C6DC2;
}

/* ==========================================================================
   Стили для карточек моделей
   ========================================================================== */
QFrame#modelCard {
    background-color: rgba(42, 58, 74, 0.3);
    border-color: #3A5A7A;
}

/* ==========================================================================
   Стили для полей ввода
   ========================================================================== */
QLineEdit#epochsInput {
    background-color: #2A3A4A;
    border-color: #3A5A7A;
}

/* ==========================================================================
   Стили для радио-кнопок
   ========================================================================== */
QRadioButton#trainModeRadio::indicator:checked {
    background-color: #4C6DC2;
    border-color: #3A5A7A;
}

QRadioButton#trainModeRadio::indicator:unchecked {
    border-color: #3A5A7A;
}

/* ==========================================================================
   Стили для индикатора прогресса
   ========================================================================== */
QProgressBar#progressBar {
    border-color: #F5F8FF;
    background-color: #1A2A3A;
}

QProgressBar#progressBar::chunk {
    background-color: #F5F8FF;
}

/* ==========================================================================
   Стили для диалоговых окон
   ========================================================================== */
QDialog, 
QMessageBox,
QInputDialog, 
QFileDialog {
    background-color: rgba(42, 58, 74, 0.7);
    border-color: #3A5A7A;
}

QDialog QPushButton, 
QInputDialog QPushButton, 
QFileDialog QPushButton {
    background-color: #2A3A4A;
}

QDialog QPushButton:hover, 
QInputDialog QPushButton:hover, 
QFileDialog QPushButton:hover {
    background-color: #3A5A7A;
}

QDialog QLineEdit, 
QInputDialog QLineEdit, 
QFileDialog QLineEdit {
    background-color: #2A3A4A;
    border-color: #3A5A7A;
}

/* ==========================================================================
   Кастомные стили для диалогов
   ========================================================================== */
ErrorDialog,
CustomInputDialog {
    background-color: rgba(42, 58, 74, 0.7);
}

ErrorDialog QWidget#headerWidget,
CustomInputDialog QWidget#headerWidget {
    background-color: #2A3A4A; 
    border-bottom: 1px solid #3A5A7A;
}

ErrorDialog QPushButton#closeButton,
CustomInputDialog QPushButton#closeButton {
    border: none;
    border-radius: 15px;
}

ErrorDialog QPushButton#closeButton:hover,
CustomInputDialog QPushButton#closeButton:hover {
    background-color: #4C6DC2; 
}

CustomInputDialog QLineEdit#dialogInput,
CustomInputDialog QTextEdit#dialogDescInput {
    background-color: #2A3A4A; 
    border-color: #3A5A7A;
    padding: 5px;
}

ErrorDialog QPushButton#dialogOkButton,
ErrorDialog QPushButton#dialogCancelButton,
CustomInputDialog QPushButton#dialogOkButton, 
CustomInputDialog QPushButton#dialogCancelButton {
    background-color: #2A3A4A; 
    border: 1px solid #3A5A7A; 
    padding: 5px 15px;
    border-radius: 5px;
}

ErrorDialog QPushButton#dialogOkButton:hover,
ErrorDialog QPushButton#dialogCancelButton:hover,
CustomInputDialog QPushButton#dialogOkButton:hover, 
CustomInputDialog QPushButton#dialogCancelButton:hover {
    background-color: #3A5A7A;
}
"""

PINK_DAWN_THEME = """
/* ==========================================================================
   Цветовая палитра (для справки)
   --primary-color: #3A2A3A  Основной цвет для кнопок и фона
   --hover-color: #5A3A5A  Цвет при наведении и для активных состояний
   --accent-color: #FF9999  Акцентный цвет для активных элементов
   --accent-hover: #FFCCCC  Светлый оттенок акцента для наведений
   --background: rgba(90, 58, 90, 0.3)  Прозрачная подложка
   --disabled-color: #7A5A7A  Цвет для отключенных элементов
   --dark-background: #2A1A2A  Темный фон для прогресс-бара
   ========================================================================== */

/* ==========================================================================
   Общие стили для всего приложения
   ========================================================================== */
QMainWindow {
    background-image: url("./src/assets/pink_dawn_background.png");
}

/* Стили для вертикальной полосы прокрутки */
QScrollBar:vertical {
    background: rgba(90, 58, 90, 0.3);
}

QScrollBar::handle:vertical {
    background: #5A3A5A;  
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: rgba(90, 58, 90, 0.3);
}

/* ==========================================================================
   Стили для рамки окна
   ========================================================================== */
QWidget#borderWidget {
    border-color: #3A2A3A;
}

/* ==========================================================================
   Стили для боковой панели
   ========================================================================== */
QFrame#sidebarFrame {
    background-color: rgba(90, 58, 90, 0.4);
}

/* ==========================================================================
   Стили для заголовка окна
   ========================================================================== */
QWidget#headerWidget {
    background: #3A2A3A;
}

/* ==========================================================================
   Стили для вкладок
   ========================================================================== */
QTabWidget::pane {
    background-color: rgba(90, 58, 90, 0.4);
    border-color: #5A3A5A;
}

QTabBar::tab {
    background-color: #3A2A3A;
}

QTabBar::tab:selected {
    background-color: #5A3A5A;
    border-bottom-color: #FF9999;
}

/* ==========================================================================
   Стили для кнопок
   ========================================================================== */
QPushButton {
    background-color: #3A2A3A;
}

QPushButton:hover {
    background-color: #5A3A5A;
}

QPushButton:disabled {
    background: #7A5A7A;
}

QPushButton#selectModelButton {
    background-color: #3A2A3A;
}

QPushButton#startTrainButton,
QPushButton#addModelButton {
    background-color: #3A2A3A;
}

QPushButton#selectModelButton:hover,
QPushButton#startTrainButton:hover,
QPushButton#addModelButton:hover {
    background-color: #5A3A5A;
}

QPushButton#prevThemeButton,
QPushButton#nextThemeButton,
QTabBar QToolButton {
    background-color: #3A2A3A;
}

QPushButton#prevThemeButton:hover,
QPushButton#nextThemeButton:hover,
QTabBar QToolButton:hover {
    background-color: #5A3A5A;
}

QPushButton#minimizeButton:hover,
QPushButton#maximizeButton:hover {
    background: #5A3A5A;
}

QPushButton#closeButton:hover {
    background: #FF9999;
}

QPushButton#deleteButton {
    background-color: #FF9999;
}

QPushButton#deleteButton:hover {
    background-color: #FFCCCC;
}

/* ==========================================================================
   Стили для карточек моделей
   ========================================================================== */
QFrame#modelCard {
    background-color: rgba(90, 58, 90, 0.3);
    border-color: #5A3A5A;
}

/* ==========================================================================
   Стили для полей ввода
   ========================================================================== */
QLineEdit#epochsInput {
    background-color: #3A2A3A;
    border-color: #5A3A5A;
}

/* ==========================================================================
   Стили для радио-кнопок
   ========================================================================== */
QRadioButton#trainModeRadio::indicator:checked {
    background-color: #3A2A3A;
    border-color: #5A3A5A;
}

QRadioButton#trainModeRadio::indicator:unchecked {
    border-color: #5A3A5A;
}

/* ==========================================================================
   Стили для индикатора прогресса
   ========================================================================== */
QProgressBar#progressBar {
    border-color: #FF9999;
    background-color: #2A1A2A;
}

QProgressBar#progressBar::chunk {
    background-color: #3A2A3A;
}

/* ==========================================================================
   Стили для диалоговых окон
   ========================================================================== */
QDialog, 
QMessageBox,
QInputDialog, 
QFileDialog {
    background-color: rgba(58, 42, 58, 0.7); 
    border-color: #5A3A5A;
}

QDialog QPushButton, 
QInputDialog QPushButton, 
QFileDialog QPushButton {
    background-color: #3A2A3A;
}

QDialog QPushButton:hover, 
QInputDialog QPushButton:hover, 
QFileDialog QPushButton:hover {
    background-color: #5A3A5A;
}

QDialog QLineEdit, 
QInputDialog QLineEdit, 
QFileDialog QLineEdit {
    background-color: #3A2A3A;
    border-color: #5A3A5A;
}

/* ==========================================================================
   Кастомные стили для CustomInputDialog 
   ========================================================================== */
ErrorDialog,
CustomInputDialog {
    background-color: rgba(90, 58, 90, 0.7); 
}

ErrorDialog QWidget#headerWidget,
CustomInputDialog QWidget#headerWidget {
    background-color: #3A2A3A; 
    border-bottom: 1px solid #5A3A5A; 
}

ErrorDialog QPushButton#closeButton,
CustomInputDialog QPushButton#closeButton {
    border: none;
    border-radius: 15px;
}

ErrorDialog QPushButton#closeButton,
CustomInputDialog QPushButton#closeButton:hover {
    background-color: #FFCCCC;
}

CustomInputDialog QLineEdit#dialogInput,
CustomInputDialog QTextEdit#dialogDescInput {
    background-color: #3A2A3A;
    border-color: #5A3A5A;
    padding: 5px;
}

ErrorDialog QPushButton#dialogOkButton,
ErrorDialog QPushButton#dialogCancelButton,
CustomInputDialog QPushButton#dialogOkButton, 
CustomInputDialog QPushButton#dialogCancelButton {
    background-color: #3A2A3A; 
    border: 1px solid #5A3A5A; 
    padding: 5px 15px;
    border-radius: 5px;
}

ErrorDialog QPushButton#dialogOkButton:hover,
ErrorDialog QPushButton#dialogCancelButton:hover,
CustomInputDialog QPushButton#dialogOkButton:hover, 
CustomInputDialog QPushButton#dialogCancelButton:hover {
    background-color: #5A3A5A;
}
"""

DAYLIGHT_MOUNTAINS_THEME = """
/* ==========================================================================
   Цветовая палитра (для справки)
   --primary-color: #1A3A5A  Основной цвет для кнопок и фона
   --hover-color: #2A5A8A  Цвет при наведении и для активных состояний
   --accent-color: #66B3FF  Акцентный цвет для активных элементов
   --accent-hover: #99CCFF  Светлый оттенок акцента для наведений
   --background: rgba(26, 58, 90, 0.3)  Прозрачная подложка
   --disabled-color: #4A7A9A  Цвет для отключенных элементов
   --dark-background: #0F2A4A  Темный фон для прогресс-бара
   ========================================================================== */

/* ==========================================================================
   Общие стили для всего приложения
   ========================================================================== */
QMainWindow {
    background-image: url("./src/assets/daylight_mountains_background.png");
}

/* Стили для вертикальной полосы прокрутки */
QScrollBar:vertical {
    background: rgba(26, 58, 90, 0.3);
}

QScrollBar::handle:vertical {
    background: #2A5A8A;  
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: rgba(26, 58, 90, 0.3);
}

/* ==========================================================================
   Стили для рамки окна
   ========================================================================== */
QWidget#borderWidget {
    border-color: #1A3A5A;
}

/* ==========================================================================
   Стили для боковой панели
   ========================================================================== */
QFrame#sidebarFrame {
    background-color: rgba(26, 58, 90, 0.4);
}

/* ==========================================================================
   Стили для заголовка окна
   ========================================================================== */
QWidget#headerWidget {
    background: #1A3A5A;
}

/* ==========================================================================
   Стили для вкладок
   ========================================================================== */
QTabWidget::pane {
    background-color: rgba(26, 58, 90, 0.4);
    border-color: #2A5A8A;
}

QTabBar::tab {
    background-color: #1A3A5A;
}

QTabBar::tab:selected {
    background-color: #2A5A8A;
    border-bottom-color: #66B3FF;
}

/* ==========================================================================
   Стили для кнопок
   ========================================================================== */
QPushButton {
    background-color: #1A3A5A;
}

QPushButton:hover {
    background-color: #2A5A8A;
}

QPushButton:disabled {
    background: #4A7A9A;
}

QPushButton#selectModelButton {
    background-color: #1A3A5A;
}

QPushButton#startTrainButton,
QPushButton#addModelButton {
    background-color: #1A3A5A;
}

QPushButton#selectModelButton:hover,
QPushButton#startTrainButton:hover,
QPushButton#addModelButton:hover {
    background-color: #2A5A8A;
}

QPushButton#prevThemeButton,
QPushButton#nextThemeButton,
QTabBar QToolButton {
    background-color: #1A3A5A;
}

QPushButton#prevThemeButton:hover,
QPushButton#nextThemeButton:hover,
QTabBar QToolButton:hover {
    background-color: #2A5A8A;
}

QPushButton#minimizeButton:hover,
QPushButton#maximizeButton:hover {
    background: #2A5A8A;
}

QPushButton#closeButton:hover {
    background: #66B3FF;
}

QPushButton#deleteButton {
    background-color: #66B3FF;
}

QPushButton#deleteButton:hover {
    background-color: #99CCFF;
}

/* ==========================================================================
   Стили для карточек моделей
   ========================================================================== */
QFrame#modelCard {
    background-color: rgba(26, 58, 90, 0.3);
    border-color: #2A5A8A;
}

/* ==========================================================================
   Стили для полей ввода
   ========================================================================== */
QLineEdit#epochsInput {
    background-color: #1A3A5A;
    border-color: #2A5A8A;
}

/* ==========================================================================
   Стили для радио-кнопок
   ========================================================================== */
QRadioButton#trainModeRadio::indicator:checked {
    background-color: #66B3FF;
    border-color: #2A5A8A;
}

QRadioButton#trainModeRadio::indicator:unchecked {
    border-color: #2A5A8A;
}

/* ==========================================================================
   Стили для индикатора прогресса
   ========================================================================== */
QProgressBar#progressBar {
    border-color: #2A5A8A;
    background-color: #0F2A4A;
}

QProgressBar#progressBar::chunk {
    background-color: #1A3A5A;
}

/* ==========================================================================
   Стили для диалоговых окон
   ========================================================================== */
QDialog, 
QMessageBox,
QInputDialog, 
QFileDialog {
    background-color: rgba(48, 48, 78, 0.7);
    border-color: #5A5A8A;
}

QDialog QPushButton, 
QInputDialog QPushButton, 
QFileDialog QPushButton {
    background-color: #30304E;
}

QDialog QPushButton:hover, 
QInputDialog QPushButton:hover, 
QFileDialog QPushButton:hover {
    background-color: #5A5A8A;
}

QDialog QLineEdit, 
QInputDialog QLineEdit, 
QFileDialog QLineEdit {
    background-color: #30304E;
    border-color: #5A5A8A;
}

/* ==========================================================================
   Кастомные стили для CustomInputDialog 
   ========================================================================== */
ErrorDialog,
CustomInputDialog {
    background-color: rgba(26, 58, 90, 0.7); 
}

ErrorDialog QWidget#headerWidget,
CustomInputDialog QWidget#headerWidget {
    background-color: #1A3A5A; 
    border-bottom: 1px solid #2A5A8A;
}

ErrorDialog QPushButton#closeButtonr,
CustomInputDialog QPushButton#closeButton {
    border: none;
    border-radius: 15px;
}

ErrorDialog QPushButton#closeButton:hover,
CustomInputDialog QPushButton#closeButton:hover {
    background-color: #66B3FF;
}

CustomInputDialog QLineEdit#dialogInput,
CustomInputDialog QTextEdit#dialogDescInput {
    background-color: #1A3A5A; 
    border-color: #2A5A8A;
    padding: 5px;
}

ErrorDialog QPushButton#dialogOkButton,
ErrorDialog QPushButton#dialogCancelButton,
CustomInputDialog QPushButton#dialogOkButton, 
CustomInputDialog QPushButton#dialogCancelButton {
    background-color: #1A3A5A;
    border: 1px solid #2A5A8A; 
    padding: 5px 15px;
    border-radius: 5px;
}

ErrorDialog QPushButton#dialogOkButton:hover,
ErrorDialog QPushButton#dialogCancelButton:hover,
CustomInputDialog QPushButton#dialogOkButton:hover, 
CustomInputDialog QPushButton#dialogCancelButton:hover {
    background-color: #2A5A8A; 
}
"""