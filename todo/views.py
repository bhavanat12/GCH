from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TodoItem, MapGeometry, CompletedMaps, FinalMaps, ApprovedMap
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from datetime import datetime

# class TodoListView(ListView):
# 	model = TodoItem
# 	template_name = 'todo/home.html'
# 	context_object_name = 'todoitem'
# 	ordering = ['auto_inc_id']

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
			'prevExist':"True"
		}
		return render(request,'todo/mapAdmin.html',context)

	if request.user.is_superuser:
		Reviews = CompletedMaps.objects.all()
		print(Reviews)
		reviewedMaps = []
		for review in Reviews:
			reviewedMaps.append({"reviewer": review.reviewer, "geometry":review.mapItem, "status":review.status, 
			"dateSubmitted":review.dateSubmitted, "layer": review.layer})

		context = {
			"reviewedItems" : reviewedMaps
		}

		if FinalMaps.objects.exists():
			prevData = FinalMaps.objects.all()[0]
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
	

		return render(request, 'todo/adminDashboard.html', context)

	items=TodoItem.objects.all().filter(author=request.user)
	context = {
		'todoitem': items
	}

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

@login_required(login_url='login')
def TodoGetView(request):
	a = request.GET.get('ID')
	a=int(a)
	items=TodoItem.objects.all().filter(auto_inc_id=a).first()
	context = {
		'todoitems': items
	}
	return render(request,'todo/todo_get.html',context)

@login_required(login_url='login')
def TodoGetAll(request):
	if request.user.is_superuser:
		items=TodoItem.objects.all()
	else:
		items=TodoItem.objects.all().filter(author=request.user)


	context = {
		'exists': "False"
	}

	approvedMap = ApprovedMap.objects.all().last()
	# time1 = approvedMap.dateSubmitted

	if MapGeometry.objects.exists():

		try:
			mapdata = MapGeometry.objects.all().get(reviewer=str(request.user))
			# time2 = mapdata.datecreated
			
			context['todoitems']: items
			
			if mapdata :
				context["geometry"] = mapdata.mapItem
				context["layer"] = mapdata.layer
				context["exists"] = "True"
				context["mapItem"] = approvedMap.mapItem
				context["latestFeaturesExist"] = True
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

	return HttpResponse("Saved changes to the Map!")

@login_required(login_url='login')
def submitForReview(request):
	if request.method == 'POST':
		print(request.POST)
		data = request.POST.get('values')
		print(data)
		# Model = apps.get_model('todo', MapGeometry)
		user = request.user
		time = datetime.now()
		print("**")
		obj = CompletedMaps.objects.create(reviewer=str(user), mapItem=data, dateSubmitted=time, status=True)
		obj.save()
	return HttpResponse("Submitted for Review")

@login_required(login_url='login')
def AdminGraphView(request):
	if request.method == 'POST':
		Graphdata = request.POST.get('graphDetails')
		reviewer = request.POST.get('Reviewer')
		layer = request.POST.get("layer")
		prevRevision = "False"
		context = {
		    'exists': "True",
			'prevRevision': prevRevision,
			'geometry': Graphdata,
			'reviewer': reviewer,
			'layer': layer
		}
		if FinalMaps.objects.exists():
			prevData = FinalMaps.objects.all()[0]
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
		
		if FinalMaps.objects.exists():
			obj = FinalMaps.objects.all()[0]
			obj.mapItem = data
			obj.dateSubmitted=time
			obj.save()
		else:
			obj = FinalMaps.objects.create(gisUser=user, mapItem=data, dateSubmitted=time)
			obj.save()

		CompletedMaps.objects.all().filter(reviewer=reviewer, status="True").update(status = "False")
		
	return HttpResponse("New Version of Map created Successfully!")



def Approval(request):
	if request.method == 'POST':
		obj = FinalMaps.objects.all()[0]
		obj.approvalCount = obj.approvalCount + 1
		obj.save()

		return HttpResponse("Approval sent Successfully!")


def SentForApprovalMap(request):
	if request.method == 'POST':
		if FinalMaps.objects.exists():
			obj = FinalMaps.objects.all()[0]
			mapdata = obj.mapItem
			layer = obj.layerURL

			context = {}

			context["exists"] = "True"
			context["geometry"] = mapdata
			context["layer"] = layer
			context["Approve"]= True
		else:
			return HttpResponse("No pending Maps to review")

	return render(request,'todo/map.html',context)


def SaveApprovedVersion(request):
	if request.method == 'POST':
		obj = FinalMaps.objects.all()[0]
		layerURL = obj.layerURL
		mapItem = obj.mapItem

		currTime = datetime.now()
		finalObj = ApprovedMap.objects.create(layerURL=layerURL, mapItem=mapItem, dateSubmitted=currTime)
		finalObj.save()

		entries= FinalMaps.objects.all()
		entries.delete()

	return HttpResponse("New Revision of the Map created successfully!")


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