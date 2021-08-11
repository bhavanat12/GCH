from django.urls import path
from .views import TodoListView, TodoCreateView, TodoUpdateView, TodoDeleteView, TodoGetAll, SubmitMap, submitForReview,AdminGraphView, FinalSubmit, Approval, SentForApprovalMap, SaveApprovedVersion, GetLatestRevision, CommentSubmit, Discard, ReviewerReview

urlpatterns = [
    path('', TodoListView, name='todo-home'),
    path('new/', TodoCreateView.as_view(), name='todo-create'),
    path('todo_get/<int:pk>/update', TodoUpdateView.as_view(), name='todo-update'),
    path('todo_get/<int:pk>/delete', TodoDeleteView.as_view(), name='todo-delete'),
    path('todo_getall/', TodoGetAll, name='todo-getall'),
    path('submitMap/', SubmitMap),
    path('submitForReview/', submitForReview),
    path('AdminMapView/', AdminGraphView, name='admin-graph-view'),
    path('FinalSubmit/', FinalSubmit),
    path('approve/', Approval, name='user-approve'),
    path('ApprovedMap/', SentForApprovalMap, name='approved-map'),
    path('SaveRevision/', SaveApprovedVersion, name='approved-revision'),
    path('GetLatestRevision/', GetLatestRevision, name='latest-revision'),
    path('CommentSubmit/', CommentSubmit, name='comment-submit'),
    path('Discard/', Discard, name='discard'),
    path('reviewerReview/', ReviewerReview, name='reviewer-review')
]