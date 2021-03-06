import numpy as np

training_spam = np.loadtxt(open("training_spam.csv"), delimiter=",").astype(np.int)
print("Shape of the spam training data set:", training_spam.shape)

testing_spam = np.loadtxt(open("testing_spam.csv"), delimiter=",").astype(np.int)
print("Shape of the spam testing data set:", testing_spam.shape)


class SpamClassifier:
    def __init__(self):
        pass

    def train(self, data):
        training_labels = training_spam[:, 0]
        training_inputs = training_spam[:, 1:]

        n_spam = np.count_nonzero(training_labels == 1)
        n_ham = np.count_nonzero(training_labels == 0)
        n = len(training_labels)

        prob_spam = np.log(n_spam / n)
        prob_ham = np.log(n_ham / n)

        log_class_priors = np.array([prob_spam, prob_ham])

        all_count = np.sum(training_inputs, axis=0)

        spam_array = np.zeros(shape=(n_spam, training_spam.shape[1] - 1))
        j = 0
        for i in range(0, n):
            if training_spam[i][0] == 1:
                spam_array[j] = training_spam[i][1:]
                j += 1
        spam_count = np.sum(spam_array, axis=0)
        spam_total_count = np.sum(spam_count)
        spam_count = spam_count + 1  # laplace smoothing

        ham_array = np.zeros(shape=(n_ham, training_spam.shape[1] - 1))
        j = 0
        for i in range(0, n):
            if training_spam[i][0] == 0:
                ham_array[j] = training_spam[i][1:]
                j += 1
        ham_count = np.sum(ham_array, axis=0)
        ham_total_count = np.sum(ham_count)
        ham_count = ham_count + 1  # laplace smoothing

        theta = np.zeros(shape=(2, training_spam.shape[1] - 1))
        for i in range(0, training_spam.shape[1] - 1):
            theta[0][i] = np.log(spam_count[i] / (spam_total_count + training_spam.shape[1] - 1))
            theta[1][i] = np.log(ham_count[i] / (ham_total_count + training_spam.shape[1] - 1))

        return log_class_priors, theta

    def predict(self, new_data):
        log_class_priors, theta = self.train(training_spam)
        class_predictions = np.zeros(shape=(new_data.shape[0]))
        for j in range(0, new_data.shape[0]):
            spam_score = 0
            ham_score = 0
            for i in range(0, new_data.shape[1] - 1):
                spam_score += new_data[j][i] * theta[0][i]
                ham_score += new_data[j][i] * theta[1][i]

            if spam_score > ham_score:
                class_prediction = 1
            else:
                class_prediction = 0

            class_predictions[j] = class_prediction
        return class_predictions


def create_classifier():
    classifier = SpamClassifier()
    classifier.train(training_spam)
    return classifier


classifier = create_classifier()
