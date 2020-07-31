from utils import *
import config

# generate list of payloads from csv
events = csv_to_payloads(config.public_key, config.event_mapping,'sample_orders.csv')
profiles = csv_to_payloads(config.public_key, config.profile_mapping,'sample_orders.csv')

# send all events to klaviyo using all cores, and save responses
event_responses = parallelize(send_event_payload, events)

# send all profiles to klaviyo using all cores, and save responses
profile_responses = parallelize(send_profile_payload, profiles)

# filter repsonses above for payloads that should be re-sent
failed_event_payloads = [response for response in event_responses if response != None]
failed_profile_payloads = [response for response in profile_responses if response != None]

# print count of failures
print('# failed event payloads',len(failed_event_payloads))
print('# failed profile payloads',len(failed_profile_payloads))