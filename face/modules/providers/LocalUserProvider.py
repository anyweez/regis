import face.models.models as models

import Provider as provider

def get_users():
    db_users = models.User.objects.all()
    
    users = []
    for db_user in db_users:
        users.append({
            'user_id' : db_user.id,
            'username' : db_user.username,
            'join_date' : db_user.date_joined.isoformat()
        })
    
    return users

def get_user(user_id):
    try:
        return models.User.objects.get(id=user_id)
    except:
        raise provider.ProviderException('A user with an ID of %s does not exist.' % user_id)
