# -*- coding: utf-8 -*-
"""
SourcingRequest model module
"""
from backend.backend.models import db
from backend.backend.models.accessor_mixin import AccessorMixin
from backend.backend.models.modified_mixin import ModifiedMixin


class SourcingRequest(AccessorMixin, ModifiedMixin, db.Document):
    """Sourcing Request model"""
    email = db.EmailField(required=True, min_length=1)
    first_name = db.StringField(required=True, min_length=1)
    last_name = db.StringField(required=True, min_length=1)
    phone = db.StringField(required=False, default='')
    company_name = db.StringField(required=False, default='')
    city = db.StringField(required=False, default='Vancouver')

    details = db.StringField(required=True, min_length=1)

    user = db.ReferenceField('User', default=None, reverse_delete_rule=db.DENY)

    pricing_option = db.StringField()

    # Stripe details
    token_id = db.StringField()
    card_id = db.StringField(min_length=10)
    card_address_zip = db.StringField(min_length=15)
    card_address_zip_check = db.BooleanField()
    card_brand = db.StringField(min_length=1)
    card_country = db.StringField(min_length=1)
    card_exp_month = db.StringField(min_length=)
    card_exp_year = db.StringField()
    card_cvc_check = db.BooleanField()
    card_last4 = db.StringField()
    stripe_charge_id = db.StringField()

    def get_details_lines(self):
        """Split the details into a list of lines"""
        return [l.strip() for l in self.details.split('\n')]

    def to_dict(self):
        """SourcingRequest to dict"""
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.first_name,
            'company_name': self.company_name,
            'city': self.city,
            'phone': self.phone,
            'details': self.details,
        }

    def get_price(self):
        """Sourcing Pricing Option to pennies"""
        return {
            'sage sourcing 1.0': 1995,
            'sage sourcing 2.0': 7995,
            'sage sourcing club': 15995
        }[self.pricing_option.lower()]

    def get_gst(self):
        """Get just the GST, in pennies. GST is 5%"""
        return int(round(self.get_price() * 0.05))

    def get_total_price(self):
        """Get the purchase amount, including GST"""
        return self.get_price() + self.get_gst()
