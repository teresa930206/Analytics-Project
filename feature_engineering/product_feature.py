Python 3.11.4 (v3.11.4:d2340ef257, Jun  6 2023, 19:15:51) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
def generate_product_features(prior_data = None):
    
    """
    Generate Product based features and return it as dataframe object.
    Later this dataframe will be merged with other dataframe to generate training data
    
    Features:
    feat_1 : product_reorder_rate       : How Frequently the product was reordered ?
    feat_2 : avg_pos_incart             : Average position of product in the cart ?
    
    next 3 values are calculated based product being 
        - organic, 
        - isYogurt - aisle
        - produce  - department
        - isFrozen  - department 
        - isdairy  - department
        - isbreakfast  - department 
        - issnack  - department
        - isbeverage  - department
    these values are then reduced to 3 columns using Non-Negative Matrix Factorization, to reduce sparsity
        
    feat_3 : p_reduced_feat_1             : column 1 from NMF output
    feat_4 : p_reduced_feat_2             : column 2 from NMF output
    feat_5 : p_reduced_feat_3             : column 3 from NMF output
    feat_6 : aisle_reorder_rate           : How frequently a product is reordered from the aisle to which this product belongs
    feat_7 : department_reorder_rate      : How frequently a product is reordered from the department to which this product belongs
    
    
    """
    
    #create an empty dataframe
    product_features = pd.DataFrame(columns=['product_id'])
    
    #add product_name
    product_features['product_id'] = prior_data['product_id'].sort_values().unique()
    
    #get reorder_rate for each product
    #reorder_rate = reorders / total orders
    df = pd.DataFrame({'reorder_rate': prior_data.groupby(['product_id','reordered'])['reordered'].\
                                                       count().groupby(level=0).\
                                                       apply(lambda x: x / float(x.sum()))}).reset_index()

    #get data of reordered products only
    new_df = df[df['reordered']==1]
    new_df['reorder_rate'] = new_df['reorder_rate'] * new_df['reordered']
    
    #handling for products which were never reordered, hence reorder_rate = 0.0
    new_df_1 = df[(df['reordered']==0) & (df['reorder_rate']==float(1.0))]
    new_df_1['reorder_rate'] = new_df_1['reorder_rate'] * new_df_1['reordered']
    new_df = new_df.append(new_df_1)
    
    #drop other columns of the new_df and sort values by product name to align with product features dataframe
    new_df.drop('reordered', axis = 1, inplace = True)
    new_df.sort_values(by='product_id', inplace =  True)   
    new_df = new_df.reset_index(drop = True)
    
    #add to feat_1 of product_features dataframe
    product_features['product_reorder_rate'] = new_df['reorder_rate']
    
    #get mean position of product in the cart, sort by product_name and add to feat_2 of product_features
    mean_position = prior_data.groupby('product_id')['add_to_cart_order'].mean().reset_index(name = 'mean_position')
    mean_position.sort_values(by = 'product_id', inplace = True)
    product_features['avg_pos_incart'] = mean_position['mean_position']
    
    
    
    #generate boolean values if product belongs to below categories
    products['organic'] = products['product_name'].apply(lambda x: 'organic' in x.lower()).astype(int)
    products['isYogurt'] = products['aisle_id'].apply(lambda x: x==120).astype(int)

    products['isProduce'] = products['department_id'].apply(lambda x: x==4).astype(int)
    products['isFrozen'] = products['department_id'].apply(lambda x: x==1).astype(int)
    products['isdairy'] = products['department_id'].apply(lambda x: x==16).astype(int)
    products['isbreakfast'] = products['department_id'].apply(lambda x: x==14).astype(int)
    products['issnack'] = products['department_id'].apply(lambda x: x==19).astype(int)
    products['isbeverage'] = products['department_id'].apply(lambda x: x==7).astype(int)

    new_product_feat = products[['organic', 'isYogurt', 'isProduce', 'isFrozen', 'isdairy', 'isbreakfast', 'issnack', 'isbeverage']]
    
    #reduce sparsity using NMF
    #ref:https://www.kaggle.com/themissingsock/matrix-decomposition-with-buyer-data
    from sklearn.decomposition import NMF
    from sklearn.preprocessing import normalize

    nmf = NMF(n_components = 3)
    model = nmf.fit(new_product_feat)
    W = model.transform(new_product_feat)
    prod_data = pd.DataFrame(normalize(W))

    prod_data.columns = ['p_reduced_feat_1', 'p_reduced_feat_2','p_reduced_feat_3']
    products.drop(['organic', 'isYogurt', 'isProduce', 'isFrozen', 'isdairy', 'isbreakfast', 'issnack', 'isbeverage'], axis = 1, inplace =True)

    product_features['p_reduced_feat_1'] = prod_data['p_reduced_feat_1']
    product_features['p_reduced_feat_2'] = prod_data['p_reduced_feat_2']
    product_features['p_reduced_feat_3'] = prod_data['p_reduced_feat_3']
    

    #Get aisle reorder rate
    df = prior_data.groupby(['aisle']).size().reset_index(name='order_count')
    aisle_reorder_rate = prior_data[prior_data['reordered']==1].groupby(['aisle']).size().reset_index(name='reorder_rate')
    df['aisle_reorder_rate'] = aisle_reorder_rate['reorder_rate']/df['order_count']
    df.drop(['order_count'], axis = 1, inplace = True)
    new_df = pd.merge(prior_data, df, on = 'aisle')
    
    
    #Get dept reorder rate
    df = prior_data.groupby(['department']).size().reset_index(name='order_count')
    aisle_reorder_rate = prior_data[prior_data['reordered']==1].groupby(['aisle']).size().reset_index(name='reorder_rate')
    df['dept_reorder_rate'] = aisle_reorder_rate['reorder_rate']/df['order_count']
    df.drop(['order_count'], axis = 1, inplace = True)
    new_df = pd.merge(new_df, df, on = 'department')
    
    new_df = new_df[['product_id','aisle_id','department_id','aisle_reorder_rate','dept_reorder_rate']]
    new_df.drop_duplicates(keep='first', inplace = True)

    #merge dept_reorder_rate and aisle_reorder_rate to existing product features
    product_features = pd.merge(product_features, new_df , on='product_id', how = 'inner')
    
    del df, new_df, new_df_1, new_product_feat, model, prod_data
    return product_featuresdef generate_product_features(prior_data = None):
    
    """
    Generate Product based features and return it as dataframe object.
    Later this dataframe will be merged with other dataframe to generate training data
    
    Features:
    feat_1 : product_reorder_rate       : How Frequently the product was reordered ?
    feat_2 : avg_pos_incart             : Average position of product in the cart ?
    
    next 3 values are calculated based product being 
        - organic, 
        - isYogurt - aisle
        - produce  - department
        - isFrozen  - department 
        - isdairy  - department
        - isbreakfast  - department 
        - issnack  - department
        - isbeverage  - department
    these values are then reduced to 3 columns using Non-Negative Matrix Factorization, to reduce sparsity
        
    feat_3 : p_reduced_feat_1             : column 1 from NMF output
    feat_4 : p_reduced_feat_2             : column 2 from NMF output
    feat_5 : p_reduced_feat_3             : column 3 from NMF output
    feat_6 : aisle_reorder_rate           : How frequently a product is reordered from the aisle to which this product belongs
    feat_7 : department_reorder_rate      : How frequently a product is reordered from the department to which this product belongs
    
    
    """
    
    #create an empty dataframe
    product_features = pd.DataFrame(columns=['product_id'])
    
    #add product_name
    product_features['product_id'] = prior_data['product_id'].sort_values().unique()
    
    #get reorder_rate for each product
    #reorder_rate = reorders / total orders
    df = pd.DataFrame({'reorder_rate': prior_data.groupby(['product_id','reordered'])['reordered'].\
                                                       count().groupby(level=0).\
                                                       apply(lambda x: x / float(x.sum()))}).reset_index()

    #get data of reordered products only
    new_df = df[df['reordered']==1]
    new_df['reorder_rate'] = new_df['reorder_rate'] * new_df['reordered']
    
    #handling for products which were never reordered, hence reorder_rate = 0.0
    new_df_1 = df[(df['reordered']==0) & (df['reorder_rate']==float(1.0))]
    new_df_1['reorder_rate'] = new_df_1['reorder_rate'] * new_df_1['reordered']
    new_df = new_df.append(new_df_1)
    
    #drop other columns of the new_df and sort values by product name to align with product features dataframe
    new_df.drop('reordered', axis = 1, inplace = True)
    new_df.sort_values(by='product_id', inplace =  True)   
    new_df = new_df.reset_index(drop = True)
    
    #add to feat_1 of product_features dataframe
    product_features['product_reorder_rate'] = new_df['reorder_rate']
    
    #get mean position of product in the cart, sort by product_name and add to feat_2 of product_features
    mean_position = prior_data.groupby('product_id')['add_to_cart_order'].mean().reset_index(name = 'mean_position')
    mean_position.sort_values(by = 'product_id', inplace = True)
    product_features['avg_pos_incart'] = mean_position['mean_position']
    
    
    
    #generate boolean values if product belongs to below categories
    products['organic'] = products['product_name'].apply(lambda x: 'organic' in x.lower()).astype(int)
    products['isYogurt'] = products['aisle_id'].apply(lambda x: x==120).astype(int)

    products['isProduce'] = products['department_id'].apply(lambda x: x==4).astype(int)
    products['isFrozen'] = products['department_id'].apply(lambda x: x==1).astype(int)
    products['isdairy'] = products['department_id'].apply(lambda x: x==16).astype(int)
    products['isbreakfast'] = products['department_id'].apply(lambda x: x==14).astype(int)
    products['issnack'] = products['department_id'].apply(lambda x: x==19).astype(int)
    products['isbeverage'] = products['department_id'].apply(lambda x: x==7).astype(int)

    new_product_feat = products[['organic', 'isYogurt', 'isProduce', 'isFrozen', 'isdairy', 'isbreakfast', 'issnack', 'isbeverage']]
    
    #reduce sparsity using NMF
    #ref:https://www.kaggle.com/themissingsock/matrix-decomposition-with-buyer-data
    from sklearn.decomposition import NMF
    from sklearn.preprocessing import normalize

    nmf = NMF(n_components = 3)
    model = nmf.fit(new_product_feat)
    W = model.transform(new_product_feat)
    prod_data = pd.DataFrame(normalize(W))

...     prod_data.columns = ['p_reduced_feat_1', 'p_reduced_feat_2','p_reduced_feat_3']
...     products.drop(['organic', 'isYogurt', 'isProduce', 'isFrozen', 'isdairy', 'isbreakfast', 'issnack', 'isbeverage'], axis = 1, inplace =True)
... 
...     product_features['p_reduced_feat_1'] = prod_data['p_reduced_feat_1']
...     product_features['p_reduced_feat_2'] = prod_data['p_reduced_feat_2']
...     product_features['p_reduced_feat_3'] = prod_data['p_reduced_feat_3']
...     
... 
...     #Get aisle reorder rate
...     df = prior_data.groupby(['aisle']).size().reset_index(name='order_count')
...     aisle_reorder_rate = prior_data[prior_data['reordered']==1].groupby(['aisle']).size().reset_index(name='reorder_rate')
...     df['aisle_reorder_rate'] = aisle_reorder_rate['reorder_rate']/df['order_count']
...     df.drop(['order_count'], axis = 1, inplace = True)
...     new_df = pd.merge(prior_data, df, on = 'aisle')
...     
...     
...     #Get dept reorder rate
...     df = prior_data.groupby(['department']).size().reset_index(name='order_count')
...     aisle_reorder_rate = prior_data[prior_data['reordered']==1].groupby(['aisle']).size().reset_index(name='reorder_rate')
...     df['dept_reorder_rate'] = aisle_reorder_rate['reorder_rate']/df['order_count']
...     df.drop(['order_count'], axis = 1, inplace = True)
...     new_df = pd.merge(new_df, df, on = 'department')
...     
...     new_df = new_df[['product_id','aisle_id','department_id','aisle_reorder_rate','dept_reorder_rate']]
...     new_df.drop_duplicates(keep='first', inplace = True)
... 
...     #merge dept_reorder_rate and aisle_reorder_rate to existing product features
...     product_features = pd.merge(product_features, new_df , on='product_id', how = 'inner')
...     
...     del df, new_df, new_df_1, new_product_feat, model, prod_data
