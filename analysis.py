
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def getYear(movieName):
    movie_list = movieName.split()
    movie_year = movie_list[-1]
    movie_year = movie_year.replace('(','')
    movie_year = movie_year.replace(')','')
    return int(movie_year)
    

fandango_df = pd.read_csv('DATA\\fandango_scrape.csv')

#Overview of the fandango data
print(fandango_df.info())
print(fandango_df.describe().transpose())


#scatterplot between rating and votes
sns.scatterplot(data=fandango_df,x='RATING',y='VOTES')
plt.savefig('figures\\Rating_Vs_Votes.jpg',bbox_inches='tight')
plt.show()




print(fandango_df.corr())

#scraping a new featur for further analysis
fandango_df['YEAR'] = fandango_df['FILM'].apply(getYear)
print(fandango_df.head())
print(fandango_df['YEAR'].value_counts())


sns.countplot(data=fandango_df,x='YEAR')
plt.savefig('figures\\Year_CountPlot.jpg',bbox_inches='tight')
plt.show()



#displaying 10 movies with the highest number of votes
print(fandango_df.sort_values('VOTES',ascending=False)[0:10])

print(len(fandango_df[fandango_df['VOTES'] == 0]))


fandango_df = fandango_df[fandango_df['VOTES'] != 0]
print(len(fandango_df))
print(fandango_df.head())
sns.kdeplot(data=fandango_df,x='RATING',shade=True,label='True Rating')
sns.kdeplot(data=fandango_df,x='STARS',shade=True,label='Stars Displayed')
plt.legend(loc=(1.05,0.5))
plt.savefig('figures\\Rating_Stars_Dis.jpg',bbox_inches='tight')
plt.show()



#Quantifying the discrepancy
fandango_df['STARS_DIFF'] = np.round(np.abs(fandango_df['STARS']-fandango_df['RATING']),2)
print(fandango_df.head())


#plotting the discrepancy 
sns.countplot(data=fandango_df,x='STARS_DIFF')
plt.savefig('figures\\Stars_Diff.jpg',bbox_inches='tight')
plt.show()


print(fandango_df.sort_values('STARS_DIFF',ascending=False).iloc[0])


#P3: Comparison of fandango ratings to other sites

all_sites = pd.read_csv('DATA\\all_sites_scores.csv')

#Exploring the df
print(all_sites.head())
print(all_sites.info())
print(all_sites.describe())


#Rotten Tomatoes
sns.scatterplot(data=all_sites,x='RottenTomatoes',y='RottenTomatoes_User')
plt.savefig('figures\\RottenTomatoes.jpg',bbox_inches='tight')
plt.show()


#Quantifying the discrepancy on RT website
all_sites['Rotteb_Diff'] = all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']
all_sites['Abs_Rotten_Diff'] = all_sites['Rotteb_Diff'].abs()
print(f"Mean absolute RT difference {all_sites['Abs_Rotten_Diff'].mean()}")


#plotiing the distribution of the RottenTomatoes_Diff
sns.displot(data=all_sites,x='Rotteb_Diff',kde=True)
plt.savefig('figures\\RottenTomatoes_Diff_Dis.jpg',bbox_inches='tight')
plt.show()

#plotiing the distribution of the Abs_RottenTomatoes_Diff
sns.displot(data=all_sites,x='Abs_Rotten_Diff',kde=True)
plt.savefig('figures\\RottenTomatoes_Abs_Diff_Dis.jpg',bbox_inches='tight')
plt.show()


#Top 5 movies users rated higher than the critic
movies_with_neg_score = all_sites[all_sites['Rotteb_Diff']<0]
print(movies_with_neg_score.sort_values('Rotteb_Diff')[0:5][['FILM','Rotteb_Diff']])


#top 5 movies critics rated higher than the users
movies_with_pos_score = all_sites[all_sites['Rotteb_Diff']>0]
print(movies_with_pos_score.sort_values('Rotteb_Diff',ascending=False)[0:5][['FILM','Rotteb_Diff']])


#METACRITIC
sns.scatterplot(data=all_sites,x='Metacritic',y='Metacritic_User')
plt.savefig('figures\\MetaCritic.jpg',bbox_inches='tight')
plt.show()


#Comparing MrtaCritic and IMDb
sns.scatterplot(data=all_sites,x='Metacritic_user_vote_count',y='IMDB_user_vote_count')
plt.savefig('figures\\MetaCritic_Vs_IMDB.jpg',bbox_inches='tight')
plt.show()

#two outliers
print(all_sites.sort_values('IMDB_user_vote_count',ascending=False).iloc[0])
print(all_sites.sort_values('Metacritic_user_vote_count',ascending=False).iloc[0])

#Fandango Scores vs all sites
#merging the databases
combined_df = pd.merge(fandango_df,all_sites,how='inner',on='FILM')
print(combined_df.info())

print(combined_df.head())


#Not all ratings are in the order of the 0 - 5, hence scoes need to be normalized
combined_df['RottenTomatoes_Norm'] = combined_df['RottenTomatoes']/20
combined_df['RottenTomatoes_User_Norm'] = combined_df['RottenTomatoes_User']/20
combined_df['Metacritic_Norm'] = combined_df['Metacritic']/20
combined_df['Metacritic_User_Norm'] = combined_df['Metacritic_User']/2
combined_df['IMDB_Norm'] = combined_df['IMDB']/2

print(combined_df.head())



#collecting all normalized scores into a seperate df
normalized_df = combined_df[['STARS','RATING','RottenTomatoes_Norm','RottenTomatoes_User_Norm','Metacritic_Norm','Metacritic_User_Norm','IMDB_Norm']]
print(normalized_df.head())




#comparing the distribution of normalized socres across all sites
sns.kdeplot(data=normalized_df,x='STARS',shade=True,palette='Set1',label='STARS')
sns.kdeplot(data=normalized_df,x='RATING',shade=True,palette='Set1',label='Rating')
sns.kdeplot(data=normalized_df,x='RottenTomatoes_Norm',shade=True,palette='Set1',label='RottenTomatoes_Norm')
sns.kdeplot(data=normalized_df,x='RottenTomatoes_User_Norm',shade=True,palette='Set1',label='RottenTomatoes_User_Norm')
sns.kdeplot(data=normalized_df,x='Metacritic_Norm',shade=True,palette='Set1',label='Metacritic_Norm')
sns.kdeplot(data=normalized_df,x='Metacritic_User_Norm',shade=True,palette='Set1',label='Metacritic_User_Norm')
sns.kdeplot(data=normalized_df,x='IMDB_Norm',shade=True,palette='Set1',label='IMDB_Norm')
plt.legend(loc=(1.05,0.5))
plt.savefig('figures\\All_Sites_Normalized_score.jpg',bbox_inches='tight')
plt.show()


#clearly RottenTomatoes_Norm has the most uniform distribution
#comparing the RottenTomatoes_Norm vs Stars of Fandango
sns.kdeplot(data=normalized_df,x='STARS',shade=True,palette='Set1',label='STARS')
sns.kdeplot(data=normalized_df,x='RottenTomatoes_Norm',shade=True,palette='Set1',label='RottenTomatoes_Norm')
plt.legend(loc=(1.05,0.5))
plt.savefig('figures\\Stars_VS_RottenTomatoes_Norm.jpg',bbox_inches='tight')
plt.show()


#creation of a clusterMap of all normalized scores across all the sites
sns.clustermap(data=normalized_df,cmap='magma',col_cluster=False)
plt.savefig('figures\\ClusterMap.jpg',bbox_inches='tight')
plt.show()


#collecting top 10 worst movies according to RottenTomatoes_Norm
top_10 = normalized_df.sort_values('RottenTomatoes_Norm')[0:10]
print(top_10)

#plotting the distributuion of top_10 worst movies
sns.kdeplot(data=top_10,x='STARS',shade=True,palette='Set1',label='STARS')
sns.kdeplot(data=top_10,x='RATING',shade=True,palette='Set1',label='Rating')
sns.kdeplot(data=top_10,x='RottenTomatoes_Norm',shade=True,palette='Set1',label='RottenTomatoes_Norm')
sns.kdeplot(data=top_10,x='RottenTomatoes_User_Norm',shade=True,palette='Set1',label='RottenTomatoes_User_Norm')
sns.kdeplot(data=top_10,x='Metacritic_Norm',shade=True,palette='Set1',label='Metacritic_Norm')
sns.kdeplot(data=top_10,x='Metacritic_User_Norm',shade=True,palette='Set1',label='Metacritic_User_Norm')
sns.kdeplot(data=top_10,x='IMDB_Norm',shade=True,palette='Set1',label='IMDB_Norm')
plt.legend(loc=(1.05,0.5))
plt.savefig('figures\\top_10_worst_movies.jpg',bbox_inches='tight')
plt.show()




