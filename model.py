from mongoengine import Document, StringField, FloatField

class Data (Document):
    full_name = StringField()
    html_url = StringField()
    description = StringField()
    stargazers_count = FloatField()
    language = StringField()

