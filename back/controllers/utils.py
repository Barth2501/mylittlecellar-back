def df_to_dict(df):
    if df.ndim == 1:
        return df.to_dict()
    ret = {}
    for key in df.index.get_level_values(0):
        sub_df = df.xs(key)
        ret[key] = df_to_dict(sub_df)
    return ret

def df_to_json(df):
    if df.ndim == 1:
        return df.to_dict()
    ret = []
    for key in df.index.get_level_values(0):
        sub_df = df.xs(key)
        ret.append(df_to_dict(sub_df))
    return ret

def df_to_multi_index_dict(df):
    ret = {}
    for key in df.index.get_level_values(0):
        sub_df = df.xs(key)
        if sub_df.ndim == 1:
            ret[key] = sub_df.to_dict()
        elif sub_df.ndim == 2:
            ret[key] = sub_df.to_dict('records')
    return ret