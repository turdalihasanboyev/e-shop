from django.shortcuts import render, redirect

from .models import ContactUS


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactUS.objects.create(name=name, email=email, subject=subject, message=message)
            return redirect('contact')
        else:
            return redirect('contact')

    return render(request, 'contact.html')
