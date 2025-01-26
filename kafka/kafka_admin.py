#this admin utiltiy will tell you which is controller broker in the cluster and each broker status 
#like leader, follower, offline, etc.
#it will also tell you the topic details like partition, replication factor, etc.
#it will also tell you the consumer group details like consumer group id, topic, partition, etc.
#it will also tell you the producer details like producer id, topic, partition, etc.

from kafka import KafkaAdminClient
import datetime


bootstrap_servers = 'localhost:9092'
filter_list=['statistic','event','metrics'] #filter the topics

def target_in_filter(target_string):
    not_in_target=True
    for filter_string in filter_list:
        if filter_string in target_string:
            not_in_target=False
            break
    return not_in_target

admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers, cline_id='monitor')
 
print("start fetching lags and monitor cluster: ", datetime.now())
try:
    consumer_groups = admin_client.list_consumer_groups()
    for group in consumer_groups:
        print("consumer group: ", group)
        group_info = admin_client.describe_consumer_group(group)
        print("consumer group info: ", group_info)
        group_state = admin_client.list_consumer_group_offsets(group) ## seems not we are see via win-cli
        print("consumer group state: ", group_state) 

except Exception as e:
    print("Error: ", e)
        
# not sure if kafka admin can be used as CLI which can fetch lags
# another alternative way is to assume you have windows kafka cli and use subprocess to fetch lags 
# then feed to pandas and show each topic lags, even it is not effecient, but it is a way to do it.

# get cluster info and which is main controller
cluster_info = admin_client.describe_cluster()
print("cluster info: ", cluster_info)

# get broker info
broker_info = admin_client.describe_configs()
print("broker info: ", broker_info)

# get topic info
topics = admin_client.list_topics()
for topic in topics:
    if target_in_filter(topic):
        topic_info = admin_client.describe_topics(topic)
        print("topic info: ", topic_info)
        





