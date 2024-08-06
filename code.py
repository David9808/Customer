%%capture
pip install openpyxl


import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import math

fd=pd.read_excel('C:/Users/obalabi adepoju/Downloads/Quantium/transaction_data.xlsx')
df=pd.read_csv('C:/Users/obalabi adepoju/Downloads/Quantium/purchase_behaviour.csv')

df.head(10)

df.info()

print(f"This dataset has {df.shape[0]} rows, {df.shape[1]} columns and it has no null values.")

print(f"Duplicate Values: {df['LYLTY_CARD_NBR'].duplicated().any()}")

lifestage_counts=df['LIFESTAGE'].value_counts()
lifestage_counts

%matplotlib inline
# Create the histogram
plt = px.histogram(df, x='LIFESTAGE',title='Customer Distribution by Lifestage Category',color='LIFESTAGE')

# Display the chart
plt.show()

df['PREMIUM_CUSTOMER'].value_counts()

plt = px.pie(df, names='PREMIUM_CUSTOMER', title='Customer Distribution',hole=0.4)

plt.show()

fd.info()

print(f"This dataset has {fd.shape[0]} rows, {fd.shape[1]} columns and it has no null values.")

# A preview of the dataset showing the first 10 records
fd.head(10)

fd['PROD_NAME'].value_counts()

print(f"This dataset contains {fd['PROD_NAME'].nunique()} distinct chip names")

print(f"Duplicate Values: {fd['LYLTY_CARD_NBR'].duplicated().any()}")


#Removing Duplicates
fd=fd.drop_duplicates(subset=['LYLTY_CARD_NBR'],keep='first')

# Check if it has been removed
print(f"Duplicate Values: {fd['LYLTY_CARD_NBR'].duplicated().any()}")

fd.info()


print(f"This dataset has {fd.shape[0]} rows and {fd.shape[1]} columns and it has no null values.")

data=pd.merge(df, fd, on='LYLTY_CARD_NBR', how='inner')
data.head(10)

grouped = data.groupby('PROD_NAME').agg(count=('PROD_NAME', 'count'))
grouped = grouped.sort_values('count', ascending=False).reset_index()  # Sorting by count
display(grouped)


grouped.describe()

test=grouped[['PROD_NAME','count']].head(50)
test

test_sample=test.sample(25)# use a subset of our test dataframe as the sample
test_sample

pop_mean=test['count'].mean()# Calculating the mean of our test population

pop_sd=test['count'].std()#Calculating the standard deviation of our test population

samp_mean=test_sample['count'].mean()# Sample mean 

z_value =1.96 
z_score= abs((samp_mean - pop_mean) / (pop_sd/math.sqrt(50)))

print(f"Z-Score: {z_score}")

# We'll be creating a new column called PACK_SIZE
data['PACK_SIZE(G)'] = data['PROD_NAME'].str.extract(r'(\d+)')
data['PACK_SIZE(G)']=pd.to_numeric(data['PACK_SIZE(G)'])

sales= data[['LYLTY_CARD_NBR','LIFESTAGE', 'PREMIUM_CUSTOMER','STORE_NBR' ,'TXN_ID', 'PROD_NBR','PROD_NAME','PACK_SIZE(G)','PROD_QTY','TOT_SALES']]

sales.head()

sales['TOT_SALES'].describe()

sales[sales['TOT_SALES'] >= 50]

# we'll replace the value with what we assume to be the correct entry
sales.iloc[59694,8]=2
sales.iloc[59694,9]=6.5

sales.loc[[59694]]

# We'll then visualize the relationship between packet sizes and total sales.
sales.plot.scatter(x='TOT_SALES',y='PACK_SIZE(G)',alpha=0.25)

g=sales.groupby('PACK_SIZE(G)').agg(count=('PACK_SIZE(G)','count'),sales=('TOT_SALES','sum'))
g = g.sort_values('count',ascending=False).reset_index()# Sorting in descending order to view the top 5 chip preferences
g

test = g.iloc[0:5,0:]
g = g.drop(range(0,5)).reset_index(drop=True)

test1= {"Pack" :['Top_5','others'],
        "count":[test['count'].sum(),g['count'].sum()],
        "sales":[test['sales'].sum(),g['sales'].sum()]
       }
test1=pd.DataFrame(test1)



ax=test1['count'].plot.bar(color='purple')

# Setting the x-axis labels
ax.set_xticklabels(test1['Pack'])

plt.title('Count of Top_5 vs Others')
plt.xlabel('Pack')
plt.ylabel('Count')

fig, ax = plt.subplots()
ax.pie(test1['sales'], labels=test1['Pack'], autopct='%1.1f%%', startangle=90, colors=['lightblue', 'grey'], wedgeprops=dict(width=0.6))

plt.title('Distribution of Sales for Top_5 vs Others')

plt.show()


ax=test['count'].plot.bar()

# Setting the x-axis labels
ax.set_xticklabels(test['PACK_SIZE(G)'])

plt.title('Distribution of Top Choices')
plt.xlabel('Pack')
plt.ylabel('Count')

#Let's see how this affect our sales
ax=test['sales'].plot.bar(color='pink')

ax.set_xticklabels(test['PACK_SIZE(G)'])

plt.title('Distribution of Top Sales')
plt.xlabel('Pack')
plt.ylabel('Sale')

#grouping our data by LIFESTAGE and finding sum of each attribute.
sales.groupby('LIFESTAGE').agg(TSALE=('TOT_SALES','sum')).sort_values('TSALE',ascending=False)

# visualizing our findings using a histogram
map={    
    'YOUNG SINGLES/COUPLES': 'blue',
    'YOUNG FAMILIES': 'grey',
    'OLDER SINGLES/COUPLES': 'blue',
    'MIDAGE SINGLES/COUPLES': 'grey',
    'NEW FAMILIES': 'grey',
    'OLDER FAMILIES': 'grey',
    'RETIREES' : 'blue'
    }
# Create the histogram
plt = px.histogram(data, x='LIFESTAGE',y='TOT_SALES',title='Sales Distribution by Lifestage Category',color='LIFESTAGE',color_discrete_map=map)

# Display the chart
plt.show()

#grouping our data by customer segments and finding sum of each group.
s=sales.groupby('PREMIUM_CUSTOMER').agg(Group=("PREMIUM_CUSTOMER",'first'),TSALE=('TOT_SALES','sum')).sort_values('TSALE',ascending=False)


plt = px.pie(s, names='Group',values='TSALE',title='Sales Segmentation')

plt.show()

sales['TOT_SALES'].describe()

d=sales.TOT_SALES[sales['TOT_SALES']>9.0].count()
d

print(f"Sales greater than 9.0 is only about {round(((d/72637) * 100),2)} % of our data.")

#Let's look at the average sale of eac customer group.
s=sales.groupby('PREMIUM_CUSTOMER').agg(AVG_SALE=('TOT_SALES','mean')).sort_values('AVG_SALE',ascending=False)
s[['AVG_SALE']]

