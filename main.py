import pandas as pd
from graphviz import Digraph
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from id3 import (
    classify_unknown, 
    get_accuracy_score, 
    id3_algorithm, 
    print_tree
)
from models import Node
from preprocessing import preprocess_dataset
from sklearn.model_selection import train_test_split	
from sklearn.metrics import accuracy_score

import seaborn as sns
import matplotlib.pyplot as plt

# Loading dataset
data = pd.read_csv("elfak.csv")
prediction_class = "enter_elfak"

# Preprocessing data
preprocessed_data = preprocess_dataset(data)
preprocessed_data.head(20)

# Analyze data
preprocessed_data.hist('years', bins=range(18, 23, 1))

cross_tab = pd.crosstab(data['score'], data['school'])
sns.heatmap(cross_tab, annot=True, cmap='YlGnBu', fmt='d')
plt.xlabel('score')
plt.ylabel('school')
plt.title('Heatmap of score vs school')

# ID3
tree_diagraph = Digraph("ID3", filename="id3.gv")
tree_top = Node(preprocessed_data, "")

tree = id3_algorithm(preprocessed_data, prediction_class, tree_top)

print_tree(tree, None, 0, "", tree_diagraph)
tree_diagraph.view()

data_to_classify = pd.read_csv("elfak_classify.csv")
preprocessed_data_to_classify = preprocess_dataset(data_to_classify)
preprocessed_data_to_classify.head(10)
classified_data = classify_unknown(preprocessed_data_to_classify, tree, prediction_class)
print('ID3: ', get_accuracy_score(classified_data))

# CART
data = pd.read_csv("elfak.csv")
preprocessed_data = preprocess_dataset(data)

y = data[prediction_class]
X = data.drop(prediction_class, axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

encoder = OneHotEncoder(handle_unknown='error')
X_train_encoded = encoder.fit_transform(X_train,)
X_test_encoded = encoder.transform(X_test)

decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train_encoded, y_train)
predicted_dataset = decision_tree.predict(X_test_encoded)
print('CART: ', accuracy_score(predicted_dataset, y_test))

# RANDOM FOREST
data = pd.read_csv("elfak.csv")
preprocessed_data = preprocess_dataset(data)

y = data[prediction_class]
X = data.drop(prediction_class, axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
random_forest_classifier = RandomForestClassifier(n_estimators=100)

encoder = OneHotEncoder(handle_unknown='error')
X_train_encoded = encoder.fit_transform(X_train,)
X_test_encoded = encoder.transform(X_test)

random_forest_classifier.fit(X_train_encoded, y_train)
predicted_dataset_rf = random_forest_classifier.predict(X_test_encoded)
print('Random forest: ', accuracy_score(predicted_dataset_rf, y_test))
