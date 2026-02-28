from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def train_model(df, target):
    X = df.drop(target, axis=1)
    Y = df[target]

    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, Y_train)

    predictions = model.predict(X_test)
    score = r2_score(Y_test, predictions)

    return model, score