#### Import libraries ####
import streamlit as st
import pandas as pd
from functionality import*
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#### Importing the data ####
@st.cache_data
def data_import():
    data = pd.read_parquet("Fulldata.parquet")
    return data

#### Data cleaning for better results ####
@st.cache_data
def data_clean(data):
    
    merge_data(data,'customer_group','NOT MAPPED','Others')
    fill_nulls_with(data,'customer_group','Others')
    drop_nulls_in_column(data,'PRH4')

    #### List of columns to be dropped ####
    list_drop_columns = ['region','order_material_net_value'] 
    drop_columns(data, list_drop_columns)
    data = explode_data(data, 'PRH4')

    #### Dictionary of items to be changed in a column with key being the item and value being the replacement ####
    change_dict = {
        'Customized': 'Customizable',
        'Instruments + Auxiliaries GBR': 'Instruments',
        'Miscellaneous + Others': 'Other',
        'Other Implants': 'Other',
        'Other Orthodontics': 'Other',
        'Other Prosthetics': 'Other',
        'Other Restorative Solutions': 'Other',
        'Other Services': 'Other',
        'Other Software + License': 'Other',
        'Digital Accessories + Others': 'Other',
        'standard': 'Other',
        'standard EXT': 'Other',
        'standard TF': 'Other',
        'hydrophilic TF': 'hydrophilic'
    }
    merge_multiple_data(data, 'PRH4', change_dict)
    options_sales_channel = ['All'] + data['sales_channel'].unique().tolist()
    options_customer_group = ['All'] + data['customer_group'].unique().tolist()
    options_dso_status = ['All'] + data['DSO_Ind'].unique().tolist()
    options_product = ['All'] + data['PRH4'].unique().tolist()
    
    return data, options_sales_channel, options_customer_group, options_dso_status, options_product

def fetch(data):
    
    global df_filtered
    
    #### Fetching user inputs ####    
    set_sales_channel = option_sales_channel
    set_customer_group = option_customer_group
    set_dso_status = option_dso_status
    set_product = option_product
    
    #### Filtering data on columns according to entries ####
    data_cycle = data.copy()
    
    if set_sales_channel != 'All':
        data_cycle = data[data['sales_channel'] == set_sales_channel]
           
    if set_customer_group != 'All':
        data_cycle = data_cycle[data_cycle['customer_group'] == set_customer_group]
        
    if set_dso_status != 'All':
        data_cycle = data_cycle[data_cycle['DSO_Ind'] == set_dso_status]  
        
    #### Converting data to buying pattern table where if a customer bought the product value is 1 or else 0 ####
    df_basket_input = pd.crosstab(data_cycle['customer_number'], data_cycle['PRH4']).applymap(encode)
    
    #### Apriori Algotithm ####
    frequent_itemsets = apriori(df_basket_input, min_support=0.02, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift")
    df_mba = rules.sort_values(["support", "confidence","lift"],axis = 0, ascending = False).reset_index()
    df_mba.drop(columns=['index'],inplace=True)

    #### Filtering out recommendations according to the product chosen buy customer #### 
    if set_product != 'ALL':
        
        df_filtered = df_mba[df_mba['antecedents'] == {set_product}].reset_index()
        df_filtered.drop(columns=['index'],inplace=True)
        df_filtered = df_filtered[['consequents','confidence']].round(2)
        df_filtered = df_filtered[df_filtered['consequents'].apply(lambda x: len(x) <= 1)]
        df_filtered['consequents'] = df_filtered['consequents'].apply(lambda x: ', '.join(map(str, x)))
        df_filtered = df_filtered.loc[df_filtered['consequents'] != 'Other' ]
        df_filtered.reset_index(inplace=True,drop=True)
        df_filtered = df_filtered.head(10)
    
    else:
        df_filtered = df_mba[['consequents', 'confidence']].round(2)
        
    if df_filtered.empty:
        df_filtered = df_mba[['consequents', 'confidence']].round(2)

    return df_filtered  


def app(data,options_sales_channel, options_customer_group, options_dso_status, options_product):
    
    global option_sales_channel
    global option_customer_group
    global option_dso_status
    global option_product
    
    st.image("Strauman_group_band.png")
    st.title(":greenProduct Recommender")
    st.subheader("Enter customer and product details to get recommendation")

    st.header("SALES CHANNEL")
    option_sales_channel = st.selectbox(
        "Select an option",
        options_sales_channel,
        index=0,
        placeholder="Select Sales Channel..."
    )

    st.write("You selected:", option_sales_channel)
    
    st.header("CUSTOMER GROUP")
    option_customer_group = st.selectbox(
        "Select an option",
        options_customer_group,
        index=0,
        placeholder="Select Customer Group..."
    )

    st.write("You selected:", option_customer_group)
    
    st.header("DSO STATUS")
    option_dso_status = st.selectbox(
        "Select an option",
        options_dso_status,
        index=0,
        placeholder="Select DSO Status..."
    )

    st.write("You selected:", option_dso_status)
    
    st.header("PRODUCT")
    option_product = st.selectbox(
        "Select an option",
        options_product,
        index=0,
        placeholder="Select Product..."
    )

    st.write("You selected:", option_product)
    
    recommend = st.button('RECOMMEND')
    
    if recommend:
        fetch(data)
        st.header("RECOMMENDATIONS")
        st.dataframe(df_filtered,width= 500, height=390)
        

def main():
    data = data_import()
    data, options_sales_channel,options_customer_group, options_dso_status, options_product = data_clean(data)
    app(data,options_sales_channel, options_customer_group, options_dso_status, options_product)

if __name__ == "__main__":
    main()
