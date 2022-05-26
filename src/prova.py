from data_load import *
from config import *
import pandas as pd
from ahead.metrics import evaluate_errors_stats_by_ids, evaluate_errors

current_pred = pd.read_feather(os.path.join(TEST_PRED,'test_prediction.feather'))
map_col = yaml_load(os.path.join(TEST_PRED,'map_col_test.yml'))
train_errors, maps_col_error = evaluate_errors(current_pred, map_col, metrics_name = ['mape','mae'], y_true='real', y_pred='pred')
train_errors_ids = evaluate_errors_stats_by_ids(train_errors,maps_col_error,metrics_name = ['mape','mae'], stats=['median','mean'])
print(train_errors_ids)
print(train_errors)
train_errors_ids.reset_index().to_feather(os.path.join(TEST_PRED,'test_errors_ids.feather'))
train_errors.reset_index().to_feather(os.path.join(TEST_PRED,'test_errors.feather'))
with open(os.path.join(TEST_PRED,'map_cols_error.yml'), 'w') as output:
     yaml.dump(maps_col_error, output)



