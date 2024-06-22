import os
import numpy as np
import librosa
import librosa.display

class AudioPreprocessor:
    """
    A class for preprocessing audio files to extract comprehensive features for machine learning models.

    Attributes:
        dataset_dir (str): The directory path where the dataset is stored.
        categories (list of str): A list of categories within the dataset directory that correspond to different classes of audio data.

    Methods:
        extract_features(file_path): Extracts audio features from an audio file.
        load_data(): Loads data from the dataset directory and extracts features and labels.
    """

    def __init__(self, dataset_dir, categories):
        self.dataset_dir = dataset_dir
        self.categories = categories

    def extract_features(self, file_path):
        """
        Extracts multiple audio features from an audio file located at file_path.

        Parameters:
            file_path (str): The path to the audio file from which features are to be extracted.

        Returns:
            numpy.ndarray: A 1D array of extracted audio features.
        """
        audio, sample_rate = librosa.load(file_path, sr=None)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        contrast = librosa.feature.spectral_contrast(y=audio, sr=sample_rate)
        features = np.mean(np.concatenate((mfccs, contrast), axis=0), axis=1)
        return features

    def load_data(self):
        data = []
        labels = []
        for category in self.categories:
            class_label = category[0].upper()
            folder_path = os.path.join(self.dataset_dir, category)
            for filename in os.listdir(folder_path):
                if filename.endswith('.wav'):
                    file_path = os.path.join(folder_path, filename)
                    features = self.extract_features(file_path)
                    data.append(features)
                    labels.append(class_label)
        return np.array(data), np.array(labels)

