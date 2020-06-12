from django.shortcuts import render


def index(request):
    return render(request, "index.html", {})


def home(request):
    return render(request, "home.html", {})


def about(request):
    return render(request, "about.html", {})


def aboutUs(request):
    return render(request, "aboutUs.html", {})


def research(request):
    return render(request, "research.html", {})


def aboutUs(request):
    return render(request, "aboutUs.html", {})


def blog(request):
    return render(request, "blog.html", {})


def contact(request):
    return render(request, "contact.html", {})


def elements(request):
    return render(request, "elements.html", {})


def portfolio(request):
    return render(request, "portfolio.html", {})


def services(request):
    return render(request, "services.html", {})
