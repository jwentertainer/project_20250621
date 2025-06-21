import pandas as pd

# 깃허브의 ‘Raw’ 링크로 접근
url = 'https://raw.githubusercontent.com/jwentertainer/project_20250621/blob/main/growup.csv'
df = pd.read_csv(url)

print(df.head())
