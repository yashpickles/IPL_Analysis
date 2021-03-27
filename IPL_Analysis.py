#!/usr/bin/env python
# coding: utf-8

# # **Data Analysis of the IPL and it's teams**
# 
# ## **-Yash Acharya**

# **Cricket and the Indian Sub-Continent:** 
# 
# From streets to offices, every location ends up being a cricket pitch. Everyone claims to be an expert, and they all have cricket running through their veins. From gully cricket, played in the streets or back yards, to the World Cup itself, cricket is a way of life in the Indian Sub-Continent. A sport and its hero's worshipped by Billions Passionately throughout the breadth and depth of India and it's neighbours.
# 
# **About IPL:**
# 
# The Indian Premier League (IPL) is a professional Twenty20 cricket league in India usually contested between March and May of every year by eight teams representing eight different cities or states in India. The league was founded by the Board of Control for Cricket in India (BCCI) in 2007.
# 
# **The Dataset:**
# 
# The Data is compiled by Mr.Prateek Bharadwaj (https://www.kaggle.com/patrickb1912/ipl-complete-dataset-20082020 ) using the 'CricSheet' as the Data Source. The Information Contained in two the datasets are Up-to-Date till newest season(2020).
# 
# Dataset1 contains Ball-by-Ball Information throughout  IPL history.
# 
# Dataset2 contains information of the Matches played in IPL.
# 

# ## **Importing the Libraries**

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# In[2]:


pip install chart-studio


# In[3]:


# Using Plotly to create Interactive graphs 
import chart_studio.plotly as py
from plotly import tools
import plotly.offline as pyo
pyo.init_notebook_mode()
from plotly.offline import iplot
import plotly.figure_factory as ff
import plotly.graph_objs as go


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style("whitegrid")
plt.style.use("fivethirtyeight")


# In[5]:


# Removing Unnecessary Warnings
import warnings
warnings.filterwarnings("ignore")


# ## **Importing the Libraries**

# In[6]:


dataset1 = pd.read_csv(r"C:\Users\Yash\Desktop\Machine Learning A-Z (Codes and Datasets)\Data Analysis of the IPL and it's teams\IPL Ball-by-Ball 2008-2020.csv")
dataset2 = pd.read_csv(r"C:\Users\Yash\Desktop\Machine Learning A-Z (Codes and Datasets)\Data Analysis of the IPL and it's teams\IPL Matches 2008-2020.csv")


# ## **Visualization of the Dataset**

# ## **a) Data Exploration**

# In[7]:


dataset1.head()


# In[8]:


dataset1.describe()


# In[9]:


dataset1.columns


# In[10]:


dataset2.head()


# In[11]:


dataset2.describe()


# In[12]:


dataset2.columns


# ## **c) Replacing Team names with their Short Versions**

# Since Sunrisers Hyderabad(2013), Delhi Capitals(2018) are the teams which replaced Deccan Chargers and Delhi Daredevils respectively as Legacy Teams. Hence they are considered same for this analysis. 

# In[13]:


to_replace = ['Mumbai Indians', 'Chennai Super Kings', 'Kolkata Knight Riders',
              'Sunrisers Hyderabad', 'Deccan Chargers', 'Rajasthan Royals',
              'Delhi Daredevils', 'Kings XI Punjab', 'Royal Challengers Bangalore',
              'Kochi Tuskers Kerala', 'Rising Pune Supergiant', 'Pune Warriors', 
              'Gujarat Lions', 'Delhi Capitals', 'Rising Pune Supergiants']


# In[14]:


value = ['MI', 'CSK', 'KKR', 'SRH', 'DCH', 'RR', 'DD', 'KXIP', 'RCB', 'KTK', 'RPS', 'PW', 'GL', 'DC', 'RPS']


# In[15]:


dataset1.replace(to_replace=to_replace, value=value, inplace=True)
dataset2.replace(to_replace=to_replace, value=value, inplace=True)


# In[16]:


dataset1.head()


# In[17]:


dataset2.head()


# ## **d) Bar Graph**

# ## **Matches/Season** 

# In[18]:


dataset2['Season'] = dataset2['date'].str[:4].astype(int)
data = [go.Histogram(x=dataset2['Season'], marker=dict(color='#71acf5', 
                                                       line=dict(color='black', width=1)), opacity=0.75)]
layout = go.Layout(title='Matches/Season', xaxis=dict(title='Season',tickmode='linear'), 
                   yaxis=dict(title='Matches'),bargap=0.2, plot_bgcolor='rgb(245,245,245)') 
plot = go.Figure(data=data, layout=layout)
iplot(plot)


# Season 6 had the most number of Matches as expected because of  
# 1) 9 Teams  
# 2) Introduction of Elimiamators and Play-offs between Top 4 teams. 

# ## **Matches Played Vs Wins**

# In[19]:


Matches_Played = pd.concat([dataset2['team1'], dataset2['team2']])
Matches_Played = Matches_Played.value_counts().reset_index()


# In[20]:


print(Matches_Played)


# In[21]:


Matches_Played.columns= ['Team','Total Matches']
Matches_Played['wins']= dataset2['winner'].value_counts().reset_index()['winner']


# In[22]:


print(Matches_Played)


# In[23]:


Matches_Played.set_index('Team',inplace=True)
print(Matches_Played)


# In[24]:


current_teams = Matches_Played.reset_index().head(8)
print(current_teams)


# In[25]:


# Creating a neat Table to display the Stats using plotly 

MvW = go.Table(
    header=dict(values=['Team', 'Matches', 'Wins'],
                fill=dict(color='#18a4f5'),
                font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                align=['center'],
               height=30),
    cells=dict(values= [current_teams['Team'], current_teams['Total Matches'], current_teams['wins']],
               fill=dict(color=['rgb(153, 203, 224)', 'rgba(211, 239, 242, 0.65)']),
               align=['center'], font_size=13, height=25))
layout = dict(
        width=750,
        height=420,
        autosize=False,
        title='Total Matches vs Wins per team',
        margin = dict(t=100),
        showlegend=False,)
Table = dict(data=[MvW], layout=layout)
iplot(Table)


# Mumbai Indans being the most decorated team that they are, were not very clinical before the season 6(2013) where they'd win the first time. Yet after 2012 season they bought important players and staff that were very crucial in their resounding succes in the latter of the 7 succeding seasons.

# ## **Win Percentage of each team**

# In[26]:


WPT1 = go.Bar(x=Matches_Played.index,y=Matches_Played['Total Matches'],
                name='Total Matches',opacity=0.4)

WPT2 = go.Bar(x=Matches_Played.index,y=Matches_Played['wins'],
                name='Matches Won',marker=dict(color='red'),opacity=0.4)

WPT3 = go.Bar(x=Matches_Played.index,
               y=(round(Matches_Played['wins']/Matches_Played['Total Matches'],3)*100),
               name='Win Percentage',opacity=0.6,marker=dict(color='gold'))

data = [WPT1, WPT2, WPT3]

layout = go.Layout(title='Match Played, Wins And Win Percentage',xaxis=dict(title='Team'),
                   yaxis=dict(title='Played'),bargap=0.2,bargroupgap=0.1, plot_bgcolor='rgb(245,245,245)')

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# In[27]:


# Teams with Best Win Percent in IPL History
Win_Percentage = round(Matches_Played['wins']/Matches_Played['Total Matches'],3)*100
Win_Percentage.sort_values(ascending=False).head(5)


# In[28]:


# Teams with Worst Win Percent in IPL History
Win_Percentage.sort_values(ascending=True).head(3)


# The most Surprising aspects of this Part of analysis: 
# 
# 1) Chennai Super Kings having "less win rate" than Royal Challengers inspite of the fact that they have been consistently qualifying into the play-offs(bar IPL-2020).
# 
# 2) Indicates that CSK performs where it matters the most i.e Tie Breakers and Play-offs while RCB is with a better Win rate hasn't been able to capitalise.
# 
# 3) Deccan Chargers were abisymal in their 5 seasons in IPL with a win rate of 38.7%, they were the worst performers among the title winners of the league.
# 
# 4) In Comparision to Deccan Chargers, Sunrisers their Hyderabad counterparts and replacers have had a way better win rate @53.2%(3rd best) and also have been consistent enough to Win in 2016.  

# ## **Stadiums with Most Matches**

# In[29]:


venue_matches = dataset2.groupby('venue').count()[['id']].sort_values(by='id',ascending=False).head()
print(venue_matches)


# In[30]:


ser = pd.Series(venue_matches['id'])
print(ser)


# In[31]:


venue_matches = dataset2.groupby('venue').count()[['id']].reset_index()


# In[32]:



data = [{"y": venue_matches['id'],"x": venue_matches['venue'], 
          "marker": {"color": "lightblue", "size": 12},
         "line": {"color": "red","width" : 2,"dash" : 'dash'},
          "mode": "markers+lines", "name": "Women", "type": "scatter"}]

layout = {"title": "Stadiums Vs. Matches", 
          "xaxis": {"title": "Stadiums", }, 
          "yaxis": {"title": "Matches Played"},
          "autosize":True,"width":900,"height":700,"plot_bgcolor":"rgb(245,245,245)"}

ven = go.Figure(data=data, layout=layout)
iplot(ven)


# Eden Gardens(Kolkata), Feroz Shah Kotla(New Delhi), Wankhede(Mumbai) and Chinnaswamy(Bengaluru) were the stadiums with most IPL matches played. One of the reasons could be their Historic and Prestigious repute over the years. Another reason could be their location, being located in a Big Metropolitan City surely works well to their advantage, to draw huge and passionate crowds.  

# ## **Prefered Choice after Winning Toss**

# In[33]:


x = dataset2["toss_decision"].value_counts().index
print(x)


# In[34]:


y = dataset2["toss_decision"].value_counts().values
print(y)


# In[35]:


data = [go.Bar(
    x = dataset2["toss_decision"].value_counts().index,
    y = dataset2["toss_decision"].value_counts().values,
    marker = dict(line=dict(color='#000000', width=1))
)]

layout = go.Layout(
   {
      "title":"Most Prefered Choice After Winning Toss",
       "xaxis":dict(title='Decision'),
       "yaxis":dict(title='Matches'),
       "plot_bgcolor":'rgb(245,245,245)'
   }
)
Dec = go.Figure(data=data,layout = layout)
iplot(Dec)


# Probable Reasons for more Teams electing to Field First:
# 
# 1) T20 being a very fast paced version of the game, needs much more quality than just being a great bowling or batting unit. This means that Teams must harness better psychological edge than their opponent.
# 
# 2) if the Captain is confident that their team can successfully chase any total. Once the target is known, the team does not have to worry about setting a winnable score.
# 
# 3) The team is very certain about pitch conditions(Usually the Home team) and the levels of deterioration of the pitch in the latter half of the match.
# 
# 4)  In some venues, the cricket ball collects a lot of dew in the outfield. This results in a poor grip on the ball by the bowlers. With a moist ball, it is difficult to spin and swing the ball. The difficulty in holding the ball also means that the bowler is more likely to be inaccurate, giving the batsmen more ill-directed deliveries to hit.

# ## **Coin Toss**

# ### **a)Match Win vs  Toss win**

# In[36]:


Match_Outcome = pd.concat([dataset2['toss_winner']])
Match_Outcome = Match_Outcome.value_counts().reset_index()


# In[37]:


print(Match_Outcome)


# In[38]:


Match_Outcome.columns= ['Team',' Toss Winner']
Match_Outcome['Match Winner']= dataset2['winner'].value_counts().reset_index()['winner']
print(Match_Outcome)


# In[39]:


Match_Outcome.set_index('Team',inplace=True)
print(Match_Outcome)


# In[40]:


current_teams = Match_Outcome.reset_index().head(8)
print(current_teams)


# ### **b) Teams Who Won the toss and Won the Match too**

# In[41]:


Tosswin_matchwin=dataset2[dataset2['toss_winner']==dataset2['winner']]
slices = [len(Tosswin_matchwin), (636-len(Tosswin_matchwin))]
labels=['Yes','No']
plt.pie(slices, labels=labels, startangle=90, shadow=True, explode=(0,0), autopct='%1.1f%%', colors=['green','red'])
plt.title("Teams who had won Toss and Won the match")
fig = plt.gcf()
fig.set_size_inches(5,5)
plt.show()


# ### **c) Win Toss**        

# In[42]:



Win_Toss = pd.concat([dataset2['team1'], dataset2['team2']])
Win_Toss = Win_Toss.value_counts().reset_index()
print(Win_Toss)


# In[43]:


Win_Toss.columns= ['Team','Total Matches']
Win_Toss['Toss wins']= dataset2['toss_winner'].value_counts().reset_index()['toss_winner']
print(Win_Toss)


# In[44]:


Win_Toss.set_index('Team',inplace=True)
print(Win_Toss)


# In[45]:


current_teams = Win_Toss.reset_index().head(8)
print(current_teams)


# In[46]:


# Teams with Best Win Percent in IPL History
Win_Percentage = round(current_teams['Toss wins']/current_teams['Total Matches'],3)*100
print(Win_Percentage)


# In[47]:


current_teams['Win %'] = Win_Percentage
print(current_teams)


# In[48]:


# Creating a neat Table to display the Stats using plotly 
WT = go.Table(
    header=dict(values=['Team', 'Toatl Matches', 'Toss Wins', 'Win %'],
                fill=dict(color='#18a4f5'),
                font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                align=['center'],
               height=30),
    cells=dict(values= [current_teams['Team'], current_teams['Total Matches'], current_teams['Toss wins'], current_teams['Win %']],
               fill=dict(color=['rgb(153, 203, 224)', 'rgba(211, 239, 242, 0.65)']),
               align=['center'], font_size=13, height=25))
layout = dict(
        width=750,
        height=420,
        autosize=False,
        title='Toss Wins vs Total Matches',
        margin = dict(t=100),
        showlegend=False,)
Table = dict(data=[WT], layout=layout)
iplot(Table)


# Interesting Bits from the Data:
# 
# 1) In Every 10 games, 6 times a Team that wins the Toss goes on to win the game. This means that Winning tosses could be very crucial in the outcome of the match. Reasos for that are below:
#   
#   a) Home team advantage, being the host team has certain advantages first being the knowledge of pitch conditions and pitch    degradation throughout the match.
#   
#   b) Weather conditions, Since for most of its life IPL was played during the Summers in India. The Weather can play an important role inthe game, for example Coastal regions like Mumbai and Chennai usually have tropical climate(i.e Hot and Humid). Under moist conditions, a batsman has to struggle with the effects of the damp ground, which slows down the ball giving spinners alot of advantages. Which the team winning the toss can exploit by batting frst and then harnesing the effectiveness of the Spin Specialist.
#   
#   c) Simply Psychological effect.
#   
# 2) Although Coin toss has a probability of 50%, Teams such as MI, RCB, DD and KKR have had more coin tosses called their way then the rest of the other 10 teams. In-fact MI, KKR and RCB are the only ones from above mentioned teams who have had more wins per toss wins. MI = 113.2%, RCB = 104.5% and KKR = 108.16% respectively.  
# 
# 3) It seems that, in the current IPL teams bunch only Punjab Kings(KXIP) and Delhi Capitals(DC) have won less matches v/s Toss Wins.   

# ## **Runs**

# ### **Runs Per Season** 

# In[49]:


# Joining the two datasets into a new variable called 'batsmen' for further use
dataset2['Season'] = dataset2['date'].str[:4].astype(int)
batsmen = dataset2[['id','Season']].merge(dataset1, left_on = 'id', right_on = 'id', how = 'left').drop('id', axis = 1)
print(batsmen.head(5))


# In[50]:


#A new variable called season for storing the total runs and seasons
Season = batsmen.groupby(['Season'])['total_runs'].sum().reset_index()
print(Season)


# In[51]:


avgruns_each_season = dataset2.groupby(['Season']).count().id.reset_index()
print(avgruns_each_season)


# In[52]:


avgruns_each_season.rename(columns={'id':'Matches'},inplace=1)
print(avgruns_each_season)


# In[53]:


avgruns_each_season['Total Runs'] = Season['total_runs']
print(avgruns_each_season)


# In[54]:


avgruns_each_season['Avg RPS'] = avgruns_each_season['Total Runs'] / avgruns_each_season['Matches']
print(avgruns_each_season)


# In[55]:


RPS = go.Table(
    header=dict(values=['Season ', 'Matches', 'Total Runs', 'Avg RPS'],
                fill=dict(color='#18a4f5'),
                font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                align=['center'],
               height=30),
    cells=dict(values= [avgruns_each_season['Season'], avgruns_each_season['Matches'], 
                        avgruns_each_season['Total Runs'], avgruns_each_season['Avg RPS']],
               fill=dict(color=['rgb(153, 203, 224)', 'rgba(211, 239, 242, 0.65)']),
               align=['center'], font_size=13, height=25))
layout = dict(
        width=750,
        height=420,
        autosize=False,
        title='Runs Per Season',
        margin = dict(t=100),
        showlegend=False,)
Table = dict(data=[RPS], layout=layout)
iplot(Table)


# In[56]:


import matplotlib.pyplot as plt


# In[57]:


# Creating Line Plots for Simplification
# Matches Per Season    
plt.plot(avgruns_each_season['Season'], avgruns_each_season['Matches'], color='red', marker='o')
plt.title('Matches Per Season', fontsize=14)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Matches', fontsize=14)
plt.grid(True)
plt.show()


# In[58]:


# Runs Per Season
plt.plot(avgruns_each_season['Season'], avgruns_each_season['Total Runs'], color='red', marker='o')
plt.title('Runs Per Season', fontsize=14)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Runs', fontsize=14)
plt.grid(True)
plt.show()


# In[59]:


plt.plot(avgruns_each_season['Season'], avgruns_each_season['Avg RPS'], color='red', marker='o')
plt.title('Avg Runs Per Season', fontsize=14)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Avg Runs', fontsize=14)
plt.grid(True)
plt.show()


# ### **Runs Distribution** 

# In[60]:


Season_boundaries = batsmen.groupby("Season")["batsman_runs"].agg(lambda x: (x==6).sum()).reset_index()
print(Season_boundaries)


# In[61]:


fours = batsmen.groupby("Season")["batsman_runs"].agg(lambda x: (x==4).sum()).reset_index()
print(fours)


# In[62]:


Season_boundaries = Season_boundaries.merge(fours,left_on='Season',right_on='Season',how='left')
print(Season_boundaries)


# In[63]:


Season_boundaries = Season_boundaries.rename(columns={'batsman_runs_x':'6"s','batsman_runs_y':'4"s'})
print(Season_boundaries)


# In[64]:


Season_boundaries['6"s'] = Season_boundaries['6"s']*6
Season_boundaries['4"s'] = Season_boundaries['4"s']*4
Season_boundaries['Total Runs'] = Season['total_runs']
print(Season_boundaries)


# In[65]:


RD1 = go.Bar(
    x=Season_boundaries['Season'],
    y=Season_boundaries['Total Runs']-(Season_boundaries['6"s']+Season_boundaries['4"s']),
    marker = dict(line=dict(color='#000000', width=1)),
    name='Non Boundaries',opacity=0.6)

RD2 = go.Bar(
    x=Season_boundaries['Season'],
    y=Season_boundaries['4"s'],
    marker = dict(line=dict(color='#000000', width=1)),
    name='Runs by 4"s',opacity=0.7)

RD3 = go.Bar(
    x=Season_boundaries['Season'],
    y=Season_boundaries['6"s'],
    marker = dict(line=dict(color='#000000', width=1)),
    name='Runs by 6"s',opacity=0.7)


data = [RD1, RD2, RD3]
layout = go.Layout(title="Run Distribution per year",barmode='stack',xaxis = dict(tickmode='linear',title="Year"),
                                    yaxis = dict(title= "Run Distribution"), plot_bgcolor='rgb(245,245,245)')

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# ### **Highest Runs scored by a Team** 

# In[66]:


most_runs  = dataset1.groupby(['id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index()
print(most_runs)


# In[67]:


most_runs = most_runs[most_runs['total_runs']>=210]
print(most_runs)


# In[68]:


HS = most_runs.nlargest(10,'total_runs')
print(HS)


# In[69]:


MRS = go.Table(
    header=dict(values=['inning ', 'batting_team ', 'bowling_team  ', 'total_runs'],
                fill=dict(color='#18a4f5'),
                font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                align=['center'],
               height=30),
    cells=dict(values= [HS['inning'], HS['batting_team'], 
                        HS['bowling_team'], HS['total_runs']],
               fill=dict(color=['rgb(153, 203, 224)', 'rgba(211, 239, 242, 0.65)']),
               align=['center'], font_size=13, height=25))
layout = dict(
        width=750,
        height=420,
        autosize=False,
        title='Highest Runs Scored by a Team',
        margin = dict(t=100),
        showlegend=False,)
Table = dict(data=[MRS], layout=layout)
iplot(Table)


# ### **Top 10 Highest Run getters in IPL History**

# In[70]:


batsmen = dataset2[['id','Season']].merge(dataset1, left_on = 'id', right_on = 'id', how = 'left').drop('id', axis = 1)
print(batsmen.head(5))


# In[71]:


max_runs = batsmen.groupby(['Season', 'batsman', 'batting_team'])['batsman_runs'].sum().reset_index()    
print(max_runs.tail(8))


# In[72]:


max_runs = max_runs[max_runs['batsman_runs']>=500]
print(max_runs)


# In[73]:


Runs_Per_Season = max_runs.nlargest(10,'batsman_runs')
print(Runs_Per_Season)


# In[74]:


HRGs = go.Table(
    header=dict(values=['Season', 'batsman', 'batting_team', 'batsman_runs'],
                fill=dict(color='#18a4f5'),
                font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                align=['center'],
               height=30),
    cells=dict(values= [Runs_Per_Season['Season'], Runs_Per_Season['batsman'], 
                        Runs_Per_Season['batting_team'], Runs_Per_Season['batsman_runs']],
               fill=dict(color=['rgb(153, 203, 224)', 'rgba(211, 239, 242, 0.65)']),
               align=['center'], font_size=13, height=25))
layout = dict(
        width=750,
        height=420,
        autosize=False,
        title='Top 10 Highest Run getters in IPL History',
        margin = dict(t=100),
        showlegend=False,)
Table = dict(data=[HRGs], layout=layout)
iplot(Table)


# ## **Wickets** 

# ### **Wickets Per Season** 

# In[75]:


# Joining the two datasets into a new variable called 'bowler' for further use
bowler = dataset2[['id','Season']].merge(dataset1, left_on = 'id', right_on = 'id', how = 'left').drop('id', axis = 1)
print(bowler.head(5))


# In[76]:


Wickets = bowler.groupby(['Season'])['is_wicket'].sum().reset_index()
print(Wickets)


# In[77]:


avgwickets_each_season = dataset2.groupby(['Season']).count().id.reset_index()
print(avgwickets_each_season)


# In[78]:


avgwickets_each_season.rename(columns={'id':'Matches'},inplace=1)
print(avgwickets_each_season)


# In[79]:


avgwickets_each_season['Total Wickets'] = Wickets['is_wicket']
print(avgwickets_each_season)


# In[80]:


avgwickets_each_season['Avg WPM'] = avgwickets_each_season['Total Wickets'] / avgwickets_each_season['Matches']
print(avgwickets_each_season)


# In[81]:


WPS = go.Table(
    header=dict(values=['Season', 'Matches', 'Total Wickets', 'Avg WPM'],
                fill=dict(color='#18a4f5'),
                font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                align=['center'],
               height=30),
    cells=dict(values= [avgwickets_each_season['Season'], avgwickets_each_season['Matches'], 
                        avgwickets_each_season['Total Wickets'], avgwickets_each_season['Avg WPM']],
               fill=dict(color=['rgb(153, 203, 224)', 'rgba(211, 239, 242, 0.65)']),
               align=['center'], font_size=13, height=25))
layout = dict(
        width=750,
        height=420,
        autosize=False,
        title='Wickets Per Season',
        margin = dict(t=100),
        showlegend=False,)
Table = dict(data=[WPS], layout=layout)
iplot(Table)


# In[82]:


# Creating Line Plots for Simplification
# Wickets Per Season    
plt.plot(avgwickets_each_season['Season'], avgwickets_each_season['Total Wickets'], color='red', marker='o')
plt.title('Wckets Per Season', fontsize=14)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Wickets', fontsize=14)
plt.grid(True)
plt.show()


# In[83]:


# Avg Wickets Per Match Per Season    
plt.plot(avgwickets_each_season['Season'], avgwickets_each_season['Avg WPM'], color='red', marker='o')
plt.title('Average Wckets Per Match', fontsize=14)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Average Wickets Per Match', fontsize=14)
plt.grid(True)
plt.show()


# ### **Teams With Most Wickets taken**

# In[90]:


bowler = dataset2[['id','Season']].merge(dataset1, left_on = 'id', right_on = 'id', how = 'left').drop('id', axis = 1)
most_wickets  = bowler.groupby(['Season', 'bowling_team'])['is_wicket'].sum().reset_index()
print(most_wickets)


# In[101]:


most_wickets  = bowler.groupby(['bowling_team'])['is_wicket'].sum().reset_index()
Team_Wickets = most_wickets.sort_values(by = 'is_wicket', ascending=False).head(10)


# In[102]:


Team_Wickets.rename(columns={'is_wicket':'Wickets'},inplace=1)
Team_Wickets.rename(columns={'bowling_team':'Team'},inplace=1)
print(Team_Wickets)


# In[104]:


WKTS = go.Table(
    header=dict(values=['Team', 'Wickets'],
                fill=dict(color='#18a4f5'),
                font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                align=['center'],
               height=30),
    cells=dict(values= [Team_Wickets['Team'], Team_Wickets['Wickets']],
               fill=dict(color=['rgb(153, 203, 224)', 'rgba(211, 239, 242, 0.65)']),
               align=['center'], font_size=13, height=25))
layout = dict(
        width=750,
        height=420,
        autosize=False,
        title='Teams with most Wickets',
        margin = dict(t=100),
        showlegend=False,)
Table = dict(data=[WKTS], layout=layout)
iplot(Table)


# In[ ]:




