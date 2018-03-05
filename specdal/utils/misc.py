import pandas as pd
import warnings
def get_monotonic_series(series):
    """return a list of series with monotonic index
    
    TODO: test what happens if not strictly monotonic
        i.e. index: 1, 2, 3, 3
    """
    if series.index.is_monotonic:
        return [series]
    else:
        index = pd.Series(series.index)
        head_positions = index[index.diff() < 0].index

        N = head_positions.size
        
        result = [series.iloc[:head_positions[0]]]
        result += [series.iloc[head_positions[i]:head_positions[i+1]] for i in range(0, N-1)]
        result += [series.iloc[head_positions[N-1]:]]
        return result

def get_pct_reflect(dataframe):
    """
    Helper function to calculate pct_reflect from other columns
    
    Returns
    -------
    pd.Series object for pct_reflect
    """
    columns = dataframe.columns.values
    pct_reflect = None
    #special case for piccolo
    if all(x in columns for x in ["tgt_count","ref_count","tgt_count_dark",
                "ref_count_dark"]):
        pct_reflect = (dataframe["tgt_count"]-dataframe["tgt_count_dark"])/(
                dataframe["ref_count"]-dataframe["ref_count_dark"])
    elif all(x in columns for x in ["tgt_count", "ref_count"]):
        pct_reflect = dataframe["tgt_count"]/dataframe["ref_count"]
    elif all(x in columns for x in ["tgt_radiance", "ref_radiance"]):
        pct_reflect = dataframe["tgt_radiance"]/dataframe["ref_radiance"]
    elif all(x in columns for x in ["tgt_reflect", "ref_reflect"]):
        pct_reflect = dataframe["tgt_reflect"]/dataframe["ref_reflect"]
    elif all(x in columns for x in ["tgt_irradiance", "ref_irradiance"]):
        pct_reflect = dataframe["tgt_irradiance"]/dataframe["ref_irradiance"]

    if pct_reflect is not None:
        pct_reflect.name = 'pct_reflect'
    else:
        warnings.warn("Dataframe lacks columns to compute pct_reflect")
    return pct_reflect