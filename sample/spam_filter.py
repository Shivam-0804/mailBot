import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from pathlib import Path
file_path = Path(__file__).parent / 'mail_data.csv'

raw_mail_data = pd.read_csv(file_path)

mail_data = raw_mail_data.fillna('')
mail_data['Category'] = mail_data['Category'].map({'spam': 0, 'ham': 1})

X = mail_data['Message']
Y = mail_data['Category']

X_Train, X_test, Y_Train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)
vectorizer = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)

X_train_features = vectorizer.fit_transform(X_Train)
X_test_features = vectorizer.transform(X_test)

Y_Train = Y_Train.astype('int')
Y_test = Y_test.astype('int')

model = LogisticRegression()
model.fit(X_train_features, Y_Train)

# train_predictions = model.predict(X_train_features)
# train_accuracy = accuracy_score(Y_Train, train_predictions)
# print(f"Accuracy on Training Data: {train_accuracy * 100:.2f}%")

print("Spam Filter: ")
input("Enter a mail: ")
input_mail = ["As a valued customer, I am pleased to advise you that following recent review of your Mob No. you are awarded with a £1500 Bonus Prize, call 09066364589"]
input_data_features = vectorizer.transform(input_mail)

prediction = model.predict(input_data_features)[0]

print("Output: ")
if prediction == 1:
    print("This is a Ham Mail.")
else:
    print("This is a Spam Mail.")
