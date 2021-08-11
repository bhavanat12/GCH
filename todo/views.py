from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TodoItem, MapGeometry, CompletedMaps, FinalMaps, ApprovedMap
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from datetime import datetime


@login_required(login_url='login')
def TodoListView(request):
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
		return render(request,'todo/mapAdmin.html',context)

	if request.user.is_superuser:
		Reviews = CompletedMaps.objects.all()
		print(Reviews)
		reviewedMaps = []
		for review in Reviews:
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

		return render(request, 'todo/adminDashboard.html', context)

	# items=TodoItem.objects.all().filter(author=request.user)
	# context = {
	# 	'todoitem': items
	# }

	loggedInUser = request.user
	context["loggedInUser"] = loggedInUser


	return render(request,'todo/userDashboard.html',context)


# @method_decorator(login_required, name='todo.views.TodoCreateView')
class TodoCreateView(LoginRequiredMixin, CreateView):
	login_url='login'
	model = TodoItem
	fields = ['author', 'item']

class TodoUpdateView(UpdateView):
	model = TodoItem
	fields = ['author', 'item']

class TodoDeleteView(DeleteView):
	model = TodoItem
	success_url = '/'

# @login_required(login_url='login')
# def TodoGetView(request):
# 	a = request.GET.get('ID')
# 	a=int(a)
# 	items=TodoItem.objects.all().filter(auto_inc_id=a).first()
# 	context = {
# 		'todoitems': items
# 	}
# 	return render(request,'todo/todo_get.html',context)

@login_required(login_url='login')
def TodoGetAll(request):
	# if request.user.is_superuser:
	# 	items=TodoItem.objects.all()
	# else:
	# 	items=TodoItem.objects.all().filter(author=request.user)


	context = {
		'exists': "False"
	}

	approvedMap = ApprovedMap.objects.all().last()
	# time1 = approvedMap.dateSubmitted

	if MapGeometry.objects.exists():

		try:
			mapdata = MapGeometry.objects.all().get(reviewer=str(request.user))
			# time2 = mapdata.datecreated
			
			# context['todoitems']: items
			
			if mapdata :
				context["geometry"] = mapdata.mapItem
				context["layer"] = mapdata.layer
				context["exists"] = "True"
				context["mapItem"] = approvedMap.mapItem
				context["latestFeaturesExist"] = True
				context["commentData"] = mapdata.comments
				print(mapdata.comments)
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

	return render(request,'todo/map.html',context)

@login_required(login_url='login')
def SubmitMap(request):
	if request.method == 'POST':
		print(request.POST)
		data = request.POST.get('values')
		print(data)
		# Model = apps.get_model('todo', MapGeometry)
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
		print(request.POST)
		data = request.POST.get('values')
		localMapData = MapGeometry.objects.all().get(reviewer=str(request.user))
		commentData = localMapData.comments
		# Model = apps.get_model('todo', MapGeometry)
		user = request.user
		time = datetime.now()
		obj = CompletedMaps.objects.create(reviewer=str(user), mapItem=data, dateSubmitted=time, comments=commentData, status=True)
		obj.save()
	return HttpResponse("Submitted for Review")

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
		print(auto_inc)
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
		return render(request,'todo/mapAdmin.html',context)

@login_required(login_url='login')
def FinalSubmit(request):
	if request.method == 'POST':
		data = request.POST.get('values')
		reviewer = request.POST.get('reviewer')
		# Model = apps.get_model('todo', MapGeometry)
		user = request.user
		time = datetime.now()

		obj = FinalMaps.objects.create(gisUser=user, mapItem=data, dateSubmitted=time, approvalCount=0)
		obj.save()

		
		# if FinalMaps.objects.exists():
		# 	obj = FinalMaps.objects.all().last()
		# 	obj.mapItem = data
		# 	obj.dateSubmitted=time
		# 	obj.save()
		# else:
		# 	obj = FinalMaps.objects.create(gisUser=user, mapItem=data, dateSubmitted=time)
		# 	obj.save()

		CompletedMaps.objects.all().filter(reviewer=reviewer, status="True").update(status = "False")
		
	return HttpResponse("New Version of Map created Successfully!")


@login_required(login_url='login')
def Approval(request):
	if request.method == 'POST':
		obj = FinalMaps.objects.all().last()
		obj.approvalCount = obj.approvalCount + 1
		obj.save()

		return HttpResponse("Approval sent Successfully!")


@login_required(login_url='login')
def SentForApprovalMap(request):
	if request.method == 'POST':
		if FinalMaps.objects.exists():
			obj = FinalMaps.objects.all().last()
			reviewerReadable = obj.reviewerReadable
			if reviewerReadable == "True":
				mapdata = obj.mapItem
				layer = obj.layerURL

				context = {}

				context["latestFeaturesExist"] = "True"
				context["mapItem"] = mapdata
				context["layer"] = layer
				context["Approve"]= True
				context["Comments"] = True


				if MapGeometry.objects.exists():

					try:
						mapdata = MapGeometry.objects.all().get(reviewer=str(request.user))
						# time2 = mapdata.datecreated
						
						context['todoitems']: items
						
						if mapdata :
							context["commentData"] = mapdata.comments
							print(mapdata.comments)
					except MapGeometry.DoesNotExist:
						a = 5

			else: 
				return HttpResponse("Admin is reviewing the map changes, please wait")

		else:
			return HttpResponse("No pending Maps to review")

	return render(request,'todo/map.html',context)


@login_required(login_url='login')
def SaveApprovedVersion(request):
	if request.method == 'POST':
		obj = FinalMaps.objects.all().last()
		layerURL = obj.layerURL
		mapItem = obj.mapItem

		currTime = datetime.now()
		finalObj = ApprovedMap.objects.create(layerURL=layerURL, mapItem=mapItem, dateSubmitted=currTime)
		finalObj.save()

		# entries= FinalMaps.objects.all()
		# entries.delete()

	return HttpResponse("New Revision of the Map created successfully!")


@login_required(login_url='login')
def GetLatestRevision(request):
	if request.method == 'POST':
		obj = ApprovedMap.objects.all().last()
		layerURL = obj.layerURL
		mapItem = obj.mapItem
		latestFeaturesExist = "True"

		context = {
			"layerURL": layerURL,
			"mapItem": mapItem,
			"latestFeaturesExist": latestFeaturesExist,
			"Approve": False
		}

		return render(request, 'todo/map.html',context)


@login_required(login_url='login')
def CommentSubmit(request):
	print(request.method)
	if request.method == 'POST':
		comment = request.POST.get('comment')
		print(comment)

		if MapGeometry.objects.exists():
			try:
				mapdata = MapGeometry.objects.all().get(reviewer=str(request.user))
				# mapdata = MapGeometry.objects.all()[0]
				mapdata.comments = comment
				mapdata.save()

			except MapGeometry.DoesNotExist:
				obj = None

	return redirect('todo-getall')


@login_required(login_url='login')
def Discard(request):
	if request.method == 'POST':
		auto_inc = request.POST.get('auto_inc')
		print(auto_inc)
		CompletedMaps.objects.filter(auto_inc=auto_inc).delete()

		return redirect('todo-home')


@login_required(login_url='login')
def ReviewerReview(request):
	if request.method == 'POST':
		if FinalMaps.objects.exists():
			obj = FinalMaps.objects.all().last()
			obj.reviewerReadable = "True"
			obj.approvalCount = 0
			obj.save()

	return redirect('todo-home')
