import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

import plotly.graph_objects as go
import plotly.express as px

import warnings
warnings.filterwarnings("ignore")

# import wordcloud
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def app():
    @st.cache
    def data_work():
        data=pd.read_csv('dataset.csv')
        data.columns=['SNo', 'Date', 'StartupName', 'IndustryVertical', 'SubVertical',
            'CityLocation', 'InvestorsName', 'InvestmentType', 'AmountInUSD',
            'Remarks']
        data['StartupName'] = data['StartupName'].apply(lambda x: (str(x).replace("\\\\","")))
        data['StartupName'] = data['StartupName'].apply(lambda x: (str(x).replace("\"","")))
        data.drop("Remarks", axis=1, inplace=True)

        print("Run Started")        
        for i in range(0,len(data["IndustryVertical"])):
            if data["IndustryVertical"][i] in ["ECommerce",
                                            "ecommerce",
                                            "Ecommerce", 
                                            "E-Commerce",
                                            "E-commerce"]:
                data["IndustryVertical"][i]="eCommerce"
                
        for i in range(0,len(data["StartupName"])):
            if data["StartupName"][i] in ["Ola",
                                        "Ola Cabs", 
                                        "Olacabs"]:
                data["StartupName"][i]="Ola"  
            elif data["StartupName"][i] =="Flipkart.com":
                data["StartupName"][i]="Flipkart"    
            elif data["StartupName"][i] =="Paytm Marketplace":
                data["StartupName"][i]="Paytm"   
        for i in range(0,len(data["StartupName"])):
            if data["InvestorsName"][i] in ['Undisclosed investors',
                                        'Undisclosed Investors',
                                        'Undisclosed',
                                        'Undisclosed investor',
                                        'Undisclosed Investor',
                                        'undisclosed investors']:
                data["InvestorsName"][i]="Undisclosed"
            
        for i in range(0,len(data["StartupName"])):
            if data["StartupName"][i] in ["OYO",
                                        "OYO Rooms", 
                                        "OyoRooms", 
                                        "Oyorooms", 
                                        "Oyo",
                                        "Oyo Rooms"]:
                data["StartupName"][i]= "OYO Rooms"
            elif data["StartupName"][i] in ["Byjuxe2x80x99s",
                                            "BYJU'S"]:
                data["StartupName"][i]= "Byju's"    
            
        for i in range  (0,len(data["CityLocation"])):
            if data["CityLocation"][i] in ["New Delhi",
                                        "Delhi",
                                        "Noida", 
                                        "Gurugram",
                                        "Gurgaon"]:
                data["CityLocation"][i]="NCR"
            elif data["CityLocation"][i]=="Bangalore":
                data["CityLocation"][i]="Bengaluru"

        for i in range(0, len(data["InvestmentType"])):
            if data["InvestmentType"][i] in ["Seed/ Angel Funding","Seed / Angel Funding","Seed/Angel Funding",
                                       "Seed / Angle Funding", "Angel / Seed Funding"]:
                data["InvestmentType"][i]="Seed/Angel Funding"


        data.loc[data['CityLocation'].isin(['\\\\xc2\\\\xa0Noida', '\\xc2\\xa0Noida']), 'CityLocation'] = 'Noida'
        data.loc[data['CityLocation'].isin(['\\\\xc2\\\\xa0Bangalore', '\\xc2\\xa0Bangalore', 'Bangalore']), 'CityLocation'] = 'Bengaluru'
        data.loc[data['CityLocation'].isin(['\\\\xc2\\\\xa0New Delhi', '\\xc2\\xa0New Delhi']), 'CityLocation'] = 'New Delhi'
        data.loc[data['CityLocation'].isin(['\\\\xc2\\\\xa0Gurgaon', 'Gurugram']), 'CityLocation'] = 'Gurgaon'
        data.loc[data['CityLocation'].isin(['\\\\xc2\\\\xa0Mumbai', '\\xc2\\xa0Mumbai']), 'CityLocation'] = 'Mumbai'
        

        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0News Aggregator mobile app", 'IndustryVertical'] = 'News Aggregator mobile app'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Online Jewellery Store", 'IndustryVertical'] = 'Online Jewellery Store'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Fashion Info Aggregator App", 'IndustryVertical'] = 'Fashion Info Aggregator App'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Online Study Notes Marketplace", 'IndustryVertical'] = 'Online Study Notes Marketplace'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Warranty Programs Service Administration", 'IndustryVertical'] = 'Warranty Programs Service Administration'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Pre-School Chain", 'IndustryVertical'] = 'Pre-School Chain'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Premium Loyalty Rewards Point Management", 'IndustryVertical'] = 'Premium Loyalty Rewards Point Management'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Contact Center Software Platform", 'IndustryVertical'] = 'Contact Center Software Platform'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Casual Dining restaurant Chain", 'IndustryVertical'] = 'Casual Dining restaurant Chain'
        data.loc[data['IndustryVertical'] == "\\\\xc2\\\\xa0Online Grocery Delivery", 'IndustryVertical'] = 'Online Grocery Delivery'
        data.loc[data['IndustryVertical'] == "Online home d\\\\xc3\\\\xa9cor marketplace", 'IndustryVertical'] = 'Online home decor marketplace'
        data.loc[data['IndustryVertical'].isin(["Fin-Tech"]), 'IndustryVertical'] = 'FinTech'   

        data.loc[data['InvestorsName'].isin(['Undisclosed investors', 'Undisclosed', 'undisclosed investors', 'Undisclosed Investor', 'Undisclosed investors']), 'InvestorsName'] = 'Undisclosed Investors'
        data.loc[data['InvestorsName'] == "\\\\xc2\\\\xa0Tiger Global", 'InvestorsName'] = 'Tiger Global'
        data.loc[data['InvestorsName'] == "\\\\xc2\\\\xa0IndianIdeas.com", 'InvestorsName'] = 'IndianIdeas'
        data.loc[data['InvestorsName'] == "\\\\xc2\\\\xa0IvyCap Ventures, Accel Partners, Dragoneer Investment Group", 'InvestorsName'] = 'IvyCap Ventures, Accel Partners, Dragoneer Investment Group'
        data.loc[data['InvestorsName'] == "\\\\xc2\\\\xa0Goldman Sachs", 'InvestorsName'] = 'Goldman Sachs'        

        data.drop([2602,2603,2604,2605,2606,2607,2608,2609,2610,2611], inplace = True)
        data.reset_index(drop=True, inplace=True)

        for i in range (0, len(data["AmountInUSD"])):
            data["AmountInUSD"][i]=re.sub('\D',"",str(data["AmountInUSD"][i]))

        data["AmountInUSD"]=pd.to_numeric(data["AmountInUSD"])

        for i in range (0, len(data["StartupName"])):
            data["StartupName"][i]=re.sub('xc2xa0',"",str(data["StartupName"][i]))

        data["AmountInUSD"][data["StartupName"]=="Rapido Bike Taxi"]=data["AmountInUSD"]/71.19
        temp1=data[["StartupName","AmountInUSD"]].groupby("StartupName").sum().sort_values(by="AmountInUSD", ascending=False)
        
        text=[]
        for i in range (0, len(data["SubVertical"])):
            if type(data["SubVertical"][i])==str:
                text.append(data["SubVertical"][i])
        
        text=" ".join(text) 
        text = text.split(" ")
        # text=set(text)
        text=" ".join(text) 

        return data, temp1, text
    st.write(" [Go Back](https://startupanalysis.wixsite.com/home/home)")
    st.title('Startups in India Visualization')
    st.text("""
    This dataset has funding information of the Indian startups from January 2015 
    till recent 2020. It includes columns with the date funded, the city the 
    startup is based out of, the names of the funders, and the amount invested (in USD).

    """)

    
    data, temp1, text=data_work()

    st.subheader('Industry Vertical Bar Graph ')
    top_filter = st.slider('Top N Industries', 3, 15, 5)  
    label=np.arange(0,top_filter)
    top=data["IndustryVertical"].value_counts().head(top_filter)
    fig=go.Figure(data=[go.Bar(y=top.values,x=top.index,marker={'color':top.values})])
    fig.update_layout(autosize=False ,plot_bgcolor='rgb(275, 275, 275)')
    fig.data[0].marker.line.width = 3
    fig.data[0].marker.line.color = "black"  
    st.plotly_chart(fig)
    


    st.subheader('Startups with Highest funding!')
    top_filter = st.slider('Top N Startups', 3, 15, 5)  # min: 3, max: 15, default: 5
    top=temp1.head(top_filter)
    label=np.arange(0,top_filter)
    fig=go.Figure(data=[go.Bar(y=top.AmountInUSD,x=top.index, marker={'color':label})])
    fig.update_layout(autosize=False ,plot_bgcolor='rgb(275, 275, 275)')
    fig.data[0].marker.line.width = 3
    fig.data[0].marker.line.color = "black" 
    st.plotly_chart(fig)
    st.write(" Investors from around the world have shown a growing interest in the Indian startup ecosystem, providing the necessary capital to fuel the growth of these companies.\n This has resulted in some of the largest funding rounds in the world, as investors seek to capitalize on the potential of India's rapidly growing market. The success of Indian startups with high funding can be attributed to a combination of factors, including the growing technology ecosystem, large market opportunity, and increasing availability of digital infrastructure and investment capital. From the above figure, we can figure out that as per 2020, Filpkart is having the highest funding of nearly 5 Billon USD and it is followed by Paytm with amount approximating to 3.2 Billion USD.")
    st.write("")
    st.write("")

    
    st.subheader('Pie-chart for top 7 different type of Fundings!')
    typ=data["InvestmentType"].value_counts().head(7)
    colrs = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    fig=go.Figure(data=[go.Pie(labels=typ.index,values=typ.values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=10,
                    marker=dict(colors=colrs), hole=.3,  pull=[0.1, 0,0, 0, 0, 0])                    
    fig.data[0].marker.line.width = 3
    fig.data[0].marker.line.color = "black"                
    fig.update_layout(height=600,autosize=False ,plot_bgcolor='rgb(275, 275, 275)')
    st.plotly_chart(fig)
    st.write("•	Seed funding: Seed funding is an initial capital provided to a startup to help get it off the ground. This type of funding is typically used to develop a prototype, build a team, and validate the business idea.")
    st.write("•	Angel funding: Angel funding is a type of funding provided by wealthy individuals or groups, known as angel investors. This funding is usually provided in the early stages of a startup and is often used to help the company scale and grow.")
    st.write("•	Venture capital: Venture capital is a type of funding provided by institutional investors, such as venture capital firms. This funding is usually provided to startups with high growth potential and is used to help the company expand and achieve its growth objectives.")
    st.write("•	Debt financing: Debt financing involves borrowing money from a lender, such as a bank or financial institution. This type of funding is usually used to finance specific projects or investments and is repaid with interest over a period of time.")
    st.write("•	Private equity: Private equity is a type of funding provided by investors who buy and own shares in private companies, typically with the goal of helping the company grow and eventually sell their shares at a profit.")
    st.write("•	Series A funding: Series A funding is a type of venture capital funding provided to startups that have already demonstrated market viability and are looking to scale their business.")
    st.write("•	Series B funding: Series B funding is a type of venture capital funding provided to startups that have already achieved significant growth and are looking to expand their operations or enter new markets.")
    st.write("")
    st.write("")

    st.subheader('Top Investors!')
    top_filter = st.slider('Top N Investors', 3, 10, 5)  # min: 3, max: 10, default: 5
    label=np.arange(0,top_filter)
    i=data['InvestorsName'].value_counts().head(top_filter+1).reset_index()
    i.columns=["InvestorsName", "Number"]
    i.drop(0,axis=0,inplace=True)
    fig=go.Figure(data=[go.Scatter(x=i.InvestorsName,y=i.Number,mode='markers',marker_size=(i.Number)*3, 
                     marker={'color':label})])
    fig.update_layout(autosize=False ,plot_bgcolor='rgb(275, 275, 275)')
    fig.data[0].marker.line.width = 3
    fig.data[0].marker.line.color = "black" 
    st.plotly_chart(fig)
    st.write("Ratan Tata: Ratan Tata is an Indian industrialist, philanthropist, and former chairman of Tata Sons, the holding company of the Tata Group. He is also an active angel investor and has invested in several startups in India and other countries.")
    st.write("Indian Angel Network: Indian Angel Network (IAN) is an angel investor group based in India that invests in early-stage startups. The network has over 500 members and has invested in more than 150 startups in India and other countries.")
    st.write("Lalaari Capital: Lalaari Capital is a venture capital firm based in Mumbai, India. The firm invests in early-stage startups in the technology and consumer sectors and has made several successful investments in India and other countries.")
    st.write("Sequoia Capital: Sequoia Capital is a venture capital firm based in Menlo Park, California. The firm has been an early investor in several successful technology companies, including Apple, Google, and Airbnb.")
    st.write("Group Angel Investors: Group Angel Investors is an angel investor group based in Spain that invests in early-stage startups. The group has made several successful investments in the technology, healthcare, and food sectors, among others.")
    st.write("")
    st.write("")
    
    st.subheader('Top Cities with Highest number of Startups!')
    top_filter = st.slider('Top N Cities', 3, 10, 5)  # min: 3, max: 10, default: 10
    label=np.arange(0,top_filter)
    cities=data["CityLocation"].value_counts().head(top_filter).reset_index()
    cities.columns=["City","Number"]
    fig=go.Figure(data=[go.Scatter(x=cities.City,y=cities.Number,mode='markers',marker_size=(cities.Number)/6, 
     marker={'color':label})])
    fig.data[0].marker.line.width = 3
    fig.data[0].marker.line.color = "black" 
    fig.update_layout(autosize=True,plot_bgcolor='rgb(275, 275, 275)')
    st.plotly_chart(fig)
    st.write("As per 202, here are some of the top cities in India with the highest number of startups:")
    st.write("•	NCR: NCR has a growing startup ecosystem, with a focus on technology, e-commerce, and education. The city has a large pool of talent, including engineers and business professionals, which has helped to fuel its startup growth.")
    st.write("•	Bengaluru: Bengaluru is known as the startup capital of India, with many startups in sectors like technology, e-commerce, and healthcare. The city has a strong ecosystem of investors, mentors, and support organizations for startups.")
    st.write("•	Mumbai: Mumbai is one of the largest cities in India and has a thriving startup ecosystem, with a focus on fintech, e-commerce, and logistics. The city is home to several leading venture capital firms and startup accelerators.")
    st.write("•	Pune: Pune is a rapidly growing startup hub, with a focus on technology, healthcare, and manufacturing. The city has a large pool of talented engineers and a growing ecosystem of investors and support organizations for startups.")
    st.write("•	Hyderabad: Hyderabad has emerged as a leading startup hub in India, with a focus on technology, healthcare, and biotech. The city is home to several top engineering colleges and research institutions, which has helped to attract talent and investment to the region.")
    st.write("Other cities with a significant number of startups include Chennai, Ahmedabad, Kolkata, and Jaipur.")


    # st.subheader('Most common words in SubVertical using WordCloud!')
    # wordcloud = WordCloud( max_words=200, background_color="white",collocations=False, width=1600, height=800).generate(text)
    # plt.figure(figsize=(20,10))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.tight_layout(pad=0)
    # plt.show()
    # st.pyplot()

    print("Run Completed")      


if __name__ == "__main__":
	app()
  
