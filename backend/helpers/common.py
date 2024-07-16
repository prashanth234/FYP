from django.utils import timezone
import zoneinfo

def get_today_date(include_time=False):
  kolkata_timezone = zoneinfo.ZoneInfo('Asia/Kolkata')
  current_time_in_kolkata = timezone.now().astimezone(kolkata_timezone)
  return (current_time_in_kolkata if include_time else current_time_in_kolkata.date())