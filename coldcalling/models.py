from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class BusinessManager(BaseUserManager):
    def create_user(self, email, name, contact_person, phone_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            contact_person=contact_person,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, contact_person, phone_number, password=None):
        user = self.create_user(
            email,
            name=name,
            contact_person=contact_person,
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Business(AbstractBaseUser):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    objects = BusinessManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact_person', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Appointment(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date = models.DateTimeField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment with {self.business.name} on {self.date}"

class LoginLogData(models.Model):
    user = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    login = models.DateTimeField(null=True, blank=True)
    logout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.type}"

# # cold_calling_model.py
# import tensorflow as tf
# from tensorflow.keras.layers import Dense, Embedding, LSTM, GlobalMaxPooling1D
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences

# class ColdCallingModel:
#     def __init__(self):
#         self.model = Sequential([
#             Embedding(input_dim=10000, output_dim=16),
#             LSTM(units=32),
#             Dense(units=1, activation='sigmoid')
#         ])
#         self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#         self.tokenizer = Tokenizer(num_words=10000)

#     def train(self, texts, labels):
#         self.tokenizer.fit_on_texts(texts)
#         sequences = self.tokenizer.texts_to_sequences(texts)
#         padded_sequences = pad_sequences(sequences, maxlen=100)
#         self.model.fit(padded_sequences, labels, epochs=10, batch_size=32)

#     def predict(self, text):
#         sequence = self.tokenizer.texts_to_sequences([text])
#         padded_sequence = pad_sequences(sequence, maxlen=100)
#         prediction = self.model.predict(padded_sequence)[0][0]
#         return prediction

#     @staticmethod
#     def create_model(input_shape, num_classes):
#         model = Sequential([
#             Embedding(input_dim=input_shape, output_dim=128),
#             LSTM(units=128),
#             Dense(units=num_classes, activation='softmax')
#         ])
#         model.compile(optimizer='adam',
#                       loss='sparse_categorical_crossentropy',
#                       metrics=['accuracy'])
#         return model


import tensorflow as tf
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class ColdCallingModel:
    def __init__(self):
        self.model = Sequential([
            Embedding(input_dim=10000, output_dim=16),
            LSTM(units=32),
            Dense(units=1, activation='sigmoid')
        ])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.tokenizer = Tokenizer(num_words=10000)

    def train(self, texts, labels):
        self.tokenizer.fit_on_texts(texts)
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=100)
        self.model.fit(padded_sequences, labels, epochs=10, batch_size=32)

    def predict(self, text):
        sequence = self.tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, maxlen=100)
        prediction = self.model.predict(padded_sequence)[0][0]
        return prediction
