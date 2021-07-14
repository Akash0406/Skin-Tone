from datetime import date
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from datetime import datetime
from .models import Contact, UserImageDb
from .camera import VideoCamera
from django.http.response import StreamingHttpResponse

# Create your views here.

def Home(request):
    return render(request, 'index.html')


def upload(request):
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('result')   
    else:
        form = UploadForm()           
    return render(request, 'upload.html', {'form' : form})

def video(request):
	return render(request,'video.html')

def image(request):
	return render(request,'image.html')

def success(request):
    return HttpResponse('Successfully Uploaded')    

def ThankYou(request):
    return render(request, 'thankyou.html')


def capture(request):
    return render(request, 'captureimage.html')    


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phoneNumber = request.POST.get('phoneNumber')

        contact = Contact(name=name, email=email, phoneNumber = phoneNumber, date = datetime.today() )
        contact.save()
                
    return render(request, 'contact.html')    


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def result(request):
    form = UserImageDb.objects.latest('name')

    result = "mild"
    return render(request, 'result.html', {'form': form, 'result': result})                  