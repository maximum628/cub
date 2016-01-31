import mongoengine


class AbstractJSONDocument(mongoengine.Document):

    meta = {'abstract': True}

    @classmethod
    def save_document(cls, data):
        """ Save a new document by a given dictionary / json """
        document = cls()
        for key, value in data.iteritems():
            setattr(document, key, value)
        document.save()
        return document


    def update_document(self, data):
        """ Modify a document by a given dictionary / json """
        for key, value in data.iteritems():
            setattr(self, key, value)
        document = self.update()
        return document


class AbstractContribution(AbstractJSONDocument):
    meta = {
        'abstract': True,
        'indexes': [{'fields': ['updated_at']}],
        'ordering': ['-updated_at']
    }

    cub_account = mongoengine.StringField(required=True)
    html_url = mongoengine.URLField(required=True, unique_with='cub_account')
    url = mongoengine.URLField(required=True)
    html_repo_url = mongoengine.URLField(required=True)
    updated_at = mongoengine.DateTimeField(required=True)
    stats = mongoengine.DictField()
