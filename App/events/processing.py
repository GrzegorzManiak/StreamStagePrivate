from .models import *
from StreamStage.identifiers import generate_event_id

from .ticketing import create_ticket_listing
from .ticketing import TicketType

# Viewing an individual Event

# Utility Functions
                    # **************
                    # ***Reviews ***
                    # **************
# Get All Reviews                    
def get_reviews(self):
    return EventReview.objects.filter(event=self).all()

# Get Reviews Count                    
def get_review_count(self):
    return get_reviews().count()

# Get Top Rated Review                    
def get_top_review(self, reviews_in = None):
    reviews = reviews_in or self.get_reviews()

    top_review = None
    rating = 0
    for review in reviews:
        if review.rating > rating:
            rating = review.rating
            top_review = review
    return top_review

# Get Overall Review Rating
def get_average_rating(self, reviews_in = None):
    avg_rating = 0

    reviews = reviews_in or self.get_reviews()
    count = reviews.count()

    if count > 0:
        for review in reviews:
            avg_rating += review.rating
        
        avg_rating /= count
    
    return round(avg_rating,1)

                    # ****************
                    # *** Showings ***
                    # ****************
# Get All Showings                    
def get_showings(self):
    return EventShowing.objects.filter(event=self).all().order_by('time')

# Get Next Showing                            
def get_next_showing(self):
    return self.get_showings().first()

                    # *************
                    # *** Media ***
                    # *************
# Get All Reviews                    
def get_cover_picture(self):
    media = EventMedia.objects.filter(event=self).all()

    if media.count() == 0:
        return None
    else:
        return media[self.primary_media_idx]

# Get All Media                    
def get_media(self):
    return EventMedia.objects.filter(event=self).all()

# Get Media Count                    
def get_media_count(self):
    return get_media().count()

def create_event(data):
    event = Event(
        broadcaster = data['broadcaster'],
        title = data['title'],
        description = data['description'],
        over_18s = data['over_18s'],
        event_id = generate_event_id(),
        #live_price = data['live_price']
    )

    create_ticket_listing(event, TicketType.Streaming, data['stream_price'], None)