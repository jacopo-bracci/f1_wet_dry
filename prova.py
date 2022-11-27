import pandas as pd
a = [['10', '1.2', '4.2'], ['15', '70', '0.03'], ['8', '5', '0']]
df = pd.DataFrame(a, columns=['one', 'two', 'three'])

df['two'] = df['two']*2

marameo = df[df['one'] > df['two']]

print(df)
print(marameo)