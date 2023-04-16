import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load


class PhishingModel:
    """

    """

    # default values
    model_path = "model/PhishingModel.joblib"
    data = pd.read_csv("dataset/phishing.csv")

    def split_labels(self):
        """
            split into data and labels
            :return: split data
        """
        X = self.data.drop(['class'], axis=1)
        y = self.data['class']
        discrete_features = X.dtypes == int
        return X, y, discrete_features

    def mi_scores(self):
        """
            Find most valuable scores
            :return: scores
        """
        X, y, discrete_features = self.split_labels()
        mi_scores = mutual_info_classif(X, y, discrete_features=discrete_features)
        mi_scores = pd.Series(mi_scores, name='MI Scores', index=X.columns)
        mi_scores = mi_scores.sort_values(ascending=False)
        return mi_scores

    def get_features(self):
        return ['text_link_disparity', 're_mail', 'urls', 'body_richness', 'contains_prime_targets', 'contains_account', 'domains', 'HTML', 'malicious_urls', 'ip_urls', 'attachments', 'dots_count', 'hex_urls', 'mailto', 'contains_update', 'contains_access']

    def get_data_with_mi_features(self):
        """
            Get most valuable features according to mi scores and features count
            :return: X, y split data with mi features
        """
        features = self.get_features()
        X = self.data[features]
        y = self.data['class']
        return X, y

    def train(self):
        """
            Train model using RandomForestClassifier
            :return: trained RandomForestClassifier model
        """
        X, y = self.get_data_with_mi_features()

        rfc = RandomForestClassifier(
            n_estimators=10,
            n_jobs=64
        )

        rfc.fit(X, y)

        return rfc

    def save_model(self, model):
        """
            Save model to provided path
            :return: void
        """
        dump(model, self.model_path)
        print("Model saved to path ", self.model_path)

    def train_and_save(self):
        """
            Train model and save to provided path
            :return: void
        """
        self.save_model(
            self.train()
        )

    # todo can be improved to calculated accuracy, use more test data and etc.
    def test(self):
        """
            Test model with first and last 10 rows of data
            :return: void
        """
        X, y = self.get_data_with_mi_features()
        model = load(self.model_path)

        print("Predictions from the beginning")
        print("Predicted:")
        print(model.predict(X.head(10)))
        print("Expected:")
        print(y.head(10))

        print("Predictions from the end")
        print("Predicted:")
        print(model.predict(X.tail(10)))
        print("Expected:")
        print(y.tail(10))

    def predict(self, data):
        """
        :param data: collected data with features to predict if email is phishing
        :return: {0, 1} predicted value. 1 means phishing detected
        """
        model = load(self.model_path)
        return model.predict(data)
