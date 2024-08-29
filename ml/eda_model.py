# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# %%
df=pd.read_csv("C:/WealthFolio/data/dataset/data.csv")

# %%
df.head(10)

# %%
df.info()

# %%
df.describe(include='all')

# %%
df.nunique()

# %%
cat_cols=df.select_dtypes(include=['object']).columns
num_cols=df.select_dtypes(include=np.number).columns.tolist()
print("Categorical Variables are ",cat_cols)
print("Numerical Variables are ",num_cols)

# %%
# Histogram and Boxplot
for col in num_cols:
    print(col)
    plt.figure(figsize=(15,4))
    plt.subplot(1,2,1)
    sns.histplot(df[col],kde=True)
    plt.ylabel("Count")
    plt.subplot(1,2,2)
    sns.boxplot(df[col])
    plt.show() 

# %%
# Countplot for categorical columns
for col in cat_cols:
    print(col)
    plt.bar(df[col].value_counts().index, df[col].value_counts().values)
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.show()

# %% [markdown]
# Observations:
# Mostly People educated from Bachelor's followed by High School, Masters and Doctorate
# Mostly people has occupation in Healthcare and Technology
# Mostly people belongs to Urban location
# Mostly people are Married
# Mostly people are Full Time employed and least people are self employed
# Mostly people has their own house
# Very least Family prefer Townhouse type of housing
# Almost half families has male as primary household member and half has female
# Mostly people prefer public transport or Car for transportation

# %%
# ScatterPlot
for col in df:
    if col != "Income":
        sns.scatterplot(x=col, y='Income', data=df)
        plt.title(f'Scatter Plot:{col} vs. Annual Household Income')
        plt.show()

# %%
# Lineplot
for col in df:
    if col != "Income":
        sns.lineplot(x=col, y='Income', data=df)
        plt.title(f'Line Plot: {col} vs. Annual Household Income')
        plt.show()

# %%
# Barplot
for col in df:
    if col != "Income":
        sns.barplot(x=col, y='Income', data=df)
        plt.title(f'Box Plot: {col} vs. Annual Household Income')
        plt.show()

# %% [markdown]
#  MultiVariate Analysis

# %%
df1=df.select_dtypes(exclude=['object'])
plt.figure(figsize=(12, 7))
sns.heatmap(df1.corr(),annot=True)
plt.show()

# %%
from sklearn.model_selection import KFold
target = 'Income'
df_encoded = df.copy()

kf = KFold(n_splits=5, shuffle=True, random_state=1)

for col in cat_cols:
    col_encoded = f'{col}_encoded'
    df_encoded[col_encoded] = 0
    
    for train_index, val_index in kf.split(df):
        X_train, X_val = df.iloc[train_index], df.iloc[val_index]
        means = X_train.groupby(col)[target].mean()
        df_encoded.loc[val_index, col_encoded] = df.loc[val_index, col].map(means)
    df_encoded[col_encoded].fillna(df[target].mean(), inplace=True)
    df_encoded.drop(columns=[col], inplace=True)

df_encoded.head()

# %% [markdown]
#  Train-test split

# %%
x=df_encoded.drop(["Income"],axis=1)
y=df_encoded["Income"]

# %%
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

# %% [markdown]
#  Feature Scaling

# %%
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

scaler.fit(x_train)

x_train_scaled = scaler.transform(x_train)
x_test_scaled = scaler.transform(x_test)

x_train_scaled = pd.DataFrame(x_train_scaled, columns=x_train.columns, index=x_train.index)
x_test_scaled = pd.DataFrame(x_test_scaled, columns=x_test.columns, index=x_test.index)

x_train_scaled.head()

# %% [markdown]
#  Model Creation

# %% [markdown]
# 1. Linear Regression

# %%
lr = LinearRegression()
lr.fit(x_train, y_train)
y_pred_lr = lr.predict(x_test)

# %% [markdown]
# 2. Gradient Boosting Regressor

# %%
gbr = GradientBoostingRegressor()
gbr.fit(x_train, y_train)
y_pred_gbr = gbr.predict(x_test)

# %% [markdown]
# 3. Elastic Net Regression

# %%
from sklearn.linear_model import ElasticNet
en = ElasticNet()
en.fit(x_train, y_train)
y_pred_en = en.predict(x_test)

# %% [markdown]
# 4. Lasso Regression

# %%
from sklearn.linear_model import Lasso
lasso = Lasso()
lasso.fit(x_train, y_train)
y_pred_lasso = lasso.predict(x_test)

# %% [markdown]
# 5. Decision Tree Regressor

# %%
from sklearn.tree import DecisionTreeRegressor
dt = DecisionTreeRegressor()
dt.fit(x_train, y_train)
y_pred_dt = dt.predict(x_test)

# %% [markdown]
# 6. Random Forest Regressor

# %%
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
rf.fit(x_train, y_train)
y_pred_rf = rf.predict(x_test)

# %% [markdown]
# Model Selection
# Comparing All Evaluation Metrics in Increasing Order

# %%
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Initialize an empty DataFrame for model comparison
model_comparison = pd.DataFrame(columns=['Model', 'MAE', 'MSE', 'RMSE', 'R²'])

# Define a function to add the model's metrics to the DataFrame
def add_model_metrics(model_name, y_test, y_pred):
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    
    return pd.DataFrame({
        'Model': [model_name],
        'MAE': [mae],
        'MSE': [mse],
        'RMSE': [rmse],
        'R²': [r2]
    })

# Gradient Boosting Regressor
model_comparison = pd.concat([model_comparison, add_model_metrics('Gradient Boosting Regressor', y_test, y_pred_gbr)], ignore_index=True)

# Linear Regression
model_comparison = pd.concat([model_comparison, add_model_metrics('Linear Regression', y_test, y_pred_lr)], ignore_index=True)

# Elastic Net Regression
model_comparison = pd.concat([model_comparison, add_model_metrics('Elastic Net Regression', y_test, y_pred_en)], ignore_index=True)

# Lasso Regression
model_comparison = pd.concat([model_comparison, add_model_metrics('Lasso Regression', y_test, y_pred_lasso)], ignore_index=True)

# Decision Tree Regressor
model_comparison = pd.concat([model_comparison, add_model_metrics('Decision Tree Regressor', y_test, y_pred_dt)], ignore_index=True)

# Random Forest Regressor
model_comparison = pd.concat([model_comparison, add_model_metrics('Random Forest Regressor', y_test, y_pred_rf)], ignore_index=True)

# Print the model comparison table
print(model_comparison)

# Plotting all evaluation metrics in increasing order
metrics = ['MAE', 'MSE', 'RMSE', 'R²']
plt.figure(figsize=(14, 10))

for i, metric in enumerate(metrics, 1):
    sorted_comparison = model_comparison.sort_values(by=metric, ascending=(metric != 'R²'))
    plt.subplot(2, 2, i)
    plt.bar(sorted_comparison['Model'], sorted_comparison[metric])
    plt.xlabel('Model')
    plt.ylabel(metric)
    plt.title(f'Model Comparison: {metric}')
    plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


