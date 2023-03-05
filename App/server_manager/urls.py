from django.urls import path
from .views import (
    announce,
    heartbeat,
    authenticate,
    streams,

    visualize_srr_tree,
    get_srr_tree
)

urlpatterns = [
    # API's
    path('announce', announce, name='announce'),
    path('heartbeat', heartbeat, name='heartbeat'),
    path('authenticate', authenticate, name='authenticate'),
    path('streams', streams, name='streams'),

    # Data visualization
    path('visualize/srr_tree', visualize_srr_tree, name='visualize_srr_tree'),
    path('get/srr_tree', get_srr_tree, name='get_srr_tree')
]