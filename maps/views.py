from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import MapGeometry, CompletedMaps, FinalMaps, ApprovedMap
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from datetime import datetime
import requests
from docusign_esign import RecipientViewRequest, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients, ApiClient, EnvelopesApi, Text, DateSigned, CarbonCopy 
from GoodCodeHackathon.settings import CLIENT_AUTH_ID, CLIENT_SECRET_KEY, account_id
from django.urls import reverse
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail

import json
import base64


@login_required(login_url='login')
def DashboardView(request):
	if request.method=='POST':
		Graphdata = request.POST.get('graphDetails')
		reviewer = "abc"
		layer = request.POST.get("layer")
		prevRevision = "True"
		context = {
			'prevRevision': prevRevision,
			'prevGraph': Graphdata,
			'reviewer': reviewer,
			'layer': layer,
			'prevExist':"True",
			"ViewComment":"True"
		}
		return render(request,'maps/mapAdmin.html',context)

	if request.user.is_superuser:
		Reviews = CompletedMaps.objects.all()
		reviewedMaps = []
		for review in Reviews:
			if review.status=="True":
				reviewedMaps.append({"reviewer": review.reviewer, "geometry":review.mapItem, "status":review.status, 
				"dateSubmitted":review.dateSubmitted, "layer": review.layer, "commentData":review.comments, "auto_inc":review.auto_inc})

		context = {
			"reviewedItems" : reviewedMaps
		}

		if FinalMaps.objects.exists():
			prevData = FinalMaps.objects.all().last()
			prevGraph = prevData.mapItem
			prevRevision = "True"
			ApprovalCount = prevData.approvalCount
			context['prevGraph'] = prevGraph
			context["prevRevision"] = prevRevision
			context['ApprovalCount'] = ApprovalCount
			context['layer'] = prevData.layerURL
			context['usersCount'] = User.objects.count() - 1
			if context['usersCount']-context['ApprovalCount']==0:
				context['approveStatus'] = True
			else:
				context['approveStatus'] = False

		else:
			context['ApprovalCount'] = 0
			context['usersCount'] = User.objects.count() - 1

		if ApprovedMap.objects.exists():
			obj = ApprovedMap.objects.all().last()
			context['signCount'] = obj.signedCount

		return render(request, 'maps/adminDashboard.html', context)

	loggedInUser = str(request.user)
	context = {"loggedInUser" : loggedInUser}


	if FinalMaps.objects.exists():
		obj = FinalMaps.objects.all().last()
		approvedBy = json.loads(obj.approvedBy)
		if str(request.user) in approvedBy:
			context["grantAccess"] = False
		else:
			context["grantAccess"] = True

	return render(request,'maps/userDashboard.html',context)



@login_required(login_url='login')
def MyMapView(request):

	context = {
		'exists': "False"
	}

	approvedMap = ApprovedMap.objects.all().last()

	if MapGeometry.objects.exists():

		try:
			mapdata = MapGeometry.objects.all().get(reviewer=str(request.user))
			
			if mapdata :
				context["geometry"] = mapdata.mapItem
				context["layer"] = mapdata.layer
				context["exists"] = "True"
				context["mapItem"] = approvedMap.mapItem
				context["latestFeaturesExist"] = True
				context["commentData"] = mapdata.comments
				
		except MapGeometry.DoesNotExist:
			context["mapItem"] = approvedMap.mapItem
			context["layer"] = approvedMap.layerURL
			context["exists"] = "False"
			context["latestFeaturesExist"] = True
	else:
		context["mapItem"] = approvedMap.mapItem
		context["layer"] = approvedMap.layerURL
		context["exists"] = "False"
		context["latestFeaturesExist"] = True
			
	context["Approve"]= False
	context["Comments"] = True
	context["loggedInUser"] = str(request.user)

	return render(request,'maps/map.html',context)



@login_required(login_url='login')
def SubmitMap(request):
	if request.method == 'POST':
		data = request.POST.get('values')
		# Model = apps.get_model('maps', MapGeometry)
		user = request.user
		time = datetime.now()

		if MapGeometry.objects.exists():
			try:
				mapdata = MapGeometry.objects.all().get(reviewer=str(request.user))
				# mapdata = MapGeometry.objects.all()[0]
				mapdata.datecreated = time
				mapdata.mapItem = data
				mapdata.save()

			except MapGeometry.DoesNotExist:
				obj = MapGeometry.objects.create(reviewer=str(user), mapItem=data, datecreated=time)
				obj.save()

		else:
			obj = MapGeometry.objects.create(reviewer=str(user), mapItem=data, datecreated=time)
			obj.save()

	return HttpResponse("Saved changes to the Map!")



@login_required(login_url='login')
def submitForReview(request):
	if request.method == 'POST':
		data = request.POST.get('values')
		localMapData = MapGeometry.objects.all().get(reviewer=str(request.user))
		commentData = localMapData.comments
		
		user = request.user
		time = datetime.now()
		obj = CompletedMaps.objects.create(reviewer=str(user), mapItem=data, dateSubmitted=time, comments=commentData, status=True)
		obj.save()

	return redirect("dashboard-home")



@login_required(login_url='login')
def AdminGraphView(request):
	if request.method == 'POST':
		Graphdata = request.POST.get('graphDetails')
		reviewer = request.POST.get('Reviewer')
		layer = request.POST.get("layer")
		tempMap = MapGeometry.objects.all().get(reviewer=str(reviewer))
		commentData = tempMap.comments
		prevRevision = "False"
		auto_inc = request.POST.get("auto_inc")
		
		context = {
		    'exists': "True",
			'prevRevision': prevRevision,
			'geometry': Graphdata,
			'reviewer': reviewer,
			'layer': layer,
			"ViewComment":"True",
			"commentData":commentData,
			"auto_inc": auto_inc
		}

		if FinalMaps.objects.exists():
			prevData = FinalMaps.objects.all().last()
			prevGraph = prevData.mapItem
			prevRevision = "True"
			context['prevGraph'] = prevGraph
			context["prevRevision"] = prevRevision

		return render(request,'maps/mapAdmin.html',context)



@login_required(login_url='login')
def FinalSubmit(request):
	if request.method == 'POST':
		data = request.POST.get('values')
		reviewer = request.POST.get('reviewer')
		commentData = request.POST.get('commentData')
		imgData = request.POST.get('imgData')
		
		user = request.user
		time = datetime.now()
		if FinalMaps.objects.exists():
			tmpObj = FinalMaps.objects.all().last()
			if tmpObj.reviewerReadable == "False":
				oldCommentData = json.loads(tmpObj.commentData)
				oldCommentData[str(reviewer)] = commentData
			else:
				oldCommentData = {}
				oldCommentData[str(reviewer)] = commentData
		else:
			oldCommentData = {}
			oldCommentData[str(reviewer)] = commentData
		obj = FinalMaps.objects.create(gisUser=user, mapItem=data, dateSubmitted=time, approvalCount=0, commentData=json.dumps(oldCommentData), imageData=imgData)
		obj.save()

		CompletedMaps.objects.all().filter(reviewer=reviewer, status="True").update(status = "False")
		
	return HttpResponse("New Version of Map created Successfully!")



@login_required(login_url='login')
def Approval(request):
	if request.method == 'POST':
		obj = FinalMaps.objects.all().last()
		obj.approvalCount = obj.approvalCount + 1
		userApprovals = json.loads(obj.approvedBy)
		userApprovals[str(request.user)] = 1
		obj.approvedBy = json.dumps(userApprovals)
		obj.save()

		return redirect("dashboard-home")



@login_required(login_url='login')
def SentForApprovalMap(request):
	context = {"loggedInUser": str(request.user)}
	if request.method == 'POST':
		if FinalMaps.objects.exists():
			obj = FinalMaps.objects.all().last()
			reviewerReadable = obj.reviewerReadable
			if reviewerReadable == "True":
				mapdata = obj.mapItem
				layer = obj.layerURL

				context["latestFeaturesExist"] = "True"
				context["mapItem"] = mapdata
				context["layer"] = layer
				context["Approve"]= True
				context["Comments"] = True

				if MapGeometry.objects.exists():

					try:
						mapdata = MapGeometry.objects.all().get(reviewer=str(request.user))

						if mapdata :
							context["commentData"] = mapdata.comments
							
					except MapGeometry.DoesNotExist:
						a = 5 # dummy variable

			else: 
				context = {"messages":"Admin is reviewing the map changes, please wait"}
				return render(request, 'maps/message.html', context)

		else:
			context = {"messages":"No pending Maps to review"}
			return render(request, 'maps/message.html', context)

	return render(request,'maps/map.html',context)



@login_required(login_url='login')
def SaveApprovedVersion(request):
	if request.method == 'POST':
		obj = FinalMaps.objects.all().last()
		layerURL = obj.layerURL
		mapItem = obj.mapItem

		currTime = datetime.now()
		finalObj = ApprovedMap.objects.create(layerURL=layerURL, mapItem=mapItem, dateSubmitted=currTime)
		finalObj.save()

		obj.reviewerReadable="False"

		revisions = FinalMaps.objects.all().filter(reviewerReadable="True")

		reviewedMaps = []
		counter = 1
		for review in revisions:
			reviewedMaps.append({"imageData": review.imageData, "commentData":json.loads(review.commentData), "counter":counter})
			counter = counter + 1

		context = {
			"reviewedItems" : reviewedMaps
		}

		return render(request, 'maps/mapDisplay.html', context)

	return HttpResponse("New Revision of the Map created successfully!")



@login_required(login_url='login')
def GetLatestRevision(request):
	if request.method == 'POST':
		obj = ApprovedMap.objects.all().last()
		layerURL = obj.layerURL
		mapItem = obj.mapItem
		latestFeaturesExist = "True"
		signedBy = json.loads(obj.signedBy)

		context = {
			"layerURL": layerURL,
			"mapItem": mapItem,
			"latestFeaturesExist": latestFeaturesExist,
			"Approve": False,
			"loggedInUser": str(request.user)
		}

		context["signButton"] = True

		if str(request.user) in signedBy:
			context["grantSignAccess"] = False
		else:
			context["grantSignAccess"] = True

		return render(request, 'maps/map.html',context)



@login_required(login_url='login')
def CommentSubmit(request):
	if request.method == 'POST':
		comment = request.POST.get('comment')

		if MapGeometry.objects.exists():
			try:
				mapdata = MapGeometry.objects.all().get(reviewer=str(request.user))
				mapdata.comments = comment
				mapdata.save()

			except MapGeometry.DoesNotExist:
				obj = None

	return redirect('my-map-view')



@login_required(login_url='login')
def Discard(request):
	if request.method == 'POST':
		auto_inc = request.POST.get('auto_inc')
		CompletedMaps.objects.filter(auto_inc=auto_inc).delete()

		return redirect('dashboard-home')



@login_required(login_url='login')
def ReviewerReview(request):
	if request.method == 'POST':
		if FinalMaps.objects.exists():
			obj = FinalMaps.objects.all().last()
			obj.reviewerReadable = "True"
			obj.approvalCount = 0
			obj.save()

	return redirect('dashboard-home')



@login_required(login_url='login')
def MeetSchedule(request):
	users = User.objects.all()
	userList = []
	for user in users:
		userList.append(user.username)

	context = {'reviewers': userList}

	return render(request, 'maps/meetPage.html', context)



@login_required(login_url='login')
def RecipientDetails(request):
	if request.method == 'POST':
		print(request.POST)
		userEmails = []
		users = User.objects.all()
		for user in users:
			if request.POST.get(str(user)) != None:
				userEmails.append(user.email)
		print(userEmails)
		# meetingdetails = {"topic": "Map Review Discussion: You're invited!",
		#             "type": 2,
		# 			"start_time": "2021-08-29T10: 15:00",
		# 			"timezone": "UTC",
		# 			"duration": "45",
		#             "agenda": "test",
		#             "settings": {"host_video": "true",
		#                         "participant_video": "true",
		#                         "join_before_host": "False",
		#                         "mute_upon_entry": "False",
		#                         "watermark": "true",
		#                         "audio": "voip",
		#                         "auto_recording": "cloud"
		#                         }
		#             }
		# headers = {'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6Imp1Y2FITnlkVDZhVE1keGt2SGdvdGciLCJleHAiOjE2MjkzNTgxOTMsImlhdCI6MTYyODc1MzM5M30.7DCLsRW8eFL4i25N1zulagKhX86HrVTv1MXdfobXn_I',
		#         'content-type': 'application/json'}
		# r = requests.post(f'https://api.zoom.us/v2/users/me/meetings', headers=headers, data=json.dumps(meetingdetails))
		
		# # converting the output into json and extracting the details
		# y = json.loads(r.text)

		# join_URL = y["join_url"]
		# meetingPassword = y["password"]
	
		# subject = 'Map Review Discussion: You\'re invited!'
		# # message = f'\n Here is your zoom meeting link: {join_URL} and your password: "{meetingPassword}"\n'
		# message = f'\n Hi { request.user }, \n\n  Here is your zoom meeting link: and password: \n\n\nThanks,\nThe Jane Goodall Institute'
		# email_from = settings.EMAIL_HOST_USER
		# recipient_list = ["bhavana.t17@iiits.in"]
		# send_mail( subject, message, email_from, recipient_list )
		return redirect('dashboard-home')




def get_access_code(request):
	base_url = "https://account-d.docusign.com/oauth/auth"
	auth_url = "{0}?response_type=code&scope=signature&client_id={1}&redirect_uri={2}".format(base_url,
	CLIENT_AUTH_ID, request.build_absolute_uri(reverse('auth_login')))

	return HttpResponseRedirect(auth_url)



def auth_login(request):
	base_url = "https://account-d.docusign.com/oauth/token"
	auth_code_string = '{0}:{1}'.format(CLIENT_AUTH_ID, CLIENT_SECRET_KEY)
	auth_token = base64.b64encode(auth_code_string.encode())

	req_headers = {"Authorization": "Basic {0}".format(auth_token.decode('utf-8'))}
	post_data = {'grant_type': 'authorization_code', 'code': request.GET.get('code')}

	r = requests.post(base_url, data=post_data, headers=req_headers)
	response = r.json()
	# return HttpResponse(response['access_token'])

	if not 'error' in response:
		return HttpResponseRedirect("{0}?token={1}".format(reverse('get_signing_url'), response['access_token']))

	return HttpResponse(response['error'])



def embedded_signing_ceremony(request):
	signer_email = 'bhavanat1298@gmail.com'
	signer_name = 'Bhavana Talluri'

	with open(r'maps\static\MapDoc.pdf', "rb") as file:
		content_bytes = file.read()
	base64_file_content = base64.b64encode(content_bytes).decode('ascii')

	document = Document(
		document_base64 = base64_file_content,
		name='Example document',
		file_extension = 'pdf',
		document_id=1
	)

	signer = Signer(
		email=signer_email, name=signer_name, recipient_id="1", routing_order="1",
		client_user_id = '2',
	)

	sign_here = SignHere(
		document_id='1', page_number='1', recipient_id='1', tab_label='SignHereTab',
		x_position='470', y_position='50')

	signer.tabs = Tabs(sign_here_tabs=[sign_here])

	envelope_definition = EnvelopeDefinition(
		email_subject="Please sign this document sent from the python SDK",
		documents=[document],
		recipients=Recipients(signers=[signer]),
		status="sent"
	)

	api_client = ApiClient()
	api_client.host = 'https://demo.docusign.net/restapi'
	api_client.set_default_header("Authorization", "Bearer " + request.GET.get('token'))

	envelope_api = EnvelopesApi(api_client)
	results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)

	envelope_id = results.envelope_id
	recipient_view_request = RecipientViewRequest(
		authentication_method='None', client_user_id='2',
		recipient_id='1', return_url=request.build_absolute_uri(reverse('sign_completed')),
		user_name = signer_name, email=signer_email
	)

	results = envelope_api.create_recipient_view(account_id, envelope_id,
	recipient_view_request=recipient_view_request)

	return HttpResponseRedirect(results.url)



def sign_complete(request):
	obj = ApprovedMap.objects.all().last()
	obj.signedCount = obj.signedCount + 1
	userSigner = json.loads(obj.signedBy)
	userSigner[str(request.user)] = 1
	obj.signedBy = json.dumps(userSigner)
	obj.save()

	return redirect('dashboard-home')
