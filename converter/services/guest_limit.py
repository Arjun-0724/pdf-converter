from datetime import date


def can_convert(request):
    """
    Returns:
    (allowed, remaining)
    """

    if request.user.is_authenticated:
        return True, None

    today = str(date.today())

    session_date = request.session.get("conversion_date")
    count = request.session.get("conversion_count", 0)

    if session_date != today:
        request.session["conversion_date"] = today
        request.session["conversion_count"] = 0
        count = 0

    remaining = 3 - count

    return count < 3, remaining




def increment_conversion(request):
    if request.user.is_authenticated:
        return

    count = request.session.get(
        "conversion_count",
        0
    )

    request.session["conversion_count"] = count + 1