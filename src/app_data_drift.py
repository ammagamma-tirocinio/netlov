import pandas as pd

from config import *
from data_load import pickle_load, yaml_load
from dataset_preparation import data_drift_prep, metadata_generation
from data_drift import univariate_drift


st.set_page_config(layout="wide")
def main():
    st.title("Dashboard prediction")
    mod = st.sidebar.selectbox("Selezionare il tipo di drift", ['Univariate', 'Multivariate'])

    #data_load
    current_pred = pd.read_feather(os.path.join(TEST_PRED,'test_prediction.feather'))
    current_map_col = yaml_load(os.path.join(TEST_PRED,'map_col_test.yml'))

    reference_pred = pd.read_feather(os.path.join(TRAIN_PRED, 'train_prediction.feather'))
    reference_map_col = yaml_load(os.path.join(TRAIN_PRED, 'map_col_train.yml'))

    id_list = st.sidebar.multiselect("Selezionare il id specifico", reference_pred['id'].unique(),None)

    if len(id_list) == 0:
        id_list = ID_LIST

    df_prediction, metadata = data_drift_prep(current_pred,reference_pred,  DATA1, DATA2, id_list)

    if mod == 'Univariate':
        ranker, univariate_res = univariate_drift(df_prediction, metadata)
        print(metadata.feature)
        
        df_warning = ranker.rank(univariate_res, model_metadata=metadata, only_drifting=False)






if __name__ == "__main__":
    main()

