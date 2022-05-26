import copy
from config import *
import nannyml as nml
from dataset_preparation import compute_month_day


def univariate_drift(pred,metadata):
    analysis = pred[pred['partition'] == 'analysis']
    reference = pred[pred['partition'] == 'reference']

    # Select a specific period wrt just important feauture
    reference_chunk = copy.deepcopy(reference)
    analysis_chunk = analysis.iloc[:120, :]
    reference_chunk['m_d'] = compute_month_day(reference_chunk, 'dat_trasporto')
    reference_chunk = reference_chunk[
        reference_chunk['m_d'].isin(compute_month_day(analysis_chunk, 'dat_trasporto'))].drop(columns='m_d')
    univariate_calculator = nml.UnivariateStatisticalDriftCalculator(model_metadata=metadata, chunk_size=120)
    univariate_calculator = univariate_calculator.fit(reference_data=reference_chunk)
    data = pd.concat([reference_chunk, analysis_chunk], ignore_index=True)
    univariate_results = univariate_calculator.calculate(data=data)
    ranker = nml.Ranker.by('alert_count')
    return ranker, univariate_results
