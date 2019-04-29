from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from pagina_web.views import (
    AboutView,
    HomePageView,
    ApplicationEnrollmentView,
    ListApplicantsView,
    ApplicantDetailsView,
    response_application,
    redirect_home,
    change_password,
    ListFaqCategoryView,
    FrequentlyAskedQuestionsView,
    edit_faq,
    delete_faq,
    AddFAQView,
    UserProfileView
)

urlpatterns = [
    url(r'^$', redirect_home, name="home"),
    url(r'^user/login/$', auth_views.login, name='login'),
    url(r'^user/logout/$', auth_views.logout, {'next_page': 'web_page:login'}, name='logout'),
    url(r'^user/change_password/$', change_password, name='change_password'),
    url(r'^user/profile/$', UserProfileView.as_view(), name="user_profile"),
    url(r'^developers/$', AboutView.as_view(), name="developers_details"),
    url(r'^application/$', ApplicationEnrollmentView.as_view(), name="application_enrollment"),
    url(r'^applicants/$', ListApplicantsView.as_view(), name="list_applicants"),
    url(r'^(?P<pk>.+)/applicant/details/$', ApplicantDetailsView.as_view(), name="applicant_details"),
    url(r'^response/(?P<pk>.+)/(?P<response_id>.+)/$', response_application, name="response_application"),
    url(r'^faq_categories/$', ListFaqCategoryView.as_view(), name="faq_categories"),
    url(r'^(?P<pk>.+)/faq/$', FrequentlyAskedQuestionsView.as_view(), name="frequently_asked_questions"),
    url(r'^(?P<pk>.+)/faq/add/$', AddFAQView.as_view(), name="add_faq"),
    url(r'^(?P<pk>.+)/faq/edit/$', edit_faq, name="edit_faq"),
    url(r'^(?P<pk>.+)/faq/delete/$', delete_faq, name="delete_faq"),
    url(r'^home/$', HomePageView.as_view(), name="home_page"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
