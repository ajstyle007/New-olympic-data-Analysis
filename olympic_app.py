import streamlit as st
import pandas as pd
import functions
import important
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df = functions.preprocess1(df, region_df)


#st.title("Olympic Data Analysis.")

st.sidebar.title("Olympic Data Analysis.")
st.sidebar.image("Olympic_image.jpg")
user_menu = st.sidebar.radio("Select an option", ("Overall Analysis", "Medal tally", "Country-wise Analysis", "Athlete-wise Analysis"))


if user_menu == "Overall Analysis":
    editions = df["Year"].unique().shape[0]-1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]

    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("cities")
        st.title(cities)
    with col3:
        st.header("sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("events")
        st.title(events)
    with col2:
        st.header("athletes")
        st.title(athletes)
    with col3:
        st.header("nations")
        st.title(nations)

    st.subheader("Countries have hosted the olympics.")
    n_df = df.drop_duplicates(subset="Year")[["Year","City"]]
    fig = px.bar(n_df, x='City', y='Year',text_auto = True,)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

    countries_over_time = important.data_over_time(df,"region")
    fig = px.line(countries_over_time, x="Year", y="region", title = 'Participating Countries over the years')
    st.plotly_chart(fig)

    events_over_time = important.data_over_time(df, "Event")
    fig = px.line(events_over_time, x="Year", y="Event", title = 'Events over the years')
    st.plotly_chart(fig)

    athlete_over_time = important.data_over_time(df, "Name")
    fig = px.line(athlete_over_time, x="Year", y="Name", title = 'Athletes over the years')
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"),annot=True)
    st.pyplot(fig)

    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    
    selected_sport = st.selectbox("Select a Sport",sport_list)
    st.title("Most successful Athletes")
    x = important.most_successful(df,selected_sport)
    st.table(x)

    st.title("Most popular sports of Olympics")
    sport_df = df["Sport"].value_counts().reset_index()
    fig = px.pie(sport_df, values='count', names='Sport')
    fig.update_layout(autosize=False, width=850,height=700)
    st.plotly_chart(fig)

    st.title("Locations of Stadium of countries where olympics held.")
    data1 = pd.read_csv("lat_long.csv")
    st.map(data1)


if user_menu == "Medal tally":

    st.sidebar.header("Medal tally")
    years, country = important.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medal_tally = important.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Medal Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title(selected_country + " overall performance in Olympics" )
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(selected_country + "'s performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)
    

if user_menu == "Country-wise Analysis":

    st.title("Country-wise Analysis")

    country = df["region"].dropna().unique().tolist()
    country.sort()

    selected_country = st.sidebar.selectbox("Select a country", country)
    new_region = important.country_wise_medal_tally(df, selected_country)
    
    fig = px.line(new_region, x = "Year", y="Medal")
    st.subheader(selected_country + "'s Medal Tally over the years")
    st.plotly_chart(fig)

    pt = important.country_event_heatmap(df,selected_country)
    st.subheader(selected_country+" excels in the following sports")
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    athlete = important.most_successful_athletes(df, selected_country)
    st.subheader("Top 10 athletes of "+ selected_country)
    st.table(athlete)

if user_menu == "Athlete-wise Analysis":

    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    st.title("Distribution of Age.")
    fig = ff.create_distplot([x1,x2,x3,x4], ["Age Distribution","Gold Medalist","Silver Medalist","Bronze Medalist"], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=850,height=530)
    st.plotly_chart(fig)

    st.title("Distribution of Age wrt sports(Gold Medalist)")
    famous_sports =['Basketball','Judo', 'Football','Tug-Of-War','Athletics','Swimming','Badminton','Sailing','Gymnastics','Art Competitions',
                'Handball','Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing','Shooting','Boxing','Taekwondo',
                'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery', 'Volleyball','Synchronized Swimming',
                 'Table Tennis', 'Baseball','Rhythmic Gymnastics','Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo', 'Cricket',
                'Ice Hockey','Motorboating']
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"]=="Gold"]["Age"].dropna())
        name.append(sport)

    fig1 = ff.create_distplot(x,name,show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, width=850,height=530)
    st.plotly_chart(fig1)


    st.title("Height vs Weight")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    
    selected_sport = st.selectbox("Select a Sport",sport_list)
    new_df = important.weight_v_height(df,selected_sport)

    fig, ax = plt.subplots(figsize=(10,10))
    ax = sns.scatterplot(new_df, x ="Weight",y = "Height", hue=new_df["Medal"],style=new_df["Sex"],s=100)
    st.pyplot(fig)

    st.title("Men vs Women participation over the years")
    final_df = important.men_vs_women(df)
    fig = px.line(final_df, x="Year", y=["Male","Female"])
    st.plotly_chart(fig)

    
    

    
    
    


    


    
    
    


    

