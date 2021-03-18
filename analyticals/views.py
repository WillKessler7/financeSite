from django.http import HttpResponse
from django.views import View

class loginView(View):
    def get(self, request):
        return HttpResponse("Login will be here soon...")

class stockPick(View):
    def get(self, request):
        return HttpResponse("You will pick your stocks here...")

class graphDisplay(View):
    def get(self, request):
        return HttpResponse("Graphs will be displayed here...")
