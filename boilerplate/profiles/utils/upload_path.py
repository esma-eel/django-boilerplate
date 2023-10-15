def profile_upload(instance, filename):
    return "/".join(["profiles", instance.uuid, filename])
