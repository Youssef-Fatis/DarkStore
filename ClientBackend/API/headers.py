loginHeaders = {
    'Content-Type': 'application/json',  # Set Content-Type to application/json
 }
def authHeader(accessToken):
    ordersHeaders = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessToken}',  # Use the token
    }
    return ordersHeaders