from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    GenreViewSet,
    PackViewSet,
    PurchaseViewSet,
    SoundViewSet,
    SubTypeViewSet,
    GetSubscriptionView,
    TransactionViewSet,
    TypeViewSet,
    UserViewSet,
    SearchView,
    LoginViewSet,
    SignupViewSet,
    CookieTokenRefreshView,
    GoogleAuthCallbackView,
    redirect_to_google_login,
    TwitterAuthCallbackView,
    redirect_to_twitter_login,
    UploadPackPreviewView,
    LogoutViewSet,
    UploadPackViewset,
    CreateCheckoutSessionView,
    stripe_webhook,
    RetrieveCheckoutSessionView,
    CancelSubscriptionView,
    ConfirmEmailView,
    SubscriptionViewSet,
    NewsletterSubscriptionView,
    AccountReactivationSendMailViewSet,
    ReactivateAccountLinkView,
    FavoriteViewSet,
    BuySongView,
    BuyPackView,
    PortalSessionCreate,
)


router = SimpleRouter()
router.register("genre", GenreViewSet, basename="genre")
router.register("pack", PackViewSet, basename="pack")
router.register("purchase", PurchaseViewSet, basename="purchase")
router.register("sound", SoundViewSet, basename="sound")
router.register("subtype", SubTypeViewSet, basename="subtype")
router.register("transaction", TransactionViewSet, basename="transaction")
router.register("type", TypeViewSet, basename="type")
router.register("user", UserViewSet, basename="user")
router.register("auth/login", LoginViewSet, basename="auth/login")
router.register("auth/signup", SignupViewSet, basename="auth/signup")
router.register("auth/logout", LogoutViewSet, basename="auth/logout")
router.register("upload_pack", UploadPackViewset, basename="upload_pack")
router.register("newsletter", NewsletterSubscriptionView, basename="newsletter")
router.register(
    "reactivate-request",
    AccountReactivationSendMailViewSet,
    basename="reactivation-request",
)
router.register("favorites", FavoriteViewSet, basename="favorites")
urlpatterns = [
    path("", include(router.urls)),
    path("search/", SearchView.as_view(), name="search"),
    path(
        "token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh_cookie"
    ),
    path(
        "auth/google/callback/",
        GoogleAuthCallbackView.as_view(),
        name="google-auth-callback",
    ),
    path("google/login/", redirect_to_google_login, name="google-login"),
    path(
        "auth/twitter/callback/",
        TwitterAuthCallbackView.as_view(),
        name="twitter-auth-callback",
    ),
    path("twitter/login/", redirect_to_twitter_login, name="twitter-login"),
    path("preview_upload/", UploadPackPreviewView.as_view(), name="preview_upload"),
    path(
        "create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
    path(
        "checkout-session/<str:session_id>/",
        RetrieveCheckoutSessionView.as_view(),
        name="retrieve-checkout-session",
    ),
    path(
        "cancel-subscription/",
        CancelSubscriptionView.as_view(),
        name="cancel-subscription",
    ),
    path(
        "auth/confirm-email/<str:key>/",
        ConfirmEmailView.as_view(),
        name="auth_confirm_email",
    ),
    path(
        "reactivate/<uuid:token>/",
        ReactivateAccountLinkView.as_view(),
        name="reactivate-account",
    ),
    path("buy/song/", BuySongView.as_view(), name="buy_song"),
    path("buy/pack/", BuyPackView.as_view(), name="buy_pack"),
    path("stripe-portal-session/", PortalSessionCreate.as_view(), name="buy_pack"),
    path("subscription/", GetSubscriptionView.as_view(), name="subscription"),
]
