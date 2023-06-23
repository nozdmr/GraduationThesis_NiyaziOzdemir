import pandas as pd #import pandas library
import plotly.graph_objects as go #import plotly graph_objects

df = pd.read_csv('C:\\Users\\niyaz\\Desktop\\supermarket_sales - Sheet1.csv') #csv file uploaded

df["gross income categorized"] = ""             #categorize gross income
for index, row in df.iterrows():
    gross_income = row["gross income"]
    
    if 0 <= gross_income <= 10:
        df.at[index, "gross income categorized"] = "0-10"
    elif 10 < gross_income <= 20:
        df.at[index, "gross income categorized"] = "10-20"
    elif 20 < gross_income <= 30:
        df.at[index, "gross income categorized"] = "20-30"
    elif gross_income > 30:
        df.at[index, "gross income categorized"] = "30+"


df["Date"] = pd.to_datetime(df["Date"])
df['Month'] = df['Date'].apply(lambda x: x.strftime('%B'))  #Month information column was created from date information with the help of pandas.to_datetime
 

df_temp1= df.groupby(["Product line", "Gender"])["Total"].sum().reset_index() #groupby for source-target and value 
df_temp1.columns= ["source", "target", "value"]  #for first part source= Product Line, target= gender 

df_temp2= df.groupby(["Gender", "Payment"])["Total"].sum().reset_index() 
df_temp2.columns= ["source", "target", "value"]  #for the second part source=gender, target= Payment

df_temp3= df.groupby(["Payment", "Customer type"])["Total"].sum().reset_index()
df_temp3.columns= ["source", "target", "value"]  

df_temp4= df.groupby(["Customer type", "City"])["Total"].sum().reset_index()
df_temp4.columns= ["source", "target", "value"]

df_temp5= df.groupby(["City","Month"])["Total"].sum().reset_index()
df_temp5.columns= ["source", "target", "value"]

df_temp6= df.groupby(["Month", "gross income categorized"])["Total"].sum().reset_index()
df_temp6.columns=["source", "target", "value"]

links= pd.concat([df_temp1, df_temp2, df_temp3, df_temp4, df_temp5, df_temp6], axis=0)  # for row by row join axis=0
links["color"]= [ "aqua", "aqua",
                  "chartreuse", "chartreuse",
                  "burlywood","burlywood",
                  "darkorange", "darkorange",
                  "indigo", "indigo",
                  "gold", "gold",
                  "fuchsia", "fuchsia", "fuchsia",
                  "navy", "navy", "navy",
                  "springgreen", "springgreen",
                  "sandybrown", "sandybrown",
                  "slategray", "slategray",
                  "olive", "olive", "olive",
                  "maroon", "maroon", "maroon",
                  "salmon", "salmon", "salmon",
                  "powderblue", "powderblue", "powderblue",
                  "seagreen", "seagreen", "seagreen",
                  "yellowgreen", "yellowgreen", "yellowgreen", "yellowgreen",
                  "turquoise", "turquoise", "turquoise", "turquoise",
                  "violet", "violet", "violet", "violet"               
                 ]

unique_source_target = list(pd.unique(links[["source", "target"]].values.ravel("K")))  #make list with source and target's unique values
mapping_dict = {k: v for v, k in enumerate(unique_source_target) }  #for mapping

links["source"]= links["source"].map(mapping_dict)
links["target"]= links["target"].map(mapping_dict)  #mapping source and target's unique values

links_dict= links.to_dict(orient="list")  #Makes dictionary, the rows of the columns in the links

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
        'text': "Supermarket Sales Analysis with Sankey Diagram",
        'x': 0.5,  # Position of the header on the x-axis (in the range 0-1)
        'y': 0.95,  # Position of the header on the y-axis (in the range 0-1)
        'xanchor': 'center',  
        'yanchor': 'top',  
        'font': {
            'size': 20,  # font size
            'color': 'blue',  # font color
           
        }
    },
    font_size=15,
     annotations=[
        dict(
            x=0,  #  position x (0-1)
            y=-0.03,  # position y (0-1)
            xref="paper",
            yref= "paper",
            text='<i>Product Type<i>',  # text
            showarrow=False,  # no arrow
            font=dict(size=15, color="black")  # font size
        ),
        dict(
            x=0.165,  
            y=-0.03,  
            xref="paper",
            yref= "paper",
            text='<i>Gender<i>',  
            showarrow=False,  
            font=dict(size=15, color="black")  
        ),
        dict(
            x=0.367,  
            y=-0.03,  
            xref="paper",
            yref= "paper",
            text='<i>Payment Method<i>',  
            showarrow=False,  
            font=dict(size=15, color="black")  
        ),
        dict(
            x=0.520,  
            y=-0.03,  
            xref="paper",
            yref= "paper",
            text='<i>Membership<i>',  
            showarrow=False,  
            font=dict(size=15, color="black")  
        ),
        dict(
            x=0.68,  
            y=-0.03,  
            xref="paper",
            yref= "paper",
            text='<i>City<i>',  
            showarrow=False,  
            font=dict(size=15, color="black")  
        ),
        dict(
            x=0.85,  
            y=-0.03,  
            xref="paper",
            yref= "paper",
            text='<i>Month<i>',  
            showarrow=False,  
            font=dict(size=15, color="black")  
        ),
        dict(
            x=1,  
            y=-0.03,  
            xref="paper",
            yref= "paper",
            text='<i>Gross Income($)<i>',  
            showarrow=False,  
            font=dict(size=15, color="black") 
        ),
     ]   
)

fig.show()