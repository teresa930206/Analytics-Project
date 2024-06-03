Python 3.11.4 (v3.11.4:d2340ef257, Jun  6 2023, 19:15:51) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
def generate_user_product_features(prior_data = None):
    
    """
    Generate User-Product interaction features and return it as dataframe object.
    Later this dataframe will be merged with other dataframe like product features and user features to generate training data
    
    Features:
    feat_1 : u_p_order_rate             :  How frequently user ordered the product ?
    feat_2 : u_p_reorder_rate           :  How frequently user reordered the product ?
    feat_3 : u_p_avg_position           :  Average position of product in the cart on orders placed by user ?
    feat_4 : u_p_orders_since_last      :  Number of orders placed since the product was last ordered ?
    feat_5 : max_streak                 :  Number of orders where user continuously brought a product without miss
    """
    

    #create an empty dataframe
    user_product_features = pd.DataFrame(columns=['user_id','product_id'])
    
    #get unique user-product pairs ( total data is reduced by 60 %)
    #prior_train_orders.groupby(["user_id","product_id"]).size().shape[0]/prior_train_orders.shape[0]  - 0.409
    #add user and product to dataframe
    u_p = prior_data.groupby(["user_id","product_id"]).size().reset_index()
    user_product_features["user_id"] = u_p["user_id"]
    user_product_features["product_id"] = u_p["product_id"]
    
    #How frequently user ordered the product ?
    # #times user ordered the product/ #times user placed an order
    df = prior_data.groupby(["user_id","product_id"])["reordered"].size()
    df = df/prior_data.groupby(["user_id"]).size()
    df = df.reset_index(name = 'order_rate')
    df.fillna(0. , inplace = True)
    user_product_features["u_p_order_rate"] = df["order_rate"]
...     
...     #How frequently user reordered the product ?
...     # #times user reordered the product/ #times user ordered the product
...     df = prior_data[prior_data["reordered"]==1].groupby(["user_id","product_id"])["reordered"].size()
...     df = df/prior_data.groupby(["user_id","product_id"]).size()
...     df = df.reset_index(name = 'reorder_rate')
...     df.fillna(0. , inplace = True)
...     user_product_features["u_p_reorder_rate"] = df["reorder_rate"]
...     
...     #Average position of product in the cart on orders placed by user ?
...     
...     df = prior_data.groupby(["user_id","product_id"])['add_to_cart_order'].mean().reset_index(name = 'mean_position')
...     user_product_features['u_p_avg_position'] = df['mean_position']
... 
...     
...     #Number of orders placed since the product was last ordered ?
...     # Get last order_number placed by user , subtract with last order_number with the product in cart 
...     
...     df = prior_data.groupby(["user_id","product_id"])['order_number'].max().reset_index()
...     df_2 = prior_data.groupby(["user_id"])['order_number'].max().reset_index()
...     new_df = pd.merge(df, df_2,  how='outer', left_on=['user_id'], right_on = ['user_id'])        
...     new_df['order_diff'] = new_df['order_number_y'] - new_df['order_number_x']
...     user_product_features['u_p_orders_since_last'] = new_df['order_diff']
...     
...     #max_streak
...     df = prior_data.groupby(["user_id","product_id"])['reordered'].apply(list).reset_index(name = 'max_streak')
...     df['max_streak'] = df['max_streak'].apply(max_streak)
...     user_product_features = pd.merge(user_product_features, df, on= ["user_id","product_id"])
...     #user_features["max_streak"] = df['reorder_summary'].apply(max_streak) 
...     
...     
...     del df, new_df, df_2
...     return user_product_featuresdef generate_user_product_features(prior_data = None):
    
    """
    Generate User-Product interaction features and return it as dataframe object.
    Later this dataframe will be merged with other dataframe like product features and user features to generate training data
    
    Features:
    feat_1 : u_p_order_rate             :  How frequently user ordered the product ?
    feat_2 : u_p_reorder_rate           :  How frequently user reordered the product ?
    feat_3 : u_p_avg_position           :  Average position of product in the cart on orders placed by user ?
    feat_4 : u_p_orders_since_last      :  Number of orders placed since the product was last ordered ?
    feat_5 : max_streak                 :  Number of orders where user continuously brought a product without miss
    """
    

    #create an empty dataframe
    user_product_features = pd.DataFrame(columns=['user_id','product_id'])
    
    #get unique user-product pairs ( total data is reduced by 60 %)
    #prior_train_orders.groupby(["user_id","product_id"]).size().shape[0]/prior_train_orders.shape[0]  - 0.409
    #add user and product to dataframe
    u_p = prior_data.groupby(["user_id","product_id"]).size().reset_index()
    user_product_features["user_id"] = u_p["user_id"]
    user_product_features["product_id"] = u_p["product_id"]
    
    #How frequently user ordered the product ?
    # #times user ordered the product/ #times user placed an order
    df = prior_data.groupby(["user_id","product_id"])["reordered"].size()
    df = df/prior_data.groupby(["user_id"]).size()
    df = df.reset_index(name = 'order_rate')
    df.fillna(0. , inplace = True)
    user_product_features["u_p_order_rate"] = df["order_rate"]
    
    #How frequently user reordered the product ?
    # #times user reordered the product/ #times user ordered the product
    df = prior_data[prior_data["reordered"]==1].groupby(["user_id","product_id"])["reordered"].size()
    df = df/prior_data.groupby(["user_id","product_id"]).size()
    df = df.reset_index(name = 'reorder_rate')
    df.fillna(0. , inplace = True)
    user_product_features["u_p_reorder_rate"] = df["reorder_rate"]
    
    #Average position of product in the cart on orders placed by user ?
    
    df = prior_data.groupby(["user_id","product_id"])['add_to_cart_order'].mean().reset_index(name = 'mean_position')
    user_product_features['u_p_avg_position'] = df['mean_position']

    
    #Number of orders placed since the product was last ordered ?
    # Get last order_number placed by user , subtract with last order_number with the product in cart 
    
    df = prior_data.groupby(["user_id","product_id"])['order_number'].max().reset_index()
    df_2 = prior_data.groupby(["user_id"])['order_number'].max().reset_index()
    new_df = pd.merge(df, df_2,  how='outer', left_on=['user_id'], right_on = ['user_id'])        
    new_df['order_diff'] = new_df['order_number_y'] - new_df['order_number_x']
    user_product_features['u_p_orders_since_last'] = new_df['order_diff']
    
    #max_streak
    df = prior_data.groupby(["user_id","product_id"])['reordered'].apply(list).reset_index(name = 'max_streak')
    df['max_streak'] = df['max_streak'].apply(max_streak)
    user_product_features = pd.merge(user_product_features, df, on= ["user_id","product_id"])
    #user_features["max_streak"] = df['reorder_summary'].apply(max_streak) 
    
    
    del df, new_df, df_2
