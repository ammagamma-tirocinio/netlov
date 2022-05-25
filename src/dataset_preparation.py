from config import *
from ahead.metrics import evaluate_errors

def graph_dataset(data,map_col,metric = METRIC,baseline = False):
  '''
  Given a dataset, extract metric column and melt the dataset for plot putposes.
  data - Dataframe
  map_col - Dict returned by ahead prediction_main
  metric_list - list containing the metric of interest -- mape,mae,me
  id_list - subset of id
  '''
  if baseline == False:
      df,_ = evaluate_errors(data, map_col, metrics_name = [metric], y_true='real', y_pred='pred')
  else:
      df, _ = evaluate_errors(data, map_col, metrics_name=[metric], y_true='real', y_pred='baseline')

  metric_columns = [map_col['val_qta_kg'][str(el)][metric] for el in range(14)]
  df = df[['dat_trasporto','id'] + metric_columns]
  dict_metric = dict(zip(metric_columns,np.arange(1,15).tolist()))

  df = pd.melt(df,id_vars = ['dat_trasporto','id'],value_vars = metric_columns, var_name = 'steps')
  df['steps'] = df['steps'].map(dict_metric)
  df = df.sort_values(by = ['steps','value']) # sorted
  df.columns = df.columns.str.replace('value', metric)
  return df

def slice_dataset(data,date1,date2 = None,id = None):
  '''
  Given a Dataset return a subset of specifc date and or ids
  data -> DataFrame
  data1,data2 = datetime.datetime()
  '''
  if date2 == None:
    if id == None:
      data = data[data['dat_trasporto'] == date1]
    else:
      data = data[(data['id'].isin(id)) & (data['dat_trasporto'] == date1)]
  else:
    datalist = pd.date_range(start = date1, end = date2, freq = 'M').tolist()
    if id == None:
      data = data[data['dat_trasporto'].isin(datalist)]
    else:
      print(id)
      data = data[(data['id'].isin(id)) & (data['dat_trasporto'].isin(datalist))]
  return data

def compute_quantile(data,q,metric):
  quant = []
  for s in range(1,15):
    quant_ref = []
    for ref in ['past_year','current_year']:
      quant_ref.append(data[metric][(data['steps'] == s)&(data['reference'] == ref) ].quantile(q))
    quant.append(quant_ref)
  return pd.DataFrame(quant, index = np.arange(1,15), columns = ['past_year','current_year'])

def last_year(data_now):
  ''' data_now: datatime '''
  if data_now == None:
    return None
  delta = pd.Timedelta(days=365)
  return data_now-delta

def data_preparation(curr_df,ref_df,map_col_curr,map_col_ref, date1,date2 = None, id_list = ID_LIST,metric = METRIC):
    current_melt = graph_dataset(curr_df, map_col_curr, metric = metric)
    reference_melt = graph_dataset(ref_df, map_col_ref, metric = metric, baseline = BASELINE)
    current_melt_id = slice_dataset(current_melt, date1,date2, id = id_list)
    reference_melt_id = slice_dataset(reference_melt, last_year(date1),last_year(date2),id = id_list)

    melt_id = pd.concat([reference_melt_id, current_melt_id])
    melt_id['reference'] = np.append(np.ones(len(reference_melt_id)), np.zeros(len(current_melt_id)))
    melt_id['reference'] = melt_id['reference'].map({1: 'reference', 0: 'current_year'})
    return melt_id,current_melt_id, reference_melt_id


