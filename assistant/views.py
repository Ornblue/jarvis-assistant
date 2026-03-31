from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import uuid
import os
from django.conf import settings
from .models import Memory, Task, ChatHistory


def preprocess_math(command):
    command = command.replace("square", "^2")
    command = command.replace("cube", "^3")
    command = command.replace("plus", "+")
    command = command.replace("minus", "-")
    command = command.replace("into", "*")
    command = command.replace("multiply", "*")
    command = command.replace("divided by", "/")
    command = command.replace("by", "/")
    return command

def home(request):
    return render(request, 'index.html')



@csrf_exempt
def process_command(request):
    if request.method == "POST":
        import json, datetime, sympy as sp, numpy as np, matplotlib.pyplot as plt, uuid, os
        from django.conf import settings
        from .models import Memory, Task, ChatHistory

        data = json.loads(request.body)
        command = data.get('command', '').lower()

        response = ""
        action = None
        query = ""
        graph_url = ""
        steps = ""

        x = sp.symbols('x')

        def clean_expr(expr):
            expr = expr.replace("square", "^2").replace("cube", "^3")
            expr = expr.replace("^", "**")
            expr = expr.replace("plus", "+").replace("minus", "-")
            expr = expr.replace("into", "*").replace("multiply", "*")
            expr = expr.replace("divided by", "/")
            return expr.strip()

        try:
            if "my name is" in command:
                name = command.replace("my name is", "").strip()
                Memory.objects.create(key="name", value=name)
                return JsonResponse({"response": f"Nice to meet you {name}"})

            if "what is my name" in command:
                mem = Memory.objects.filter(key="name").last()
                return JsonResponse({"response": f"Your name is {mem.value}" if mem else "I don't know your name yet"})

            if "remind me" in command:
                Task.objects.create(title=command)
                return JsonResponse({"response": "Reminder saved"})

            if "show tasks" in command:
                tasks = Task.objects.all()
                return JsonResponse({"response": str([t.title for t in tasks])})

            if any(op in command for op in ['+', '-', '*', '/', '%']):
                expr = clean_expr(command)
                result = sp.sympify(expr)

                try:
                    if result.is_Number:
                        if result.is_Integer:
                            response = f"Answer is {int(result)}"
                        else:
                            decimal = round(float(result.evalf()), 4)
                            response = f"Answer is {result} = {decimal}"
                    else:
                        response = f"Answer is {result}"
                except:
                    response = f"Answer is {result}"

                return JsonResponse({"response": response})

            if "derivative" in command:
                expr = command.replace("derivative of", "")
                expr = expr.split("with respect to")[0]
                expr = expr.split("=")[0]
                expr = clean_expr(expr)

                result = sp.diff(sp.sympify(expr), x)
                steps = f"d/dx({expr}) = {result}"
                return JsonResponse({"response": f"Derivative is {result}", "steps": steps})

            if "integral" in command or "integrate" in command:
                expr = command.replace("integral", "").replace("integrate", "")
                expr = expr.split("with respect to")[0]
                expr = clean_expr(expr)

                result = sp.integrate(sp.sympify(expr), x)
                steps = f"∫({expr}) dx = {result}"
                return JsonResponse({"response": f"Integral is {result}", "steps": steps})

            if "sin" in command or "cos" in command or "tan" in command:
                expr = clean_expr(command)
                result = sp.N(sp.sympify(expr))
                return JsonResponse({"response": f"Result is {result}"})

            if "log" in command:
                val = float(command.replace("log", "").strip())
                result = sp.log(val)
                return JsonResponse({"response": f"Log value is {result}"})

            if "plot" in command or "graph" in command:
                expr = command.replace("plot", "").replace("graph", "")
                expr = clean_expr(expr)

                sym = sp.sympify(expr)
                f = sp.lambdify(x, sym, "numpy")

                xs = np.linspace(-10, 10, 200)
                ys = f(xs)

                filename = f"{uuid.uuid4().hex}.png"
                path = os.path.join(settings.BASE_DIR, "static", filename)

                plt.figure()
                plt.plot(xs, ys)
                plt.grid()
                plt.savefig(path)
                plt.close()

                graph_url = f"/static/{filename}"
                return JsonResponse({"response": "Here is the graph", "graph": graph_url})

            if "play" in command:
                query = command.replace("play", "").strip()
                return JsonResponse({
                    "response": f"Playing {query}",
                    "action": "youtube_play",
                    "query": query
                })

            if "spotify" in command:
                return JsonResponse({
                    "response": "Opening Spotify",
                    "action": "spotify"
                })

            if "news" in command:
                return JsonResponse({
                    "response": "Opening news",
                    "action": "news"
                })

            if "search" in command or "google" in command:
                query = command.replace("search", "").replace("google", "").strip()
                return JsonResponse({
                    "response": f"Searching {query}",
                    "action": "search",
                    "query": query
                })

            if "time" in command:
                now = datetime.datetime.now().strftime("%H:%M")
                return JsonResponse({"response": f"The time is {now}"})

            if "hello" in command or "hi" in command:
                return JsonResponse({"response": "Hello! How can I help you?"})

            if "who are you" in command:
                return JsonResponse({"response": "I am Jarvis, your assistant."})

            if "how are you" in command:
                return JsonResponse({"response": "I am functioning perfectly."})

        except:
            pass

        ChatHistory.objects.create(user_message=command, jarvis_response="fallback")

        return JsonResponse({
            "response": "Try asking math, calculus, graph, play, search or commands"
        })
