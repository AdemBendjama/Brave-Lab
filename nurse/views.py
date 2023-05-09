from django.shortcuts import render
from django.contrib.auth.decorators import login_required , permission_required

# Create your views here.

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def nurse_home(request):
    
    return render(request,'nurse/nurse.html')