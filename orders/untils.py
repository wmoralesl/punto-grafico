from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.template import TemplateDoesNotExist


def printPDF(template_src, css_url, context_dict=None):
    if context_dict is None:
        context_dict = {}
        
    try:
        template = get_template(template_src)
        html_template = template.render(context_dict)
        
        # Intenta generar el PDF
        pdf_file = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])
        
        # Si se genera correctamente, devuelve el PDF como una respuesta HTTP
        return HttpResponse(pdf_file, content_type='application/pdf')
        
    except TemplateDoesNotExist as e:
        # Maneja el caso en que el template no existe
        error_message = f"Error: El template '{template_src}' no existe."
        return HttpResponse(error_message, status=500)
        
    except Exception as e:
        # Maneja cualquier otro error que pueda ocurrir durante el proceso
        error_message = f"Error: {str(e)}"
        return HttpResponse(error_message, status=500)

