from config import *
from data_load import pickle_load, yaml_load
from dataset_preparation import data_preparation
from plots import grafico1,grafico2,grafico3

def main():
    st.title("Dashboard prediction")
    current_pred = pickle_load(os.path.join(TEST_PRED,'test_prediction.pickle'))
    current_map_col = yaml_load(os.path.join(TEST_PRED,'map_col_test.yml'))


    if BASELINE:
        reference_pred = pickle_load(os.path.join(TEST_PRED,'test_prediction_bl.pickle'))
        reference_map_col= yaml_load(os.path.join(TEST_PRED,'map_col_test.yml'))

    else:
        reference_pred = pickle_load(os.path.join(TRAIN_PRED, 'train_prediction.pickle'))
        reference_map_col = yaml_load(os.path.join(TRAIN_PRED, 'map_col_train.yml'))

    # Select ID
    list_of_id = st.sidebar.radio("Selezionare la variabile", list(cols_pred.labels_to_pred))

    melt_id,current_melt_id, reference_melt_id = data_preparation(current_pred, reference_pred,current_map_col, reference_map_col, DATA1, DATA2, ID_LIST)


    grafico1(current_melt_id,reference_melt_id,melt_id)
    grafico2(current_melt_id,reference_melt_id)
    grafico3(current_melt_id,reference_melt_id,melt_id)


if __name__ == "__main__":
    main()



