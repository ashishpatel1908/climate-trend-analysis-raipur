import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('Python/temperature.csv')
df['Date']=pd.to_datetime(df['Date'],format='%d-%m-%Y')
df[['Temp Max','Temp Min','Rain']]=df[['Temp Max','Temp Min','Rain']].apply(pd.to_numeric,errors='coerce')
df = df[df['Date'].dt.year < 2024]
day_of_year=df['Date'].dt.dayofyear

#Grouping according to year
his_avg=df.groupby(day_of_year)[['Temp Max','Temp Min','Rain']].transform('mean')
df[['Temp Max','Temp Min','Rain']]=df[['Temp Max','Temp Min','Rain']].fillna(his_avg)
group=df.groupby(df['Date'].dt.year)[['Temp Max','Temp Min','Rain']].mean()

#Grouping according to decade
df['Decade']=(df['Date'].dt.year//10)*10
decadal_avg=df.groupby('Decade')[['Temp Max','Temp Min','Rain']].mean()


#Monthly trends
df['Month']=df['Date'].dt.month
months=df.groupby('Month')[['Temp Max','Temp Min','Rain']].mean()
months.index=['Jan','Feb','Mar','Apr','May','Jun',
                 'Jul','Aug','Sep','Oct','Nov','Dec']

#HeatWave
df['Heatwave']=df['Temp Max']>40
heatwave_per_year=df.groupby(df['Date'].dt.year)['Heatwave'].sum()

#Rainfall
rainfall=df.groupby(df['Date'].dt.year)['Rain'].sum()

#Temperature Rise
first=group[group.index<1960]['Temp Max'].mean()
last=group[group.index>2011]['Temp Max'].mean()
rise=last-first

#Heatwave Rise
early = heatwave_per_year[heatwave_per_year.index < 1971].mean()
recent = heatwave_per_year[heatwave_per_year.index > 2003].mean()

#Conclusion
print(f'Hottest Month      :{months["Temp Max"].idxmax()}')
print(f'Coldest Month      :{months["Temp Min"].idxmin()}')
print(f'Temperature Rise   :{rise:.2f} degree C over 73 years')
print(f'Highest Rain Year  :{rainfall.idxmax()}({rainfall.max():.0f} mm)')
print(f'Lowest Rain Year   :{rainfall.idxmin()}({rainfall.min():.0f} mm)')
print(f"Heatwave days 1950s:{early:.1f} days/year")
print(f"Heatwave days 2000s:{recent:.1f} days/year")


#PLots
fig ,ax=plt.subplots(nrows=2,ncols=2,figsize=(10,6))
ax[0,0].plot(group.index,group['Temp Max'],marker='o',color='#fcba03')
ax[0,0].plot(group.index,group['Temp Min'],marker='o',color='#0c149c')
ax[0,0].set_title('Yearly temperature')
ax[0,0].legend(['Temp Max','Temp Min'])


ax[1,1].plot(decadal_avg.index,decadal_avg['Temp Max'],marker='+',color='#fcba03')
ax[1,1].plot(decadal_avg.index,decadal_avg['Temp Min'],marker='+',color='#0c149c')
ax[1,1].set_title('Decadal temperature')
ax[1,1].legend(['Temp Max','Temp Min'])

ax[0,1].bar(rainfall.index,rainfall,color='#1a93d9')
ax[0,1].set_title('Yearly accumulated rainfall(mm)')
ax[0,1].legend(['Rainfall'])

ax[1,0].plot(months.index,months['Temp Max'],marker='o',color='#fcba03')
ax[1,0].plot(months.index,months['Temp Min'],marker='o',color='#0c149c')
ax[1,0].set_title('Monthly temperature')
ax[1,0].legend(['Temp Max','Temp Min'])


plt.tight_layout()
plt.show()
