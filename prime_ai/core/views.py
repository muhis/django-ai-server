import random
from django.urls import reverse
from django.shortcuts import Http404, HttpResponse, get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sympy import sieve

from core.models import Trial


def get_trial(request):
    """Return a trial index file
    Arguments:
        request {request} -- Django request object.
    """
    layers = generate_layers()
    x_train, y_train = generate_train_dataset()
    x_test, y_test = generate_test_dataset()
    reporting_url = reverse('report_result')
    context = {
        'layers': layers,
        'x_train': x_train,
        'y_train': y_train,
        'x_test': x_test,
        'y_test': y_test,
        'report_url': reporting_url,
    }
    trial = Trial.objects.create(js_payload=context)
    context.update({'uuid': trial.uuid})
    return render(request, 'main.html', context=context)


@csrf_exempt
def report_result(request):
    """Endpoint where the user post back their results

    Arguments:
        request {Django request} -- A request with the result as payload
    """
    if request.method != 'POST':
        raise Http404()
    result = request.POST['result'][11:]
    uuid = request.POST['uuid']
    trial = get_object_or_404(Trial, uuid=uuid)
    trial.result_accuracy_percentage = result
    trial.save()
    return HttpResponse()


def generate_layers():
    """Return experiment payload that a client can execute
    """
    number_of_layers = random.choice(range(1, 10))
    layers = []
    for layer in range(number_of_layers):
        layer_type = random.choice(['dense', 'dropout'])
        layers.append(layer_type)
    return layers


def generate_train_dataset():
    """Generate random dataset for the script
    """
    return generate_dataset((1, 100))


def generate_test_dataset():
    return generate_dataset((100, 200))


def generate_dataset(dataset_range):
    primes = [number for number in sieve.primerange(*dataset_range)]
    x = primes[:-1]
    y = primes[1:]
    return x, y
