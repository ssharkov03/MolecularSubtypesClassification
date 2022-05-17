import joblib
import cloudpickle as cp
import pandas as pd
import numpy as np
import pickle
from urllib.request import urlopen
from config import COLUMN_DATA_PATH
from config import MODEL_PATH

THRESH = 0.7

# Change column order for further ML predictions
def remodeling_dataframe(df):
    with open('COLUMN_DATA_PATH', 'rb') as data:
        columns_order = pickle.load(data)

    comment = "None"
    if np.array_equiv(columns_order, df.columns):
        return df, comment

    shape_x = df.shape[0]
    shape_y = len(columns_order)

    new_df = np.full((shape_x, shape_y), np.nan)
    new_df = pd.DataFrame(new_df)
    new_df.columns = columns_order
    new_df.index = df.index

    needed_columns_set = set(columns_order)
    real_columns_set = set(df.columns)
    valid_columns_in_real_set = needed_columns_set.intersection(real_columns_set)
    valid_columns = list(valid_columns_in_real_set)
    num_of_valid_columns = len(valid_columns)

    if num_of_valid_columns/shape_y < THRESH:
        comment = f"Risk {num_of_valid_columns/shape_y:0.6f}"
    new_df[valid_columns] = df[valid_columns]
    return new_df, comment


def cancerTypeDetection(path_to_sample, type_of_file, separator=',', index_column=0):
    if type_of_file == 'csv':
        sample = pd.read_csv(path_to_sample, sep=separator, index_col=index_column)
    elif type_of_file == 'txt':
        sample = pd.read_table(path_to_sample, sep=separator, index_col=index_column)
    else:
        sample = cp.load(urlopen(path_to_sample))

    if not isinstance(sample, pd.DataFrame):
        return None, "Not dataframe"

    model = joblib.load(MODEL_PATH)
    sample, comment = remodeling_dataframe(sample)  # comment can be "Risk"

    try:
        model_prediction = model.predict_all(sample.to_numpy())
        labels = ['Basal', 'Her2', 'Luminal A', 'Luminal B']
        model_prediction.rename(columns={'prediction_0': 'Basal', 'prediction_1': 'Her2', 'prediction_2': 'Luminal A', 'prediction_3': 'Luminal B', 'label': 'Результат предсказания'}, inplace=True)
        print(model_prediction)
        model_prediction['Результат предсказания'] = model_prediction['Результат предсказания'].apply(lambda x: labels[x])
        model_prediction.index = sample.index

    except (AttributeError, IndexError):
        return None, "Error"

    return model_prediction, comment


if __name__ == '__main__':
    model_pred, com = cancerTypeDetection("D:\\MyProjects\\Cancer detection\\patientDataSample.csv", 'automlCompete93strong.pkl', 'csv')
    print(model_pred, com)