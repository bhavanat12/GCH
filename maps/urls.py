from django.urls import path
from .views import RecipientDetails, MeetSchedule, DashboardView, MyMapView, SubmitMap, submitForReview,AdminGraphView, FinalSubmit, Approval, SentForApprovalMap, SaveApprovedVersion, GetLatestRevision, CommentSubmit, Discard, ReviewerReview, embedded_signing_ceremony, get_access_code, auth_login, sign_complete
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', DashboardView, name='dashboard-home'),
    path('MyMapView/', MyMapView, name='my-map-view'),
    path('submitMap/', SubmitMap),
    path('submitForReview/', submitForReview, name='submit-review'),
    path('AdminMapView/', AdminGraphView, name='admin-graph-view'),
    path('FinalSubmit/', FinalSubmit),
    path('approve/', Approval, name='user-approve'),
    path('ApprovedMap/', SentForApprovalMap, name='approved-map'),
    path('SaveRevision/', SaveApprovedVersion, name='approved-revision'),
    path('GetLatestRevision/', GetLatestRevision, name='latest-revision'),
    path('CommentSubmit/', CommentSubmit, name='comment-submit'),
    path('Discard/', Discard, name='discard'),
    path('reviewerReview/', ReviewerReview, name='reviewer-review'),
    path('meetSchedule/', MeetSchedule, name='meet-schedule'),
    path('recipients/', RecipientDetails, name='recipients'),
    url(r'^get_signing_url/$', embedded_signing_ceremony, name='get_signing_url'),
    url(r'^get_access_code/$', get_access_code, name='get_access_code'),
    url(r'^auth_login/$', auth_login, name='auth_login'),
    url(r'^sign_completed/$', sign_complete, name='sign_completed'),
]
