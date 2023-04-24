from django.contrib.auth import get_user_model
from StreamStage.templatetags import cross_app_reverse
from django.test import TestCase
from django.test.client import RequestFactory
from StreamStage.settings import DEBUG

# -- Payments imports
import json
import time
import datetime
from accounts.models import Broadcaster
from events.models import (
    Event,
    Category,
    EventShowing,
    TicketListing
)
from .views import (
    add_payment_method,
    get_payment_methods,
    create_payment_intent,
    check_payment_intent,
    remove_payment_method
)

# -- Tests
class PaymentsTest(TestCase):
    def setUp(self):
        DEBUG = True
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            cased_username='test',
        )
        self.user.is_streamer = True
        self.user.save()
        self.user.ensure()

        # -- Create event
        self.event = Event.objects.create(
            description='test',
            title='test',
            over_18s=True,
            broadcaster=Broadcaster.objects.create(
                handle='test',
                streamer=self.user,
                over_18=True,
                name='test',
            )
        )

        self.event.categories.add(Category.objects.create(
            name='test',
        ))

        self.event.save()

        # -- Create event showing
        self.event_showing = EventShowing.objects.create(
            event=self.event,
            country='IE',
            city='Dublin',
            venue='test',
            time=datetime.datetime.now() + datetime.timedelta(days=1),
            max_duration=60,
        )

        # -- Create ticket listing
        self.ticket_listing = TicketListing.objects.create(
            event=self.event,
            showing=self.event_showing,
            price=100,
            ticket_detail='test',
            ticket_type=1,
        )


        # -- Convert user to a dict
        self.user = self.user.__dict__
        
    
    def test_add_payment_method(self): 
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'add_payment'
        ), { 
            'card': '4242424242424242',
            'exp_month': '12',
            'exp_year': '2050',
            'cvc': '123',
            'name': 'test'
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = add_payment_method(request)

        self.assertEqual(response.status_code, 200)

    def test_add_invalid_payment_method(self): 
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'add_payment'
        ), { 
            'card': '4242424242424242',
            'exp_month': '12',
            'exp_year': '2000',
            'cvc': '123',
            'name': 'test'
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = add_payment_method(request)

        self.assertEqual(response.status_code, 400)

    def test_get_payment_methods(self):
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'add_payment'
        ), { 
            'card': '4242424242424242',
            'exp_month': '12',
            'exp_year': '2050',
            'cvc': '123',
            'name': 'test'
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = add_payment_method(request)
        
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        payment_id = json_response['data']['id']
        
        request = RequestFactory()
        request = request.get(cross_app_reverse(
            'accounts', 'get_payments'
        ))

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = get_payment_methods(request)

        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response['data'][0]['id'], payment_id)
        
    def test_remove_payment_method(self):
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'add_payment'
        ), { 
            'card': '4242424242424242',
            'exp_month': '12',
            'exp_year': '2050',
            'cvc': '123',
            'name': 'test'
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = add_payment_method(request)
        
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        payment_id = json_response['data']['id']
        
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'remove_payment'
        ), { 'id': payment_id })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = remove_payment_method(request)

        self.assertEqual(response.status_code, 200)

        request = RequestFactory()
        request = request.get(cross_app_reverse(
            'accounts', 'get_payments'
        ))

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = get_payment_methods(request)

        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response['data']), 0)

    def test_create_payment_intent_out_of_stock(self):
        # -- Add a card 
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'add_payment'
        ), { 
            'card': '4242424242424242',
            'exp_month': '12',
            'exp_year': '2050',
            'cvc': '123',
            'name': 'test'
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = add_payment_method(request)
        
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        payment_id = json_response['data']['id']

        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'create_payment'
        ), { 
            'buyable_id': self.ticket_listing.listing_id,
            'payment_method': payment_id,
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = create_payment_intent(request)

        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['message'], 'Item out of stock!')


    def test_create_payment_intent_saved_card(self):
        self.ticket_listing.maximum_stock = 100
        self.ticket_listing.remaining_stock = 10
        self.ticket_listing.save()

        # -- Add a card 
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'add_payment'
        ), { 
            'card': '4242424242424242',
            'exp_month': '12',
            'exp_year': '2050',
            'cvc': '123',
            'name': 'test'
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = add_payment_method(request)
        
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        payment_id = json_response['data']['id']

        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'create_payment'
        ), { 
            'buyable_id': self.ticket_listing.listing_id,
            'payment_method': payment_id,
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = create_payment_intent(request)

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 'success')
        intent_id = json_response['data']['intent_id']

    def test_create_payment_intent_new_card(self):
        self.ticket_listing.maximum_stock = 100
        self.ticket_listing.remaining_stock = 10
        self.ticket_listing.save()  

        card = {
            'buyable_id': self.ticket_listing.listing_id,
            'payment_method': {
                'card': '4242424242424242',
                'exp_month': '12',
                'exp_year': '2050',
                'cvc': '123',
                'name': 'test',
                'save': False
            }
        }

        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'create_payment'
        ), card, content_type='application/json')

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = create_payment_intent(request)

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 'success')
        intent_id = json_response['data']['intent_id']

        # -- Make sure the card was not saved
        request = RequestFactory()
        request = request.get(cross_app_reverse(
            'accounts', 'get_payments'
        ))

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = get_payment_methods(request)

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response['data']), 0)

    def test_create_payment_intent_new_card_save(self):
        self.ticket_listing.maximum_stock = 100
        self.ticket_listing.remaining_stock = 10
        self.ticket_listing.save()  

        card = {
            'buyable_id': self.ticket_listing.listing_id,
            'payment_method': {
                'card': '4242424242424242',
                'exp_month': '12',
                'exp_year': '2050',
                'cvc': '123',
                'name': 'test',
                'save': True
            }
        }

        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'create_payment'
        ), card, content_type='application/json')

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = create_payment_intent(request)

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 'success')
        intent_id = json_response['data']['intent_id']

        # -- Make sure the card was saved
        request = RequestFactory()
        request = request.get(cross_app_reverse(
            'accounts', 'get_payments'
        ))

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = get_payment_methods(request)

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response['data']), 1)

    def test_check_payment_intent(self):
        self.ticket_listing.maximum_stock = 100
        self.ticket_listing.remaining_stock = 10
        self.ticket_listing.save()

        # -- Add a card 
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'add_payment'
        ), { 
            'card': '4242424242424242',
            'exp_month': '12',
            'exp_year': '2050',
            'cvc': '123',
            'name': 'test'
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = add_payment_method(request)
        
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        payment_id = json_response['data']['id']

        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'create_payment'
        ), { 
            'buyable_id': self.ticket_listing.listing_id,
            'payment_method': payment_id,
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = create_payment_intent(request)

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 'success')
        intent_id = json_response['data']['intent_id']


        # -- Check the intent, loop, leeping 2 seconds between each check
        #    If the intent is not ready after 10 checks, fail the test
        for i in range(10):
            request = RequestFactory()
            request = request.post(cross_app_reverse(
                'accounts', 'check_payment'
            ), { 'intent_id': intent_id })

            request.user = get_user_model().objects.get(id=self.user['id'])
            request.csrf_processing_done = True
            response = check_payment_intent(request)

            self.assertEqual(response.status_code, 200)
            json_response = json.loads(response.content)
            if json_response['status'] == 'success': break
            else: time.sleep(2)

        self.assertEqual(json_response['status'], 'success')
        
    def test_check_start_subscrription_saved_payment(self):
        # -- Add a card 
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'add_payment'
        ), { 
            'card': '4242424242424242',
            'exp_month': '12',
            'exp_year': '2050',
            'cvc': '123',
            'name': 'test'
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = add_payment_method(request)
        
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        payment_id = json_response['data']['id']

        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'create_payment'
        ), { 
            'buyable_id': 'ss_monthly',
            'payment_method': payment_id,
        })

        request.user = get_user_model().objects.get(id=self.user['id'])
        request.csrf_processing_done = True
        response = create_payment_intent(request)

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 'success')
        intent_id = json_response['data']['intent_id']


        # -- Check the intent, loop, leeping 2 seconds between each check
        #    If the intent is not ready after 10 checks, fail the test
        for i in range(10):
            request = RequestFactory()
            request = request.post(cross_app_reverse(
                'accounts', 'check_payment'
            ), { 'intent_id': intent_id })

            request.user = get_user_model().objects.get(id=self.user['id'])
            request.csrf_processing_done = True
            response = check_payment_intent(request)

            self.assertEqual(response.status_code, 200)
            json_response = json.loads(response.content)
            if json_response['status'] == 'success': break
            else: time.sleep(2)

        self.assertEqual(json_response['status'], 'success')