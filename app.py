import streamlit as st
import pickle
import pandas as pd


st.markdown("""
<style>
.stApp{
background-image: linear-gradient(to right,#141e30,#243b55);
color:white;
}
</style>
""", unsafe_allow_html=True)

teams = ['Sunrisers Hyderabad',
'Mumbai Indians',
'Royal Challengers Bangalore',
'Kolkata Knight Riders',
'Kings XI Punjab',
'Chennai Super Kings',
'Rajasthan Royals',
'Delhi Capitals']


cities = ['Hyderabad','Bangalore','Mumbai','Indore','Kolkata','Delhi',
'Chandigarh','Jaipur','Chennai','Cape Town','Port Elizabeth',
'Durban','Centurion','East London','Johannesburg','Kimberley',
'Bloemfontein','Ahmedabad','Cuttack','Nagpur','Dharamsala',
'Visakhapatnam','Pune','Raipur','Ranchi','Abu Dhabi',
'Sharjah','Mohali','Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))

st.markdown("<h1 style='text-align:center;color:#FFD700;'>🏏 IPL Win Predictor</h1>", unsafe_allow_html=True)

col1,col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))

with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))


selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score')

with col4:
    overs = st.number_input('Overs completed')

with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):

    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_remaining = 10 - wickets

    if overs == 0:
        crr = 0
    else:
        crr = score / overs

    if balls_left == 0:
        rrr = 0
    else:
        rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({
        'batting_team':[batting_team],
        'bowling_team':[bowling_team],
        'city':[selected_city],
        'runs_left':[runs_left],
        'balls_left':[balls_left],
        'wickets':[wickets_remaining],
        'total_runs_x':[target],
        'crr':[crr],
        'rrr':[rrr]
    })

    result = pipe.predict_proba(input_df)

    loss = result[0][0]
    win = result[0][1]

    st.subheader("Win Probability")

    st.progress(int(win*100))

    st.write(batting_team + " winning chance:", round(win*100), "%")
    st.write(bowling_team + " winning chance:", round(loss*100), "%")