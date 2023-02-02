DJANGO_SECRET_KEY = 'django-insecure-69z7g4z57r(g_rd4ott1mca#)^hykt681ig5znx!ra1+7q#9_-'
SENDGIRD_TOKEN = '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'

# OAUTH
OAUTH_PROVIDERS = {
    'google': {
        'client_id': '701632206335-5j55b6b730umr3sicjg84h358e4ji6q7.apps.googleusercontent.com',
        'secret': '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',
        'scopes': {
            'email': 'https://www.googleapis.com/auth/userinfo.email', 
            'profile': 'https://www.googleapis.com/auth/userinfo.profile'
        },
        'userinfo_url': 'https://www.googleapis.com/userinfo/v2/me',
        'redirect_uri': 'https://sso.streamstage.co/google',
    }
}