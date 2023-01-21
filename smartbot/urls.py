from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework import routers


from .views import *
from profiles.views import *
from blog.views import *
from django.conf.urls.static import static
from .settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt
from .socialLogin import TokenLoginConfirm


router = routers.DefaultRouter()

router.register(r'account', ProfileMiniViewSet, basename='Profile')
router.register(r'accountSummary', ProfileEditViewSet, basename='Profile')
router.register(r'chatbots', ChatbotMiniViewset, basename="mybots")

router.register(r'chatbotsDashboard',
                ChatbotAnalyticalViewset, basename="mybots")
router.register(r'chatbotsEdit/(?P<id>.*)',
                ChatbotEditViewset, basename="editBot")
router.register(r'chatbotsDelete/(?P<id>.*)',
                chatbotDeleteViewset, basename="editBot")
router.register(r'chatbotHost/(?P<id>.*)',
                chatbotHostViewset, basename='chatbotHost')


router.register(r'helpdeskTickets', HelpdeskTicketViewset,
                basename='HelpdeskTicket')


router.register(r'blogs',     BlogViewset, basename='Blog')
router.register(r'blog',     BlogPostViewset, basename='BlogPost')


urlpatterns = [
    path('', RedirectToFrontEnd, name="redirectToFrontend"),
    path('api-info/', include(router.urls)),


    # Profile URLs
    path('auth/login/', csrf_exempt(ObtainAuthToken.as_view())),
    path('auth/logout/', Logout.as_view()),
    path('api-info/register/', RegisterUserView.as_view()),
    path('api-info/updateProfile/', ProfileUpdateUserVew.as_view()),
    path('api-info/validateToken/', ValidateToken.as_view()),
    path('api-info/saveChatbot/',  ChatbotUpdate.as_view()),
    path('api-info/logSession/',     logSession.as_view()),
    path('api-info/saveHelpdeskTicket/',     OpenHelpdeskTicket.as_view()),
    path('api-info/sendEmail/',     sendEmail.as_view()),
    path('api-info/sentimentAnalysis/',     SentimentAnalysis.as_view()),

    path('api-info/autoRespond/',    AutoRespond.as_view()),




    # Google Signin URLs
    path('accounts/login/', RedirectToFrontEnd, name='google_login'),
    path('accounts/signup/', RedirectToFrontEnd, name='google_login'),
    path('accounts/', include('allauth.urls')),
    path('login/confirmed/google/', TokenLoginConfirm, name='github_login'),
    path('activate/<uid>/<token>/', ActivateAccount, name='activate'),
    path('google26a07d368bac3722.html', googleVerification),

    path('tinymce/', include('tinymce.urls')),

    # Admin URLs
    path('admin/', admin.site.urls),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
