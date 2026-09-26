from .models import WhatsappMessage


def whatsapp_unread(request):
    """
    Makes the unread WhatsApp count available in every template (used for the
    sidebar badge). Counts distinct customer phone numbers with at least one
    unread incoming message, not total unread messages.
    """
    if not request.path.startswith("/admin/"):
        count = (
            WhatsappMessage.objects.filter(direction="in", is_read=False)
            .values("phone")
            .distinct()
            .count()
        )
    else:
        count = 0

    return {"whatsapp_unread_count": count}