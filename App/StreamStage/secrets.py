DJANGO_SECRET_KEY = 'django-insecure-69z7g4z57r(g_rd4ott1mca#)^hykt681ig5znx!ra1+7q#9_-'
SENDGIRD_TOKEN = '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'
NODE_ANNOUNCE_KEY = 'DB917464A48CEDE87A22225ED67BEF95A97E45A3A389C9DE5D8A78E779'
CLOUDFLARE_TOKEN = 'WVviIoo2j-eDgSzyno5llaF_EHNqnGp7F9RUP_iD'
STRIPE_PUB_KEY = 'pk_test_51M6y9CHEyDrsSJvelnXxEtxn277Z3hfbVVIk9xK9mHGaRWkL0HFefAf1ng4hHzAaKc11wlq2cfudpiccZzFEL29s00dz15pnGu'
STRIPE_SECRET_KEY = 'sk_test_51M6y9CHEyDrsSJvexuyA5aeupHqHNGzEy2YwSNnUHla9Y3fW0pBUIxkdknMWWoGhYdluWth8UMJyi3kMKdxdRHFO00ZtBDaTqT'

STRIPE_SUBSCRIPTIONS = {
    'SSP': 'price_1Mn8TfKeLSBX93CvYi3x6RLu'
}

STRIPE_MODES = {
    'live': {
        'pub': 'pk_live_51MluK8KeLSBX93CvBxGhDGotysXopqoTvL4E7HYvmi4lrGFId5Ik4N7FvPo65JdrfHghzaLoxEhNhQuIADiCW8uq00BUFyzq9P',
        'pri': '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',
        
        'prices': {
            'SSP': 'price_1Mn8TfKeLSBX93CvYi3x6RLu'
        }
    },

    'test': {
        'pub': 'pk_test_51MluK8KeLSBX93CvBxGhDGotysXopqoTvL4E7HYvmi4lrGFId5Ik4N7FvPo65JdrfHghzaLoxEhNhQuIADiCW8uq00BUFyzq9P',
        'pri': 'sk_test_51MluK8KeLSBX93CvdELL57Uvj6z3vI8Yhk9xw7I35wDDTOhN8vDEdahTnSX8sqADnA9iwDsWKDzI6p4LrmLEsiRQ00JcaN5yQG',

        'prices': {
            'SSP': 'price_1MmcXIKeLSBX93CvwgTOkru0'
        }
    }
}

STRIPE_MODE = 'test'
STRIPE = STRIPE_MODES[STRIPE_MODE]
    
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
    },

    'github': {
        'client_id': '954a843cc41db453bcb6',
        'secret': '528c4b4f3470b94225ba0e5ee4674c3dcfdcb1ac',
        'scopes': [ 'read:user', 'user:email' ],
        'api_url': 'https://github.com/login/oauth/authorize',
        'access_url': 'https://github.com/login/oauth/access_token',
        'userinfo_url': 'https://api.github.com/user',
        'redirect_uri': 'https://me.streamstage.co/sso/github',
        'ttl': 3600
    },

    'discord': {
        'client_id': '1078294558162550864',
        'secret': 'JSckKdMDeyHxqxG2OVfBOiX9QOTwVo4q',
        'scopes': [ 'identify', 'email' ],
        'api_url': 'https://discord.com/api/oauth2/authorize',
        'access_url': 'https://discord.com/api/oauth2/token',
        'userinfo_url': 'https://discord.com/api/users/@me',
        'redirect_uri': 'https://me.streamstage.co/sso/discord',
        'ttl': 3600
    }
}