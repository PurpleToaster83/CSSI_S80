import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def month_to_num(month_abbr):
    """
    helper function to convert a month's string
    abreviation to a integer
    """

    # make a dict of value for months
    month_map = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }

    # return an int by indexing with the passed in key
    return month_map[month_abbr]


def visit_to_num(visitor_type):
    """
    helper function to conver the visitor type
    to an integer
    """

    # return 0 if new vistor and 1 if returning visitor
    if visitor_type == 'New_Visitor':
        return 0

    return 1


def string_bool_to_num(string_type):
    """
    helper function to convert a true/false string
    to a boolean
    """

    # if the string is 'FALSE' then return a 0
    if string_type == 'FALSE':
        return 0

    return 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1]) 
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # create a integer list of labels and evidence
    evidence = []
    labels = []

    # open the csv data file and read out the data with a DictReader
    with open(filename, newline='') as csv_file:
        file_content = csv.DictReader(csv_file, delimiter=',')

        for row in file_content:
            user_info = []

            # remove the revenue column from the row and add to revenue list
            labels.append(string_bool_to_num(row['Revenue']))
            del row['Revenue']

            # append features user_info
            user_info.append(int(row['Administrative']))
            user_info.append(float(row["Administrative_Duration"]))
            user_info.append(int(row['Informational']))
            user_info.append(float(row['Informational_Duration']))
            user_info.append(int(row['ProductRelated']))
            user_info.append(float(row['ProductRelated_Duration']))
            user_info.append(float(row['BounceRates']))
            user_info.append(float(row['ExitRates']))
            user_info.append(float(row['PageValues']))
            user_info.append(float(row['SpecialDay']))
            user_info.append(month_to_num(row['Month']))
            user_info.append(int(row['OperatingSystems']))
            user_info.append(int(row['Browser']))
            user_info.append(int(row['Region']))
            user_info.append(int(row['TrafficType']))
            user_info.append(visit_to_num(row['VisitorType']))
            user_info.append(string_bool_to_num(row['Weekend']))

            evidence.append(user_info)

        # check that the csv file loaded properly
        if len(labels) != len(evidence):
            raise Exception("Data not loaded properly")

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # create a nearest_neighbor classifier and fit to the input-output pairs
    neighbor_classifier = KNeighborsClassifier(n_neighbors=1)

    return neighbor_classifier.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    predicted_positive = 0.0
    predicted_negative = 0.0

    # loop over all positions in labels/predictions
    for prediction, label in zip(predictions, labels):

        # if the prediction equals the label
        if prediction == label:

            # increment sensitivity/specificity depending on value of label
            if label == 1:
                predicted_positive += 1
            elif label == 0:
                predicted_negative += 1

    # count how many were actually positive/negative
    true_positive = labels.count(1)
    true_negative = labels.count(0)

    # divide sensitivity and specificity by true positive/negative examples to get decimal value
    sensitivity = predicted_positive / true_positive
    specificity = predicted_negative / true_negative

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
