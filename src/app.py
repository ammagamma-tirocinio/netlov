import pandas as pd

from config import *
from data_load import pickle_load, yaml_load
from dataset_preparation import data_preparation
from plots import grafico1,grafico2,grafico3

#@st.cache(allow_output_mutation=True)
st.set_page_config(layout="wide")
def main():
    st.title("Dashboard prediction")
    baseline = st.sidebar.selectbox("Selezionare il confronto", ['past_year','baseline'])

    current_pred = pd.read_feather(os.path.join(TEST_PRED,'test_prediction.feather'))
    current_map_col = yaml_load(os.path.join(TEST_PRED,'map_col_test.yml'))

    if baseline == 'baseline':
        reference_pred = pd.read_feather(os.path.join(TEST_PRED,'test_prediction_bl.feather'))
        reference_map_col= yaml_load(os.path.join(TEST_PRED,'map_col_test.yml'))
        bl = True

    else:
        reference_pred = pd.read_feather(os.path.join(TRAIN_PRED, 'train_prediction.feather'))
        reference_map_col = yaml_load(os.path.join(TRAIN_PRED, 'map_col_train.yml'))
        bl = False


    id_list = st.sidebar.multiselect("Selezionare il id specifico", reference_pred['id'].unique(),None)
    print(id_list)
    if type(id_list) == str:
        id_list = [id_list]
    elif len(id_list) == 0:
        id_list = ID_LIST

    melt_id,current_melt_id, reference_melt_id = data_preparation(current_pred, reference_pred,current_map_col, reference_map_col, DATA1, DATA2, id_list, baseline = bl)

    #check_errors_type = st.sidebar.radio("Show errors",
    #                                     ["global", "ids_step", "ids_all_steps", "id","ids_steps_first8"])

    st.plotly_chart(grafico1(current_melt_id,reference_melt_id,melt_id))
    st.plotly_chart(grafico2(current_melt_id,reference_melt_id))
    st.plotly_chart(grafico3(current_melt_id,reference_melt_id,melt_id))


if __name__ == "__main__":
    main()



