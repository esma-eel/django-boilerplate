from rest_framework_simplejwt.views import TokenBlacklistView


class JWTTokenBlacklistView(TokenBlacklistView):
    _serializer_class = (
        "boilerplate.authentication.api.blacklist.serializers"
        ".JWTTokenBlacklistSerializer"
    )


class SlidingTokenBlacklistView(TokenBlacklistView):
    _serializer_class = (
        "boilerplate.authentication.api.blacklist.serializers"
        ".SlidingTokenBlacklistSerializer"
    )
