DJANGO_SECRET_KEY = 'django-insecure-69z7g4z57r(g_rd4ott1mca#)^hykt681ig5znx!ra1+7q#9_-'
SENDGIRD_TOKEN = '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'

# OAUTH
OAUTH_PROVIDERS = {
    'google': {
        'client_id': '701632206335-h3c6bl04mep98c42s2li8ba1icl4pk1s.apps.googleusercontent.com',
        'secret': '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',
        'scopes': {
            'email': 'https://www.googleapis.com/auth/userinfo.email', 
            'profile': 'https://www.googleapis.com/auth/userinfo.profile'
        },
        'userinfo_url': 'https://www.googleapis.com/userinfo/v2/me',
        'redirect_uri': 'https://me.streamstage.co/sso/google',
        'ttl': 3600
    }
}