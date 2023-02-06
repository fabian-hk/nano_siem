import os


def template_env_vars(request):
    data = {"INSTANCE_NAME": os.getenv("INSTANCE_NAME", "My Nano SIEM")}
    return data
