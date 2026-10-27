import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

np.random.seed(42)
dates=pd.date_range(start='18/8/2026', periods=100)
sales=np.random.randint(100,500,size=len(dates))
customer=np.random.randint(20,100,size=len(dates))
traffic=np.random.randint(200,800,size=len(dates))
ad_spend=np.random.randint(50,300,size=len(dates))

data=pd.DataFrame({
    'Date': dates,
    'Sales': sales,
    'Customer':customer,
    'traffic':traffic,
    'ad_spend':ad_spend
})
data.set_index('Date',inplace=True)

window_size=10
data['MA_Sales']=data['Sales'].rolling(window=window_size).mean()
data['EWMA_Sales']=data['Sales'].ewm(span=window_size).mean()
data['MA_Customer']=data['Customer'].rolling(window=window_size).mean()
data['EWMA_Customer']=data['Customer'].ewm(span=window_size).mean()
data['MA_traffic']=data['traffic'].rolling(window=window_size).mean()
data['EWMA_traffic']=data['traffic'].ewm(span=window_size).mean()

print("Data With moving averages:")
print(data.head(20))
print("Press Y and enter to continue")
choice=input()

if choice.lower()=='y':
    fig,ax=plt.subplots(figsize=(10,6))
    def update(num):
        ax.clear()
        ax.set_title(f'time series data and moving averages (Day  {num+1})')
        ax.plot(data.index[:num+1],data['Sales'][:num+1],label='Sales',color='blue',alpha=0.5)
        ax.plot(data.index[:num+1],data['MA_Sales'][:num+1],label='MA Sales',color='blue',linestyle='--')
        ax.plot(data.index[:num+1],data['EWMA_Sales'][:num+1],label='EWMA Sales',color='blue',linestyle=':')
    
        ax.plot(data.index[:num+1],data['Customer'][:num+1],label='Customer',color='green',alpha=0.5)
        ax.plot(data.index[:num+1],data['MA_Customer'][:num+1],label='MA Customer',color='green',linestyle='--')
        ax.plot(data.index[:num+1],data['EWMA_Customer'][:num+1],label='EWMA Customer',color='green',linestyle=':')
        
        ax.plot(data.index[:num+1],data['traffic'][:num+1],label='traffic',color='red',alpha=0.5)
        ax.plot(data.index[:num+1],data['MA_traffic'][:num+1],label='MA traffic',color='red',linestyle='--')
        ax.plot(data.index[:num+1],data['EWMA_traffic'][:num+1],label='EWMA traffic',color='red',linestyle=':')
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Values')
        ax.legend(loc='upper left')
        ax.grid(True)
        
    ani=animation.FuncAnimation(fig,update,frames=len(data),repeat=False)
    plt.tight_layout()
    plt.show()
        
        

