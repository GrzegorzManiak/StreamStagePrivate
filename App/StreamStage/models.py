from django.db import models
import uuid
import time
import datetime

MINUTE = 60
HOUR = 3600
DAY = 86400
WEEK = 604800
MONTH = 2592000
YEAR = 31536000

class SentEmail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email_id = models.UUIDField(default=uuid.uuid4, editable=False)
    member_id = models.UUIDField(null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Statistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    statistic = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    value = models.IntegerField()
    created = models.IntegerField(default=time.time())

    def log(
        group: str, 
        statistic: str, 
        value: int = 1
    ):  
        """
            Logs a statistic
        """
        stat = Statistics(
            statistic=statistic,
            group=group,
            value=value
        )
        stat.save()



    def build_statistic(
        group: str, 
        statistic: str,
        time_frame: [int, int],
        frame_type: str = 'minute'
    ):
        """
            Builds a statistic dict between the two times
            format: {
                'lables': [ '1', '2', '3' ],
                'data': [ 1, 2, 3 ]
            }
        """
        time_frame = [ int(time_frame[0]), int(time_frame[1]) ]

        # -- Get the statistics
        stats = Statistics.objects.filter(
            group=group,
            statistic=statistic,
            created__gte=get_time(frame_type, time_frame[0]),
            created__lte=get_time(frame_type, time_frame[1])
        ).order_by('created')


        # -- Start building the data
        data = {
            'labels': [],
            'data': []
        }

        # -- Create the labels and data
        dif = (time_frame[0] - time_frame[1])
        for i in range(dif):
            data['labels'].append(generate_lable(time_frame, frame_type, i))

            # -- Get the data
            stat = stats.filter( 
                created__gte=get_time(frame_type, time_frame[0] - i),
                created__lte=get_time(frame_type, time_frame[1] + i)
            )

            # -- Add the data
            data['data'].append(stat.count())

        data['labels'].reverse()
        data['data'].reverse()

        return data



def get_time(
    frame_type: str = 'minute',
    frame: int = 1,
) -> int:
    current_time = int(time.time())
    frame = int(frame)

    match frame_type:
        case 'minute': return current_time - int(frame * MINUTE)
        case 'hour': return current_time - int(frame * HOUR)
        case 'day': return current_time - int(frame * DAY)
        case 'week': return current_time - int(frame * WEEK)
        case 'month': return current_time - int(frame * MONTH)
        case 'year': return current_time - int(frame * YEAR)
        case _: raise Exception('Invalid frame')



def generate_lable(
    time_frame: [int, int],
    frame_type: str,
    frame: int,
) -> str:
    match frame_type:
        case 'minute': return f'{frame}m'
        case 'hour': return f'{frame}h' if frame > 9 else f'0{frame}:00h'
        case 'day': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%a')
        case 'week': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b %d')
        case 'month': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b')
        case 'year': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b %d')