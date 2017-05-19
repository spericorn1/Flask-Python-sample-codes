# -*- coding: utf-8 -*-
"""
Eventsage's interface module for Stripe
"""
import stripe


class EventsageStripe(object):
    """
    The object used to communicate with Stripe's API.
    """

    def init_app(self, app):
        """
        Initialize Stripe for the provided app.

        this method conforms to the Flask-style standard of initializing
        modules that depend on the app they are running in.
        """
        stripe.api_key = app.config['STRIPE_API_KEY']

    def cancel_subscription(self, customer=None, user=None):
        """
        Cancel a subscription.

        cancels a customer's current subscription.
        """
        if not customer and not user:
            raise UnboundLocalError('customer or user required')

        if not customer:
            customer = self.get_customer(user)

        return customer.cancel_subscription(at_period_end=True)

    def create_customer(self, user, card_token, plan):
        """
        Create a new stripe customer for the given user.

        saves the customer id to the user instance.
        """
        customer = stripe.Customer.create(
            card=card_token,
            plan=plan,
            email=user.email,
        )
        user.stripe_customer_id = customer.id
        user.save()
        return customer

    def get_customer(self, user):
        """
        Return the Stripe customer for the given user.
        """
        if not user.stripe_customer_id:
            return None

        return stripe.Customer.retrieve(user.stripe_customer_id)

    def get_plans(self):
        """
        Return all plans available to be subscribed to.
        """
        return stripe.Plan.all()

    def update_subscription(self, plan, customer=None, user=None):
        """
        Update a subscription.

        changes a current customer's subscription to a new one.
        """
        if not customer and not user:
            raise UnboundLocalError('customer or user required')

        if not customer:
            customer = self.get_customer(user)

        return customer.update_subscription(
            plan=plan,
            trial_end='now',
        )
