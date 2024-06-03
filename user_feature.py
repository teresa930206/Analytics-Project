Python 3.11.4 (v3.11.4:d2340ef257, Jun  6 2023, 19:15:51) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
def generate_user_features(prior_data = None):
    
    """
    Generate User based features and return it as dataframe object.
    Later this dataframe will be merged with other dataframe like product features to generate training data
    
    Features:
    feat_1 : user_reorder_rate              : Average reorder rate on orders placed?
    feat_2 : user_unique_products           : Distinct Products ordered ?
    feat_3 : user_total_products            : Total products ordered ?
    feat_4 : user_avg_cart_size             : mean Products per order ? = average cart size ?
    feat_5 : user_avg_days_between_orders   : Average days between orders ?
    feat_6 : user_reordered_products_ratio  : user product reorder ratio
    
    """
    
    #create an empty dataframe
    user_features = pd.DataFrame(columns=['user_id'])
    
    #Add user_id
    user_features['user_id'] = prior_data['user_id'].sort_values().unique()
    
    # Get mean reorder rate for every user
    # Process :
    #  1. Count reorders for every user_id using reordered feature of prior_train_orders
    #  2. Perform Groupby on this output using user_id and get prob of reorder == 0 and reorder == 1
    #  3. Seperate reorder == 0 and reorder == 1 using pivot and fill 0 , where reorder==1 is NA ( indicating no reorders)
    #  4. Add reorder == 1 column to feat_1 
    
    user_reorder_rate = prior_data.groupby(["user_id","reordered"])['reordered'].count().groupby(level = 0).apply(lambda x: x / float(x.sum())).reset_index(name='reorder_rate')
    user_reorder_rate = user_reorder_rate.pivot(index ='user_id', columns ='reordered', values =['reorder_rate']) 
    user_reorder_rate = pd.DataFrame(user_reorder_rate.to_records())
    user_reorder_rate.columns = ['user_id','0', '1']
    user_reorder_rate.set_index("user_id", inplace = True)
    user_reorder_rate.fillna(0, inplace = True)
    user_reorder_rate.reset_index(inplace = True)
...     user_features['user_reorder_rate'] = user_reorder_rate['1']
...     
...     #Get count of all unique products for every user
...     user_features['user_unique_products'] = prior_data.groupby(["user_id"])['product_name'].nunique().reset_index(name = 'unique')['unique']
...     
...     #Get count of all products ordered by user
...     user_features['user_total_products'] = prior_data.groupby(["user_id"])['product_name'].size().reset_index(name = 'count')['count']
...     
...     #Get mean products per user = Average cart size of user
...     df = prior_data.groupby(["user_id","order_id"])['add_to_cart_order'].count().reset_index(name='cart_size')\
...                                                                 .groupby('user_id')['cart_size'].mean().reset_index()
...     user_features['user_avg_cart_size'] = df['cart_size']
...     
...     #Get average days between 2 orders for every user
...     df = prior_data.groupby(["user_id","order_id"])['days_since_prior_order'].max().reset_index(name='mean_days_between_orders')\
...                                                                 .groupby('user_id')['mean_days_between_orders'].mean().reset_index()
...     user_features['user_avg_days_between_orders'] = df['mean_days_between_orders']
...     
...     
...     #get user product reorder ratio 
...     # number of unique products reordered / number of unique products ordered
...     df['user_id'] = prior_data['user_id'].sort_values().unique()
...     df['user_unique_products'] = prior_data.groupby(["user_id"])['product_name'].nunique().reset_index(name = 'unique')['unique']
...     df['user_reordered_products'] = prior_data[prior_data['reordered']==1].groupby(["user_id"])['product_name'].nunique().reset_index(name = 'reordered_unique')['reordered_unique']
...     df.fillna(0, inplace = True)
...     user_features['user_reordered_products_ratio'] = df['user_reordered_products'] / df['user_unique_products']
...     
...     del df
...     return user_featuresdef generate_user_features(prior_data = None):
    
    """
    Generate User based features and return it as dataframe object.
    Later this dataframe will be merged with other dataframe like product features to generate training data
    
    Features:
    feat_1 : user_reorder_rate              : Average reorder rate on orders placed?
    feat_2 : user_unique_products           : Distinct Products ordered ?
    feat_3 : user_total_products            : Total products ordered ?
    feat_4 : user_avg_cart_size             : mean Products per order ? = average cart size ?
    feat_5 : user_avg_days_between_orders   : Average days between orders ?
    feat_6 : user_reordered_products_ratio  : user product reorder ratio
    
    """
    
    #create an empty dataframe
    user_features = pd.DataFrame(columns=['user_id'])
    
    #Add user_id
    user_features['user_id'] = prior_data['user_id'].sort_values().unique()
    
    # Get mean reorder rate for every user
    # Process :
    #  1. Count reorders for every user_id using reordered feature of prior_train_orders
    #  2. Perform Groupby on this output using user_id and get prob of reorder == 0 and reorder == 1
    #  3. Seperate reorder == 0 and reorder == 1 using pivot and fill 0 , where reorder==1 is NA ( indicating no reorders)
    #  4. Add reorder == 1 column to feat_1 
    
    user_reorder_rate = prior_data.groupby(["user_id","reordered"])['reordered'].count().groupby(level = 0).apply(lambda x: x / float(x.sum())).reset_index(name='reorder_rate')
    user_reorder_rate = user_reorder_rate.pivot(index ='user_id', columns ='reordered', values =['reorder_rate']) 
    user_reorder_rate = pd.DataFrame(user_reorder_rate.to_records())
    user_reorder_rate.columns = ['user_id','0', '1']
    user_reorder_rate.set_index("user_id", inplace = True)
    user_reorder_rate.fillna(0, inplace = True)
    user_reorder_rate.reset_index(inplace = True)
    user_features['user_reorder_rate'] = user_reorder_rate['1']
    
    #Get count of all unique products for every user
    user_features['user_unique_products'] = prior_data.groupby(["user_id"])['product_name'].nunique().reset_index(name = 'unique')['unique']
    
    #Get count of all products ordered by user
    user_features['user_total_products'] = prior_data.groupby(["user_id"])['product_name'].size().reset_index(name = 'count')['count']
    
    #Get mean products per user = Average cart size of user
    df = prior_data.groupby(["user_id","order_id"])['add_to_cart_order'].count().reset_index(name='cart_size')\
                                                                .groupby('user_id')['cart_size'].mean().reset_index()
    user_features['user_avg_cart_size'] = df['cart_size']
    
    #Get average days between 2 orders for every user
    df = prior_data.groupby(["user_id","order_id"])['days_since_prior_order'].max().reset_index(name='mean_days_between_orders')\
                                                                .groupby('user_id')['mean_days_between_orders'].mean().reset_index()
    user_features['user_avg_days_between_orders'] = df['mean_days_between_orders']
    
    
    #get user product reorder ratio 
    # number of unique products reordered / number of unique products ordered
    df['user_id'] = prior_data['user_id'].sort_values().unique()
    df['user_unique_products'] = prior_data.groupby(["user_id"])['product_name'].nunique().reset_index(name = 'unique')['unique']
    df['user_reordered_products'] = prior_data[prior_data['reordered']==1].groupby(["user_id"])['product_name'].nunique().reset_index(name = 'reordered_unique')['reordered_unique']
    df.fillna(0, inplace = True)
    user_features['user_reordered_products_ratio'] = df['user_reordered_products'] / df['user_unique_products']
    
    del df
