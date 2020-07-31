# Klaviyo account
public_key = 'abc123'

# event example
# edit this to conform to your data, or delete 
event_mapping = {
    'event':'PlacedOrder',
    'customer_properties':{
        '$email':'EMAIL',
    },
    'properties':{
        '$event_id':'ORDER_ID',
        '$value':'ORDER_TOTAL',
        'OrderType':'ORDER_TYPE',
        'CouponCode':'COUPON_CODE'
    },
    'time':'DATE_ORDERED'
}

# profile property example
# edit this to conform to your data, or delete 
profile_mapping = {
    'properties': {
        '$email':'EMAIL',
        '$first_name':'BILL_FIRST_NAME',
        '$last_name':'BILL_LAST_NAME',
        '$region':'BILL_STATE_CODE',
        '$zip':'BILL_ZIP',
        '$phone_number' : 'BILL_PHONE',
    }
}
