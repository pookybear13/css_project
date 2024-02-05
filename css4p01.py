import pandas as pd

"""
cleaning the data
"""

df = pd.read_csv('movie_dataset.csv',index_col=0) #i think rank actually just an index

pd.set_option('display.max_rows',None)
print(df.info())
#print(df.describe())

#creating col with names without spaces and dropping those without
df['Runtime_in_min'] = df['Runtime (Minutes)']

df.drop(columns=['Runtime (Minutes)'],inplace=True)

df['Revenue_in_mil'] = df['Revenue (Millions)']

df.drop(columns=['Revenue (Millions)'],inplace=True) 

print(df.info())

#print(df.loc[357])

df.drop(357, inplace = True) #removing row 357 as there is a wrong entry. As a result we lose information on both the rating and metascore

df = df.reset_index(drop=True) #resetting index

print(df.info())

#print(df.loc[969])

"""
Dealing with nan values. 
Upon comparision with IMDB online, most of the values for the metascore correspond with what's available online. For nan values in the metascore
we replace with the metascore values found online for the movie in the row with that nan value. Similarily, we can jus
"""

#movie Paris pieds nus
df.loc[25,'Metascore'] = 74 

print('\n')
print('mode is:')
print(df['Metascore'].mode())
print('mean is:')
print(df['Metascore'].mean())

#checking number of blank entries in metascore
Null_meta = df['Metascore'].isnull().sum()
print('No. of empty cells: ',Null_meta)

"""
ok we've got way too many nan values for the metascore so we're gonna replace these vales with the mode. We replace them with the mode because in theory, the mean and the mode should 
be close to the mean but in this case they aren't. This hints that there are outliers that are skewing the mean. Because of this, I've decided to use the mode. We will use the mode as 66
"""
mode = 66

df["Metascore"].fillna(mode, inplace = True)

#checking for nans
Null_meta = df['Metascore'].isnull().sum()
print('empty cells: ',Null_meta)

#checking no. of empty cells in the revenue col
Null_rev = df['Revenue_in_mil'].isnull().sum()
print('no. of empty cells in revenue col: ',Null_rev)

"""
Ok there are way too many empty cells in this column. We cant drop all these rows as this will skew the data too much. 
"""

#checking mean and mode of Rev col
print('\n')
print('the mean is:')
print(df['Revenue_in_mil'].mean())
print('the mode is:')
print(df['Revenue_in_mil'].mode())
print(df['Revenue_in_mil'].describe())

#we gonna fill these nans with the mean
mean = df['Revenue_in_mil'].mean()
df['Revenue_in_mil'].fillna(mean,inplace=True)
#checkinf if empty
print(df['Revenue_in_mil'].describe())
Null_rev = df['Revenue_in_mil'].isnull().sum()
print('no. of empty cells in revenue col: ',Null_rev)

#cheking for nan vals in the other cols
Null_year = df['Year'].isnull().sum()
print('no. of nan in year: ', Null_year)

Null_runtime= df['Runtime_in_min'].isnull().sum()
print('no. of nan in runtime: ',Null_runtime)

Null_rate = df['Rating'].isnull().sum()
print('No. of nan in rating: ',Null_rate)

Null_votes = df['Votes'].isnull().sum()
print('no. of nan in votes: ', Null_votes)

#ok no empty entries in these columns

#############################################################################################################################################################################
#############################################################################################################################################################################
"""
Quiz questions
"""
print('\n')

#finding highest rated movie 
row = df.loc[df['Rating'].idxmax()]
print('highest rated movie')
print(row)

#Average revenue 
Ave_rev = df['Revenue_in_mil'].mean()
print('average revenue: ', Ave_rev)

import numpy as np

#getting indices of movies in year 2015
idx_2015 = df.index[df['Year'] == 2015].tolist()
#print(idx_2015)

#indices of movies in year 2016
idx_2016 = df.index[df['Year'] == 2016].tolist()
print(len(idx_2016)) #note gives 296 cos we dropped one movie which was released in 2016

#indices of movies in 2017 
idx_2017 = df.index[df['Year'] == 2017].tolist()

#indices of movies from 2015 - 2017

Idx = []

for i in range(len(idx_2015)):
  Idx.append(idx_2015[i])
  
for i in range(len(idx_2016)):
  Idx.append(idx_2016[i])
  
for i in range(len(idx_2017)):
  Idx.append(idx_2017[i])
  
#print(np.shape(Idx))
#print(idx_2017)
Rev = []

#cycling through the indices to get value in Rev col
for i in range(len(Idx)):
   Rev.append(df.loc[i,'Revenue_in_mil'])
   
#print(Rev)

Revenue = np.array(Rev)

#getting mean 
mean = Revenue.mean()
print('Average revenue between 2015 and 2017: ', mean)


#Movies by Christopher Nolan
idx_Nolan = df.index[df['Director'] == 'Christopher Nolan'].tolist()
print('No. of movies by Nolan: ',len(idx_Nolan))

#movies with rating 8.0
idx_8 = df.index[df['Rating'] >= 8.0].tolist()
print('No. of movies with rating 8.0: ', len(idx_8))

#median rating of Nolan movies 
"""
Nolan_rating = []

for i in range(len(idx_Nolan)):
  Nolan_rating.append(df.loc[i,'Rating'])
  print(df.loc[i,'Rating'])

Ratings = np.array(Nolan_rating)
print(Ratings)
print('median rating of Nolan movies: ', np.median(Ratings))
"""

Direct_g = df.groupby('Director')
CG = Direct_g.get_group('Christopher Nolan')
print('Medain rating by Nolan: ', CG['Rating'].median())
#finding year with highest rating
yg = df.groupby('Year')
#getting years in data set 

year = np.arange(2000,2022,1)

Year_g = []
y_used = []

for i in range(len(year)):
  y = year[i]
  if y in df['Year'].values:
    Year_g.append(yg.get_group(y))
    y_used.append(y)
  else:
     print(f"{y} does not exist in the DataFrame.")
     
#Num_year = len(Year_g)
#me = Year_g[0]
print(y_used)
print(Year_g[0]['Rating'].mean())

#getting mean rating for each year
for i in range(len(Year_g)):
  y = y_used[i]
  print(f" mean for {y}:", Year_g[i]['Rating'].mean()) 
  
#finding increas in movies from 2006 to 2016
print(len(Year_g[1]))

for i in range(len(Year_g)):
  y = y_used[i]
  print(f"No. of movies in {y}: ",len(Year_g[i]))
  
#No. of movies in 2006
mi = len(Year_g[0])

#No. of movies in 2016
mf = len(Year_g[10])

#percentage increase 
P = ((mf -mi)/mi) *100
print(P)

##Finding actor in most movies

#a = df.loc[1,'Actors'].split(',')

#print(len(df['Actors']))

actors = []

for i in range(len(df['Actors'])):
   a = df.loc[i,'Actors'].split(',')
   for b in range(len(a)):
     actors.append(a[b])
   
#print(actors)

name_series = pd.Series(actors)

# use value_counts() to get the counts of each unique word
name_counts = name_series.value_counts()

print("Most frequent name is", name_counts.index[0])

#finding number of unique genres
genres = []

for i in range(len(df['Genre'])):
   a = df.loc[i,'Genre'].split(',')
   for b in range(len(a)):
     genres.append(a[b])


word_series = pd.Series(genres)

#getting counts of ech unique genre
genre_counts = word_series.value_counts()

#length of genre counts must be total number of unique genres
print('the number of unique genres is ', len(genre_counts))
"""
#Correlations
Cor1 = df['Rating'].corr(df['Year'])
print('Correlation between year and rating:',Cor1)

Cor2 = df['Rating'].corr(df['Revenue_in_mil'])
print('Correlation between rating and revenue:',Cor2)

Cor3 = df['Rating'].corr(df['Metascore'])
print('Correlation between rating and metascore:',Cor3)

Cor4 = df['Rating'].corr(df['Votes'])
print('Correlation between rating and votes:',Cor4)

Cor5 = df['Runtime_in_min'].corr(df['Rating'])
print('Correlation between runtime and rating:',Cor5)

Cor=  df.corr()[['Year', 'Rating', 'Votes']]
"""

#dropping cols we dont need for correlation 

df.drop(columns=['Title'],inplace=True)
df.drop(columns=['Genre'],inplace=True)
df.drop(columns=['Description'],inplace=True)
df.drop(columns=['Director'],inplace=True)
df.drop(columns=['Actors'],inplace=True)

#print(df.info())
pd.set_option('display.max_rows', None)
cor = df.corr()
print(cor)

 
