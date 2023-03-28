from typing import Union
from django.db import models
import psutil
import uuid
import time
import datetime

SECOND = 10
MINUTE = 60
HOUR = 3600
DAY = 86400
WEEK = 604800
MONTH = 2592000
YEAR = 31536000

network_tx = []
network_rx = []
cpu_usage = []
memory_usage = []

kb = float(1024)
mb = float(kb ** 2)
gb = float(kb ** 3)

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
        time_frame: Union[int, int],
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
        data = { 'labels': [], 'data': [] }

        # -- Create the labels and data
        dif = (time_frame[0] - time_frame[1])
        for i in range(dif):
            data['labels'].append(generate_lable(time_frame, frame_type, i))

        # -- Get the statistics (not system)
        if group == 'system':
            global network_rx
            global network_tx
            global cpu_usage
            global memory_usage

            match statistic:
                case 'cpu_usage': stats = cpu_usage
                case 'memory_usage': stats = memory_usage
                case 'network_tx': stats = network_tx
                case 'network_rx': stats = network_rx
                
            # -- Process the statistics
            for i in range(dif):
                # -- Add the data 
                more_than = get_time(frame_type, time_frame[0] - i)
                less_than = get_time(frame_type, (time_frame[0] - i) - 1)
                values = []

                for stat in stats: 
                    if (
                        stat['created'] > more_than and
                        stat['created'] < less_than 
                    ): values.append(stat['value'])

                if len(values) <= 0: data['data'].append(0.0)
                else: data['data'].append(sum(values) / len(values))

            # -- Interpolate the values
            for i, n in enumerate(data['data']):
                if n > 0.5: continue
                elif i == 0: data['data'][i] = data['data'][1]
                elif i == len(data['data'])-1: data['data'][i] = data['data'][i-1]
                else: data['data'][i] = (data['data'][i-1] + data['data'][i+1]) / 2

        else: 
            stats = Statistics.objects.filter(
                group=group,
                statistic=statistic,
                created__gte=get_time(frame_type, time_frame[0]),
                created__lte=get_time(frame_type, time_frame[1])
            ).order_by('created')


            for i in range(dif):
                # -- Get the data
                stat = stats.filter( 
                    created__gte=get_time(frame_type, time_frame[0] - i),
                    created__lte=get_time(frame_type, (time_frame[0] - i) - 1)
                )

                # -- Add the data
                data['data'].append(stat.count())



        data['labels'].reverse()
        return data



def get_time(
    frame_type: str = 'minute',
    frame: int = 1,
) -> int:
    current_time = int(time.time())
    frame = int(frame)

    match frame_type:
        case 'seconds': return current_time - int(frame * SECOND)
        case 'minute': return current_time - int(frame * MINUTE)
        case 'hour': return current_time - int(frame * HOUR)
        case 'day': return current_time - int(frame * DAY)
        case 'week': return current_time - int(frame * WEEK)
        case 'month': return current_time - int(frame * MONTH)
        case 'year': return current_time - int(frame * YEAR)
        case _: raise Exception('Invalid frame')



def generate_lable(
    time_frame: Union[int, int],
    frame_type: str,
    frame: int,
) -> str:
    match frame_type:
        case 'seconds': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%M:%S')
        case 'minute': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%H:%M')
        case 'hour': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%H:%M')
        case 'day': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%a')
        case 'week': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b %d')
        case 'month': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b')
        case 'year': return datetime.datetime.fromtimestamp(get_time(frame_type, frame)).strftime('%b %d')


def get_network_usage():
    """
    Returns the network traffic in bytes per second for the past second.
    """
    net_io_counters1 = psutil.net_io_counters()
    time.sleep(1)
    net_io_counters2 = psutil.net_io_counters()
    
    bytes_sent = net_io_counters2.bytes_sent - net_io_counters1.bytes_sent
    bytes_recv = net_io_counters2.bytes_recv - net_io_counters1.bytes_recv
    
    bytes_sent_per_sec = bytes_sent / 1
    bytes_recv_per_sec = bytes_recv / 1
    
    # Make sure that the values are a bit more than 0
    if bytes_sent_per_sec < 1: bytes_sent_per_sec = 1
    if bytes_recv_per_sec < 1: bytes_recv_per_sec = 1

    # Round the values to 2 decimal places
    bytes_sent_per_sec = round(bytes_sent_per_sec, 2)
    bytes_recv_per_sec = round(bytes_recv_per_sec, 2)

    return (bytes_sent_per_sec, bytes_recv_per_sec)




def get_cpu_usage():
    """
    Returns the CPU usage in percentage for the past second.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage



def get_memory_usage():
    """
    Returns the memory usage in percentage for the past second.
    """
    memory_usage = psutil.virtual_memory().percent
    return memory_usage



def log_stats(
    network_rx,
    network_tx,
    cpu_usage,
    memory_usage
):
    """
    Logs the statistics
    """

    # -- Get the stats
    network_usage = get_network_usage()

    # -- Log the stats
    network_rx.append({
        'created': time.time(),
        'value': network_usage[1]
    })
    network_tx.append({
        'created': time.time(),
        'value': network_usage[0]
    })
    cpu_usage.append({
        'created': time.time(),
        'value': get_cpu_usage()
    })
    memory_usage.append({
        'created': time.time(),
        'value': get_memory_usage()
    })

    # Crimp the data to 1000 points
    network_rx = network_rx[-1000:]
    network_tx = network_tx[-1000:]
    cpu_usage = cpu_usage[-1000:]
    memory_usage = memory_usage[-1000:]

    return [
        network_rx,
        network_tx,
        cpu_usage,
        memory_usage
    ]


# -- Start the background proccess
from threading import Thread

def log_thread():
    global network_rx
    global network_tx
    global cpu_usage
    global memory_usage

    while True:
        [ network_rx, network_tx, cpu_usage, memory_usage ] = log_stats(
            network_rx, network_tx, cpu_usage, memory_usage)
        time.sleep(SECOND)

thread = Thread(daemon=True, target=log_thread, name='log_thread')
thread.start()