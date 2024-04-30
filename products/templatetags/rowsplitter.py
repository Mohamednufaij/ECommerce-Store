from django import template

register = template.Library()

@register.filter(name='chunks')
def rowsplit(list,rowsize):
    chunk = []
    i = 0
    for data in list:
        chunk.append(data)
        i += 1
        if i == rowsize:
            yield chunk
            chunk = []
            i = 0  # Reset i after yielding chunk
    if chunk:  # Yield the remaining elements
        yield chunk
