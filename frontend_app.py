#### Import libraries ####

from tkinter import *
import tkinter as tk
from tkinter import ttk
import pandas as pd
from functionality import*
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#### Importing the data ####
def data_import():
    
    global data
    
    data = pd.read_parquet("Fulldata.parquet")

#### Data cleaning for better results ####
def data_clean():
    
    global data
    
    merge_data(data,'customer_group','NOT MAPPED','Others')
    fill_nulls_with(data,'customer_group','Others')
    drop_nulls_in_column(data,'PRH4')

    #### List of columns to be dropped ####
    list_drop_columns = ['region','order_material_net_value'] 

    drop_columns(data,list_drop_columns)
    data = explode_data(data,'PRH4')

    #### Dictionary of items to be changed in a column with key being the item and value being the replacement ####
    change_dict = {'Customized':'Customizable',                       
                'Instruments + Auxiliaries GBR':'Instruments',
                'Miscellaneous + Others':'Other',
                'Other Implants':'Other',
                'Other Orthodontics':'Other',
                'Other Prosthetics':'Other',
                'Other Restorative Solutions':'Other',
                'Other Services':'Other',
            'Other Software + License':'Other',
            'Digital Accessories + Others':'Other',
            'standard':'Other',
            'standard EXT':'Other',
            'standard TF':'Other',
            'hydrophilic TF':'hydrophilic'}
    
    merge_multiple_data(data,'PRH4',change_dict)
    
    
def fetch():
    
    global treeview
    
    #### If treeview exists forget the treeview ####
    if 'treeview' in globals() and treeview.winfo_exists():
        treeview.pack_forget()
    
    #### Fetching user inputs ####    
    set_sales_channel = entry_sales_channel.get()
    set_customer_group = entry_customer_group.get()
    set_dso_status = entry_dso_status.get()
    set_product = entry_product.get()
    
    #### Filtering data on columns according to entries ####
    data_cycle = data.copy()
    
    if set_sales_channel != 'All':
        data_cycle = data[data['sales_channel'] == set_sales_channel]
           
    if set_customer_group != 'All':
        data_cycle = data_cycle[data_cycle['customer_group'] == set_customer_group]
        
    if set_dso_status != 'All':
        data_cycle = data_cycle[data_cycle['DSO_Ind'] == set_dso_status]  
        
    #### Converting data to buying pattern table where if a customer bought the product value is 1 or else 0 ####
    df_basket_input = pd.crosstab(data_cycle['customer_number'], data_cycle['PRH4']).map(encode)
    
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
    
    else:
        df_filtered = df_mba[['consequents', 'confidence']].round(2)    
    
    #### Creating the recommendation view in app #### 
    columns_to_display = df_filtered.columns.tolist()
    treeview = ttk.Treeview(frame_suggestion, columns=columns_to_display, show="headings")
    populate_treeview(treeview, df_filtered)
    treeview.pack(pady=5)
   
def populate_treeview(treeview, dataframe):
    
    treeview.delete(*treeview.get_children()) #### Remove existing rows form the Treeview ####
    
    for index,row in dataframe.iterrows():
        treeview.insert("", "end", values=list(row)) #### Inserting data into the Treeview ####
    
#### Window ####
def app():
    
    global entry_sales_channel
    global entry_customer_group
    global entry_dso_status
    global entry_product
    global window 
    global frame_suggestion
    
    bg_colour = '#2f3030'
    fg_colour = '#419977'
    window = tk.Tk()
    window.title('Straumann Group Recommender')
    window.geometry("720x400")
    window.minsize(720,400)
    #small_icon = tk.PhotoImage(file="taxi_small.png")
    #large_icon = tk.PhotoImage(file="taxi_big.png")
    #window.iconphoto(False, large_icon, small_icon)
    window.configure(bg= bg_colour)
    
    label_title = Label(text = 'PRODUCT RECOMMENDATION', bg = bg_colour,fg = fg_colour,font=("Arial",25,"bold"))
    label_title.grid(row=0,column=0,columnspan=20,ipadx=100)
    
    frame_title = Frame(bg= bg_colour, relief=RAISED,highlightbackground= fg_colour, highlightthickness=2)
    frame_title.grid(row=0,column=0,columnspan=20)
    frame_selection = Frame(bg= bg_colour, relief=RAISED,highlightbackground= fg_colour, highlightthickness=2)
    frame_selection.grid(row=1,column=0,columnspan=10)
    frame_suggestion = Frame(bg=bg_colour,relief=RAISED,highlightbackground= fg_colour, highlightthickness=2)
    frame_suggestion.grid(row=1,column=13,columnspan=10)
    
    label_title = Label(frame_title,text = 'PRODUCT RECOMMENDATION', bg = bg_colour,fg = fg_colour,font=("Arial",25,"bold"))
    label_title.grid(row=0,column=0,columnspan=20,ipadx=100)
    
    label_suggestion = Label(frame_suggestion,text='Suggestions',bg= bg_colour,fg= fg_colour,font=("Arial",15,"bold"))
    label_suggestion.pack()

    label_sales_channel = Label(frame_selection,text='Sales Channel',bg = bg_colour,fg = fg_colour,font=("Arial",15,"bold"))
    label_sales_channel.pack()
    
    options_sales_channel = ['All'] + data['sales_channel'].unique().tolist()
    print(options_sales_channel)
    entry_sales_channel = ttk.Combobox(frame_selection, width = 27,values= options_sales_channel)
    entry_sales_channel.pack(pady=5)
    entry_sales_channel.current(0)  

    label_customer_group = Label(frame_selection,text='Customer Group',bg= bg_colour,fg= fg_colour,font=("Arial",15,"bold"))
    label_customer_group.pack()

    options_customer_group = ['All'] + data['customer_group'].unique().tolist()
    print(options_customer_group)
    entry_customer_group = ttk.Combobox(frame_selection, width = 27, values= options_customer_group)
    entry_customer_group.pack(pady=5)
    entry_customer_group.current(0)  

    label_dso_status = Label(frame_selection,text='DSO Status',bg= bg_colour,fg=fg_colour,font=("Arial",15,"bold"))
    label_dso_status.pack()

    options_dso_status = ['All'] + data['DSO_Ind'].unique().tolist()
    print(options_dso_status)
    entry_dso_status = ttk.Combobox(frame_selection, width = 27, values= options_dso_status)
    entry_dso_status.pack(pady=5)
    entry_dso_status.current(0)
    
    label_product = Label(frame_selection,text='PRODUCT',bg= bg_colour,fg=fg_colour,font=("Arial",15,"bold"))
    label_product.pack()

    options_product = ['All'] + data['PRH4'].unique().tolist()
    entry_product = ttk.Combobox(frame_selection, width = 27, values= options_product)
    entry_product.pack(pady=5)
    entry_product.current(0)    
    
    Predict_button = Button(frame_selection,text='PREDICT',width=15,font=("Arial",14),bg= fg_colour,fg="white",command=fetch)
    Predict_button.pack(pady=5)

    window.mainloop()

def main():
    data_import()
    data_clean()
    app()

if __name__ == "__main__":
    
    main()