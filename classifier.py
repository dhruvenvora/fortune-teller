# Classifiers

from sklearn import svm
import utils

# Preprocess the data

# Load the data from JSON file

# Initialize the classifier

clf = SVM()

# Split data in test and training set

# Train data
clf.fit(x_train, y_train)

# Test data
y_pred = clf.predict(x_test)

# Calculate accuracy
accuracy = utils.accuracy(y_pred, y_test)

# Print result and graphs


