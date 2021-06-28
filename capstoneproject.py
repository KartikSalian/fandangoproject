import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
fandango= pd.read_csv('fandango_scrape.csv')
print(fandango.head())
print(fandango.info())
print(fandango.describe())

# Scatter plot for ratings and votes

#sns.scatterplot(data=fandango,x='RATING',y='VOTES')             ####

# per year movie count
fandango['YEAR']= fandango['FILM'].apply(lambda title: title.split('(')[-1].replace(')',' ') )
print(fandango.head())
yearcount=fandango['YEAR'].value_counts()
print(yearcount)
#sns.countplot(data=fandango,x='YEAR')               #####

#top 10 movies with highest votes

top_ten=fandango.nlargest(10,'VOTES')
print(top_ten)

#dataframe with only reviewed

new_fandango= fandango[fandango['VOTES']>0]

#diffrence in ratings and stars

sns.kdeplot(data=new_fandango,x='RATING',fill=True,clip=[0,5],label='Ratings') ####
sns.kdeplot(data=new_fandango,x='STARS',fill=True,clip=[0,5],label='STARS')    #####
plt.legend(loc=(1,0.5))

#for differnce in stars and ratings
new_fandango['Star_diff']=new_fandango['STARS']-new_fandango['RATING']
new_fandango['Star_diff']=new_fandango['Star_diff'].round(2)
print(new_fandango)
sns.countplot(data=new_fandango,x='Star_diff')                                   ####
onestardiff=new_fandango[new_fandango['Star_diff']==1]
print(onestardiff)

print('         ')
#all other sites
all_sites=pd.read_csv('all_sites_scores.csv')
print(all_sites)
print(all_sites.columns)
print(all_sites.info())

#Rotten tomato
sns.scatterplot(data=all_sites,x='RottenTomatoes',y='RottenTomatoes_User')          ####
plt.ylim(0,110)


#diffrence in critics and user
all_sites['RT_diff']=all_sites['RottenTomatoes_User']-all_sites['RottenTomatoes']
print(all_sites)
sns.histplot(data=all_sites,x='RT_diff',kde=True)  ###3
plt.ylim(0,40)
plt.xlim(-60,80)


#top 5 user rated compare to critics
Tfive_user=all_sites.nsmallest(5,'RT_diff')[['FILM','RT_diff']]
print(Tfive_user)

#top 5 critic compare to user rated
Tfive_critic=all_sites.nlargest(5,'RT_diff')[['FILM','RT_diff']]
print(Tfive_critic)


#compare it with fandango

df= pd.merge(fandango,all_sites,on='FILM',how='inner')
print(df)

#round of all ratings to 5

print(df.describe().transpose()['max'])

df['RT_Norm']=np.round(df['RottenTomatoes']/20,1)
df['RTU_Norm']=np.round(df['RottenTomatoes_User']/20,1)
df['Meta_Norm']=np.round(df['Metacritic']/20,1)
df['MetaU_Norm']=np.round(df['Metacritic_User']/2,1)
df['IMDB_Norm']=np.round(df['IMDB']/2,1)
print(df.head())
print(df.columns)


all_normscores=df[['STARS', 'RATING','RT_Norm', 'RTU_Norm', 'Meta_Norm', 'MetaU_Norm', 'IMDB_Norm']]
print(all_normscores)


def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = old_legend.get_title().get_text()
    ax.legend(handles, labels, loc=new_loc, title=title, **kws)


fig, ax = plt.subplots()
sns.kdeplot(data=all_normscores,fill=True,clip=(0,5),palette='tab10')
move_legend(ax, "upper left")


#http://github.com/mwaskom/seaborn/issues/2280

#rottentomatoes vs star

fig, ax = plt.subplots()
sns.kdeplot(data=all_normscores[['RT_Norm','STARS','IMDB_Norm']],fill=True,clip=(0,5),palette='tab10') ######
move_legend(ax, "upper left")


#worst to 10 movie compare
worst_normscore=df[['FILM','STARS', 'RATING','RT_Norm', 'RTU_Norm', 'Meta_Norm', 'MetaU_Norm', 'IMDB_Norm']]

worst_flims=worst_normscore.nsmallest(10,'RT_Norm')
print(worst_flims)
sns.kdeplot(data=worst_flims,fill=True,clip=(0,5),palette='tab10')              #####
move_legend(ax, "upper left")

plt.show()


