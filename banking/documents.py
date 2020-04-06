from django.conf import settings
from django_elasticsearch_dsl import DocType, fields, Index

from .models import Account

accounts = Index('accounts')

accounts.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@accounts.doc_type
class AccountDocument(DocType):
    holder = fields.ObjectField(properties={
        'email': fields.TextField(),
    })
    class Meta:
        model = Account
        fields = [
            'created',
            'status'
        ]

        related_models = [settings.AUTH_USER_MODEL]