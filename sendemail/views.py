from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView

from .forms import ContactForm


class SuccessView(TemplateView):
    template_name = "contact/thankyou.html"


class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact/contact.html"

    def get_success_url(self):
        return reverse("success")  # Redirect to the success page

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        full_message = f"""
            Received message below from 
            Email - {email}, 
            Subject - {subject}
            ________________________
            Message - {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super().form_valid(form)  # Call the parent class method to handle form validation
