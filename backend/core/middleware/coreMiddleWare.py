class CoreMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    host = request.get_host().lower().strip()  # Get the full host (e.g., abc.selfdive.com)
    parts = host.split('.')

    print(host)

    if len(parts) > 2:  # If there's more than the root domain
        request.entity = parts[0]
    else:
        request.entity = None

    return self.get_response(request)
