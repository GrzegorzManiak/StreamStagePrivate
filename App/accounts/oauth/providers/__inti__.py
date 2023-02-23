"""
    This module contains all the OAuth providers that are supported by 
    StreamStage

    Google, Github and Discord are currently supported
"""
from .google import Google, GoogleUser
from .github import Github, GithubUser