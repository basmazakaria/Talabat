import streamlit as st
import openpyxl as os
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np 

import zipfile

with zipfile.ZipFile('data_cleaned_final.zip', 'r') as zip_ref:
    zip_ref.extractall('Talabat')
    df=pd.read_csv("data_cleaned_final.csv")


fd=pd.read_excel("fct_order.xlsx")
vd=pd.read_excel("dim_vendor.xlsx")
dd=pd.read_excel("dim_date.xlsx")
ad=pd.ExcelFile("Talabat Dataset.xlsx")

fm=pd.read_excel('fct_meta.xlsx')
vm=pd.read_excel('vend_meta.xlsx')
dm=pd.read_excel('date_meta.xlsx')


st.image('talabat.png')
tab1,tab2,tab3,tab4 = st.tabs(["Dataset Overview", "Data Preparation","Talabat Analysis","Our Team"])
with tab1:
    
    st.subheader('The dataset provides information on Talabat Platform from Sep_2021 to Jan_2022. The dataset contains the followin tables:')

    st.subheader('fct_order Table:')

    st.markdown(''' * It contains details about the orders(order_id,order_time,vendo_id...etc)''')
    st.markdown(''' * **Meta Data**:''')
    st.dataframe(fm,use_container_width=True)
    with st.expander("Show fct_order Details Sample Data"):
        st.dataframe(fd.head(),use_container_width=True)
        st.write(f"###### orders Dataframe Shape = **{fd.shape}**")

    st.subheader('dim_vendor Table:')
    st.markdown(''' * It contains details about the vendors(vendo_id,name_en,..etc)''')
    st.markdown(''' * **Meta Data**:''')
    st.dataframe(vm)
    with st.expander("Show dim_vendors Details Sample Data"):
        st.dataframe(vd.head(),use_container_width=True)
        st.write(f"###### vendors Dataframe Shape = **{vd.shape}**")

    st.subheader('dim_date Table:')
    st.markdown('''
       * It contains details about the orders time
       * **Meta Data**:''')
    st.dataframe(dm)
    with st.expander("Show dim_date Details Sample Data"):
        st.dataframe(dd.head(),use_container_width=True)
        st.write(f"###### date Dataframe Shape = **{dd.shape}**")
    
    st.divider()
    st.subheader('Schema Diagram:')
    st.image('Schema.jpg')

    st.divider()
    st.subheader('Dashboard:')
    ##image
    st.link_button("View Dashboard", "link")

    st.divider()
    st.subheader('Presentation:')
    st.link_button("View Our Presentation", "link")



with tab2:
    st.markdown('''
    #### **Data Preparation:**
    As we saw the dataset and it's tables let's discover how we prepared it for our work:
                

    ''')
    st.dataframe(ad.sheet_names)
    st.divider()
    
    st.markdown('''#### **Data Quality (Data Preparation)**''')
    st.image('Picture4.png')
    st.markdown('''
    1.**Loading Data**:
       * Data was loaded from two Excel files dim_vendor.xlsx and fct_order.xlsx using :red[pd.read_excel().]''')
    st.markdown('''
    2.**Merging Data**:
       * The two datasets were merged on the vendor_id column using pd.merge() to create a unified dataset.''')
    st.markdown('''
    3.**Handling Missing Values**:
       * Missing values in categorical columns like reason, sub_reason, and owner were filled with placeholders like 'Successful order'.
       * For the numerical column affordability_amt_total, missing values were replaced with 0.
       * If both actual_delivery_time and promised_delivery_time were missing, they were filled with zeros along with order_delay.

    ''')
    #st.image('missing.png')
    st.dataframe(fd[['reason','sub_reason','owner']].head())
    st.markdown('''
    4.**City Cluster Update**:
       * Specific cities were grouped into clusters (e.g., cities like "Shebeen El Koom" and "Al Mahallah Al Kubra" were assigned to the "Delta" cluster).
         
    ''')
    st.image('city.png')
    #st.dataframe(fd[['City Cluster','City'=='Al Mahal lah Al Kubra']].head())
    st.markdown('''
    5.**Saving Cleaned Data**:
       * The cleaned and processed dataset was saved to data_cleaned_final.csv.
    ''')
    #
    st.dataframe(df.head())
    st.divider()
    st.subheader('Preprocessing Notebook:')
    st.link_button("View Our the Notebook", "https://colab.research.google.com/drive/1oKlQQm0k8WmiH_tSn9IEwxfkD7v3RxYB?usp=sharing")


with tab3:
    #data = pd.read_csv('data_cleaned_final.csv')

    #st.set_page_config(page_title="Talabat Analysis", initial_sidebar_state='expanded')

    col1, col2 = st.columns([3, 1])
    with col1:
       st.title(':orange[Talabat Analysis]')
    with col2:
       st.image("Picture5.png", use_column_width=True)
    st.divider()


    st.subheader('Talabat Analysis Overview')
    st.markdown('''**What's Talabat?**
    Talabat is an online delivary platform that delivers food and products 
    from stores to homes.
    Foynded in 2004 in Kuwait, and soon expanded to include manny middle Eastern countries
    uch as Suadi Arabia, Bahrain, UAE Oman, Qatar, Jordan. 
    ''')


    st.markdown('''#### **Here is some of our humble analysis:**''')

# Top 5 Cities by Order Count
    top_5_cities = df['City'].value_counts().nlargest(5)

# Plotting Top 5 Cities

    fig = px.bar(x=top_5_cities.values, y=top_5_cities.index, orientation='h',
                labels={'x': 'Order Count', 'y': 'City'}, title='Top 5 Cities by Order Count')
    fig.update_traces(marker_color='#FF9800', text=top_5_cities.values, textposition='auto')
    st.plotly_chart(fig)
    st.divider()

# Calculate average order value per city
    average_order_value_by_city = df.groupby('City')['gmv_amount_lc'].mean().nlargest(10)

# Plotting Average Order Value by City
    fig = px.bar(x=average_order_value_by_city.values, y=average_order_value_by_city.index, orientation='h',
                 labels={'x': 'Average Order Value (LC)', 'y': 'City'}, title='Top 10 Cities by Average Order Value')
    fig.update_traces(marker_color='#2196F3', text=average_order_value_by_city.values.round(2), textposition='auto')
    st.plotly_chart(fig)
    st.divider()

# Calculate success rate per platform
    successful_orders_by_platform = df.groupby('platform')['is_successful'].mean() * 100

# Plotting Successful Orders by Platform
    fig = px.bar(successful_orders_by_platform, x=successful_orders_by_platform.index,
                y=successful_orders_by_platform.values,
                labels={'x': 'Platform', 'y': 'Success Rate (%)'}, title='Successful Orders by Platform')
    fig.update_traces(marker_color='#4CAF50', text=successful_orders_by_platform.values.round(2), textposition='auto')
    st.plotly_chart(fig)
    st.divider()


# Calculate average actual and promised delivery time
    average_times = df[['actual_delivery_time', 'promised_delivery_time']].mean()

# Plotting Average Delivery Time vs. Promised Time
    fig = px.bar(x=average_times.index, y=average_times.values,
                labels={'x': 'Time Type', 'y': 'Time (mins)'}, title='Average Delivery Time vs. Promised Time')
    fig.update_traces(marker_color=['#FF5722', '#8BC34A'], text=average_times.values.round(2), textposition='auto')
    st.plotly_chart(fig)
    st.divider()


# Calculate delivery fee as a percentage of basket amount
    df['delivery_fee_percentage'] = (df['delivery_fee_amount_lc'] / data['basket_amount_lc']) * 100

# Plot delivery fee percentage distribution
    fig = px.histogram(df, x='delivery_fee_percentage', nbins=50,
                   labels={'delivery_fee_percentage': 'Delivery Fee as % of Basket Amount'},
                   title='Distribution of Delivery Fee as Percentage of Basket Amount')
    st.plotly_chart(fig)
    st.markdown(''' * Delivery Fee as a Percentage of Basket Amount: This KPI helps identify how 
    much delivery charges take up relative to the total value of orders, which can inform pricing strategies.''')
    st.divider()


# Calculate success rate by city and platform
    success_rate_city_platform = df.groupby(['City', 'platform'])['is_successful'].mean().unstack() * 100

# Plotting Success Rate by City and Platform
    fig = px.imshow(success_rate_city_platform,
                labels=dict(x="Platform", y="City", color="Success Rate (%)"),
                title="Order Success Rate by City and Platform")
    st.plotly_chart(fig)
    st.markdown(''' * Order Success Rate by City and Platform
    This KPI measures the percentage of successful orders for each combination of city and platform. It allows you 
    to assess the performance of different platforms in various cities, helping to identify areas where improvements may be needed.''')
    st.divider()


    st.markdown(''' #### **Dashboard Analysis**: ''')
    st.link_button("View Our Dashboard", "https://drive.google.com/file/d/18UldRBKfi1GFrDwetuydDcBk25uYeXc7/view?usp=sharing")
    st.divider()

    st.markdown(''' #### **Analysis Notebook**: ''')
    st.link_button("View Our Notebook", "link")
with tab4:
    #st.set_page_config(page_title="Our Team", initial_sidebar_state='expanded')

    col1, col2 = st.columns([3, 1])
    with col1:
       st.title('Meet Our Team')
    with col2:
       st.image("Picture1.png", use_column_width=True)
    st.divider()

# LinkedIn icon URL
    linkedin_icon = "https://img.icons8.com/?size=100&id=8808&format=png&color=FFFFFF"

    st.markdown("<h3>Our Team Members</h3>", unsafe_allow_html=True)
    team_members = [
       {"name": "Mohamed Abbas", "linkedin": "https://www.linkedin.com/in/mo-abbass/"},
       {"name": "Mohamed Hassan", "linkedin": "https://www.linkedin.com/in/mohamed-hassan22?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"},
       {"name": "Ahmed Hosny", "linkedin": "https://www.linkedin.com/in/ahmed-hosny8?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"},
       {"name": "Basma Zakaria", "linkedin": "https://www.linkedin.com/in/basma-zakaria-a59a72328/"}
    ]

    for member in team_members:
       st.markdown(f"""
          <style>
                .hover-div {{
                   padding: 10px;
                   border-radius: 10px;
                   background-color: #2c413c;
                   margin-bottom: 10px;
                   display: flex;
                   justify-content: space-between;
                   align-items: center;
                   transition: background-color 0.3s ease, box-shadow 0.3s ease;
               }}
                .hover-div:hover {{
                   background-color: #1e7460; /* Slightly lighter background color on hover */
                   box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2); /* Adds a shadow on hover */
               }}
                .linkedin-icon {{
                   width: 35px; /* Bigger icon size */
                   vertical-align: middle;
               }}
           </style>
            <div class="hover-div">
               <h4 style="margin-left: 15px; color: white;">{member['name']}</h4>
               <a href="{member['linkedin']}" target="_blank" style="margin-right: 25px;">
                   <img src="{linkedin_icon}" class="linkedin-icon"/>
               </a>
            </div>
          """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
       <h3 style='color: #386641;'>We Value Your Feedback!</h3>
       <p style='font-size: 18px;'>Thank you for visiting our project page! We hope you enjoyed exploring our work. Your feedback is important to us, and we'd love to hear your thoughts, suggestions, or any questions you may have.</p>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
       <p style='font-size: 18px;'>A special thanks to <strong>Eng. Karim Ahmed</strong> for your valuable mentorship and supervision, which has been instrumental in our growth and success.</p>
    """, unsafe_allow_html=True)
