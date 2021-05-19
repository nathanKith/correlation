from django.shortcuts import render
from app.forms import TickerForm
from app.models import correleation

def main(request):
    if request.method == 'POST':
        form = TickerForm(data=request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            try:
                results = correleation(clean_data['ticker1'], clean_data['ticker2'])
                
                return render(request, 'index.html', {
                    'answers': results,
                })
            except:
                return render(request, 'index.html', {
                    'answers': ['Произошли некоторые проблемы'],
                })
        
        return render(request, 'index.html', {
            'answers': [''],
        })

    return render(request, 'index.html', {
        'answers': [''],
    })
