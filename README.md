# Code Execution for HTML and Python

This project provides a simple API interface for executing HTML and Python code. The code is written in Django and uses `subprocess` to execute the code.

## Features

- **HTML Code**: When HTML code is received, the API saves it to a file named `output.html` and opens it in the default browser.
- **Python Code**: When Python code is received, the API executes it and returns the standard output or execution errors.

## Code

```python
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        language = request.POST.get('language', '')
        try:
            if language.lower() == 'html':
                with open('output.html', 'w') as f:
                    f.write(code)
                subprocess.run(['xdg-open', 'output.html'])  
                return JsonResponse({'output': 'HTML code executed successfully'})
            else:
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
            return JsonResponse({'output': 'Error: ' + str(e)})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
```
