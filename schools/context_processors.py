from schools.models import Year, Term, FIRST
import datetime

y = datetime.datetime.today()
year = str(y.year) + " / " + str(y.year + 1)

try:
    s = Year.objects.get(is_current_year=True)
except Year.DoesNotExist:
    s = Year.objects.create(year=year, is_current_year=True)
    s.save()

try:
    term = Term.objects.get(is_current_term=True)
except Term.DoesNotExist:
    term = Term.objects.create(term=FIRST, is_current_term=True)
    term.save()


def year_processor(request):
    current_year = Year.objects.get(is_current_year=True)
    return {"current_year": current_year}


def term_processor(request):
    current_term = Term.objects.get(is_current_term=True)
    return {"current_term": current_term}
