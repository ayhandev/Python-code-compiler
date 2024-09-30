import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        language = request.POST.get('language', '')

        # Ограничение для выполнения только HTML и Python
        allowed_languages = ['html', 'python']

        if language.lower() not in allowed_languages:
            return JsonResponse({'output': 'Error: Unsupported language'}, status=400)

        try:
            if language.lower() == 'html':
                if '<script>' in code.lower() or '</script>' in code.lower():
                    return JsonResponse({'output': 'Error: Scripts are not allowed in HTML'}, status=400)

                with open('output.html', 'w') as f:
                    f.write(code)

                subprocess.run(['xdg-open', 'output.html'])
                return JsonResponse({'output': 'HTML code executed successfully'})

            elif language.lower() == 'python':
                forbidden_keywords = ['import os', 'import sys', 'open(', 'exec(', 'eval(', 'subprocess', '__import__', 'shutil', 'inspect', 'socket', 'threading', 'multiprocessing', 'http', 'urllib']
                if any(keyword in code for keyword in forbidden_keywords):
                    return JsonResponse({'output': 'Error: Forbidden keyword in Python code'}, status=400)

                result = subprocess.run(['python', '-c', code], capture_output=True, text=True, timeout=5)
                output = result.stdout

                if output:
                    return JsonResponse({'output': output})
                elif result.stderr:
                    return JsonResponse({'output': result.stderr})
                else:
                    return JsonResponse({'output': 'No output'})

        except subprocess.TimeoutExpired:
            return JsonResponse({'output': 'Timeout: Process execution took too long'})
        except Exception as e:
            return JsonResponse({'output': 'Error: ' + str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
