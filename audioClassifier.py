from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report


class AudioClassifier:

    def __init__(self, preprocessor):
        self.y_test = None
        self.X_test = None
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.encoder = LabelEncoder()
        self.preprocessor = preprocessor

    def train(self, X, y):
        y_encoded = self.encoder.fit_transform(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.4, random_state=42)
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test

    def evaluate(self):
        predictions = self.model.predict(self.X_test)
        print(classification_report(self.y_test, predictions, target_names=self.encoder.classes_))

    def predict(self, file_path):
        features = self.preprocessor.extract_features(file_path)
        features = features.reshape(1, -1)  # Reshape for a single sample prediction
        prediction = self.model.predict(features)
        return self.encoder.inverse_transform(prediction)[0]
