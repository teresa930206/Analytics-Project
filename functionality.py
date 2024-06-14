def merge_data(data,column,entity,replacement):
    data.loc[data[column] == entity, column] = replacement
    
def fill_nulls_with(data,column,replacement):
    data[column] = data[column].fillna(replacement)
    
def drop_nulls_in_column(data,column):
    data.dropna(subset=[column],inplace=True)

def drop_columns(data,column_list):
    for column in column_list:
        
     data.drop(columns=[column], inplace=True)

def explode_data(data,column):
    list_column_names = [col for col in data.columns if col not in [column]]
    df_exploded = (data.set_index(list_column_names)
    .apply(lambda x: x.str.split(', ').explode())
    .reset_index())
    return df_exploded  

def merge_multiple_data(data,column,dict):
    for key, value in dict.items():
        data.loc[data[column] == key, column] = value
        
def encode(item_freq):
    res = False
    if item_freq > 0:
        res = True
    return res