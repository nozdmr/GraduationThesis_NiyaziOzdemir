import pandas as pd
import plotly.graph_objects as go

df = pd.read_excel('C:\\Users\\niyaz\\Desktop\\finansal.xlsx', sheet_name= "Anonymized Original with Catego")

df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
df["Year"]=df["Transaction Date"].dt.year

print(df.isnull().any())

df.dropna(subset=["Transaction Type"], inplace=True)
df.dropna(subset=["Category"], inplace=True)
df.dropna(subset=["Location Country"], inplace=True)
df.dropna(subset=["Debit Amount"], inplace=True)


df_temp1= df.groupby(["Year", "Category"])["Debit Amount"].sum().reset_index()
df_temp1.columns= ["source", "target", "value"]

df_temp2= df.groupby(["Category", "Transaction Type"])["Debit Amount"].sum().reset_index()
df_temp2.columns= ["source", "target", "value"]

df_temp3= df.groupby(["Transaction Type", "Location Country"])["Debit Amount"].sum().reset_index()
df_temp3.columns= ["source", "target", "value"]

links= pd.concat([df_temp1, df_temp2, df_temp3], axis=0)  
links["color"]= [ "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", "aqua", #2015
                  "burlywood","burlywood", "burlywood","burlywood", "burlywood","burlywood", "burlywood","burlywood", "burlywood","burlywood", "burlywood","burlywood", "burlywood","burlywood", #2016
                  "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", "chartreuse", #2017
                  "darkorange", "darkorange","darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", "darkorange", #2018
                  "indigo", "indigo","indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", #2019
                  "gold", "gold","gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", "gold", #2020
                  "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", "fuchsia", #2021
                  "navy", "navy", "navy","navy", "navy", "navy","navy", "navy", "navy","navy", "navy", "navy","navy", "navy", "navy","navy", "navy", #2022
                  "aqua", #account transfer
                  "orange","orange", #amazon
                  "yellow", "yellow", "yellow","yellow", "yellow", #bills
                  "darkgreen","darkgreen", "darkgreen", #cash
                  "peru", #clothes
                  "violet", #dine out 
                  "turquoise", "turquoise", "turquoise", #entertainment
                 "slategray", "slategray",  #fitness
                 "seagreen", #groceries1 
                 "seagreen", #groceries2
                  "maroon", #health
                  "pink", "pink", "pink", "pink", #home improvement
                  "yellowgreen", #hotels
                  "gold", "gold", "gold", #insurance
                  "darkorchid","darkorchid", "darkorchid", "darkorchid", #invesment
                  "burlywood", "burlywood", "burlywood", #mortgage
                  "olive", "olive", "olive", #other shopping
                  "sandybrown","sandybrown", "sandybrown", #others 
                  "chocolate", #purchase of uk
                  "darkmagenta", #rent
                  "black", #safety deposit 
                  "navy", "navy", "navy", "navy", #savings
                   "fuchsia","fuchsia", "fuchsia", "fuchsia", #services
                  "springgreen", #services/hpme 
                   "red", "red", #supplementary income
                  "powderblue", #travel
                  "darkkhaki",  #bp
                  "gold", #chq
                  "chartreuse",  #cpt
                  "salmon", #dd
                  "navy", "navy", "navy", "navy", "navy", "navy", "navy", "navy", "navy", "navy", "navy", "navy", "navy", "navy", "navy",  #deb
                  "black", # FEE
                  "olive", #FPO
                  "chocolate", #PAY
                  "orange", #SO
                  "red" #tfr
                  
                 ]


unique_source_target = list(pd.unique(links[["source", "target"]].values.ravel("K")))  

mapping_dict = {k: v for v, k in enumerate(unique_source_target) } 


links["source"]= links["source"].map(mapping_dict)
links["target"]= links["target"].map(mapping_dict)  



links_dict= links.to_dict(orient="list")   



fig = go.Figure(data=[go.Sankey(
    
    node= dict(
        pad=20,
        thickness= 20,
        line= dict(color= "black", width=0.5),
        label= unique_source_target,
        color="blue"
    ),
    link= dict(
        source = links_dict["source"],
        target = links_dict["target"],
        value = links_dict["value"],
        color= links["color"]
    )
)]
)

fig.update_layout(
     title={
        'text': "Financial Analysis with Sankey Diagram",
        'x': 0.5,  # Position of the header on the x-axis (in the range 0-1)
        'y': 0.95,  # Position of the header on the y-axis (in the range 0-1)
        'xanchor': 'center', 
        'yanchor': 'top',  
        'font': {
            'size': 20,  
            'color': 'blue', 
           
        }
    },
    font_size=16,
     annotations=[
        dict(
            x=0,  # position x (range between 0-1)
            y=-0.05,  # position y (range between 0-1)
            xref="paper",
            yref= "paper",
            text='<i>Year<i>',  # text
            showarrow=False,  # no arrow
            font=dict(size=15, color="black")  # font size
        ),
        dict(
            x=0.35,  
            y=-0.05,  
            xref="paper",
            yref= "paper",
            text='<i>Category<i>',  
            showarrow=False,  
            font=dict(size=15, color="black")  
        ),
        dict(
            x=0.70,  
            y=-0.05,  
            xref="paper",
            yref= "paper",
            text='<i>Transaction Type<i>',  
            showarrow=False,  
            font=dict(size=15, color="black")  
        ),
        dict(
            x=0.99,  
            y=-0.05,  
            xref="paper",
            yref= "paper",
            text='<i>Country<i>',  
            showarrow=False,  
            font=dict(size=15, color="black") 
        ),
    ]
)       
fig.show()
