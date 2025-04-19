from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

import numpy as np
import pandas as pd
import joblib
import json
import keras
import os

from config import *

def save_models_metadata(models: dict) -> None:
    '''
    Сохраняет метаданные моделей (имя и описание) в файл
    '''

    metadata = {
        k: {"name": v["name"], "description": v.get("description", DEFAULT_DESCRIPTION)} 
        for k, v in models.items() if k != STANDARD_MODEL_ID
    }
    with open(MODELS_DESCRIPTION_FILENAME, "w") as f:
        json.dump(metadata, f)


def restore_integrity() -> None:
    '''
    Восстанавливает целостность директорий (на случай если удалена папка моделей). Больше пока ничего не проверяет
    '''

    if not os.path.exists(MODELS_DIRECTORY_PATH):
        os.makedirs(MODELS_DIRECTORY_PATH)


def get_models() -> dict[str:dict]:
    '''
    Возвращает модели по файлу описания моделей
            Возвращаемое значение:
                    models (dict[str:dict]): словарь моделей, ключ - ID, значение - словарь со свойствами
    '''
    models = {
        STANDARD_MODEL_ID: {
            "name": STANDARD_MODEL_NAME,
            "description": STANDARD_MODEL_DESCRIPTION,
            "var_name": None
        },
    }

    descriptions = {}

    try:
        with open(MODELS_DESCRIPTION_FILENAME) as f:
            descriptions = json.load(f)

        for model_id, description in descriptions.items():
            description["var_name"] = None
            models[model_id] = description

    except FileNotFoundError:
        # Ничего не делаем, если файла нет
        pass

    return models


def get_model(id: str) -> tuple['keras.src.models.model', MinMaxScaler, MinMaxScaler]:
    '''
    Возвращает кортеж: (модель, Scaler для X, Scaler для Y)
            Параметры:
                    id (str): id модели
            Возвращаемое значение:
                    model(tuple[keras.src.models.model, MinMaxScaler, MinMaxScaler]): необходимые модели
    '''
    model = None
    scaler_X = None
    scaler_Y = None

    model_path = os.path.join(MODELS_DIRECTORY_PATH, id + ".keras")
    scaler_X_path = os.path.join(MODELS_DIRECTORY_PATH, "scaler_X" + id + ".keras")
    scaler_Y_path = os.path.join(MODELS_DIRECTORY_PATH, "scaler_Y" + id + ".keras")

    try:
        if os.path.exists(model_path):
            model = load_model(model_path)
        else:
            print(f"Файлы модели {id} отсутствуют или пусты")
            return None, None, None
        
        if os.path.exists(scaler_X_path):
            scaler_X = joblib.load(scaler_X_path)
        if os.path.exists(scaler_Y_path):
            scaler_Y = joblib.load(scaler_Y_path)

    except Exception as e:
        print(f"Ошибка загрузки модели {id}: {e}")
        return None, None, None

    return model, scaler_X, scaler_Y


def get_standard_model() -> keras.src.models.model:

    '''
    Возвращает стандартную заготовленную модель
            Возвращаемое значение:
                    model(keras.src.models.model): модель
    '''

    model = Sequential()
    model.add(Dense(64, input_dim=2, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer=Adam(learning_rate=0.01), loss='mse')
    return model


def get_sсaled_data(years:list[int], months:list[int], temps:list[int], scaler_X:MinMaxScaler, scaler_y:MinMaxScaler) -> tuple[np.array, np.array]:
  
    '''
    Возвращает нормализованные данные
            Параметры:
                    years(list[int]): года
                    months(list[int]): месяца
                    temps(list[int]): temps[i] = средняя температура years[i], month[i]
                    scaler_X(MinMaxScaler): модель для нормализации годов и месяцев
                    scaler_Y(MinMaxScaler): модель для нормализации температур
            Возвращаемое значение:
                    scaled_data(tuple[np.array, np.array]): нормализованны данные
    '''

    X = np.column_stack((years, months))
    y = temps

    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))
    return X_scaled, y_scaled


def train_model(model_id:str, train_data_filename:str, epochs:int, verbose=1, callbacks=None):
    '''
    Тренирует модель
            Параметры:
                    model_id(str): id модели
                    train_data_filename(str): имя файла, на котором происходит обучение
                    epochs(int): количество эпох
            Возвращаемое значение:
                    train_data(tuple[dict, keras.src.models.model, dict, dict]): передает history обучения, обученную модель, результаты оценки (mae, mse), модели нормализации
    '''

    find_model = False
    model = None

    model_filename = model_id + ".keras"

    for model_file in os.scandir(MODELS_DIRECTORY_PATH):  
        if model_file.is_file() and model_file.name == model_filename:
            model = load_model(MODELS_DIRECTORY_PATH + "\\" + model_filename)
            find_model = True

    if not find_model:
        # Если не нашли стандартную модель в файлах, значит нужно ее создать
        if model_id == STANDARD_MODEL_ID:
            model = get_standard_model()
        # Если не нашли нестандартную модель в файлах, значит ее кто-то удалил оттуда
        else:
            raise FileNotFoundError("Не найден файл модели")

    historic_data = pd.read_csv(os.path.abspath(train_data_filename), encoding='utf-8', sep=";", index_col=False, header=0, low_memory=False)
    if "timestamp" not in historic_data.columns:
        historic_data = historic_data.rename(columns={'Местное время в Москве (ВДНХ)':'timestamp'})

    historic_data = historic_data[["timestamp", "T"]]
    historic_data['timestamp'] = pd.to_datetime(historic_data['timestamp'], dayfirst=True)
    historic_data['year'] = historic_data.timestamp.dt.year
    historic_data['month'] = historic_data.timestamp.dt.month

    aggregated_data = historic_data.groupby(['year', 'month'])['T'].agg(['mean'])

    years = []
    months = []
    for year, month in np.array(aggregated_data.index):
        years.append(year)
        months.append(month)

    temperatures = np.array(aggregated_data["mean"])

    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_scaled, y_scaled = get_sсaled_data(years, months, temperatures, scaler_X, scaler_y)

    # Оцениваем точность модели
    evaluate_test = {"mae":0, "mse":0}
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled)
    model.fit(X_train, y_train, epochs=epochs, verbose=verbose, callbacks=callbacks)
    predictions = model.predict(X_test)
    y_pred = scaler_y.inverse_transform(predictions)
    y_true = scaler_y.inverse_transform(y_test)
    evaluate_test["mae"] = mean_absolute_error(y_true, y_pred)
    evaluate_test["mse"] = mean_squared_error(y_true, y_pred)

    # Обучение модели
    history = model.fit(X_test, y_test, epochs=epochs, verbose=verbose, callbacks=callbacks)

    return history, model, evaluate_test, {"scaler_X": scaler_X, "scaler_Y": scaler_y}