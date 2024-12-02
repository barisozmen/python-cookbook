
self_closing_tags = ['img', 'br', 'link', 'meta']


def render_html(raw, indent=0):
      # print('raw>',raw)
    if raw is None: return
    splitted = raw[0].split(maxsplit=1)
    tag, attributes = splitted if len(splitted)>1 else (splitted[0], '')
    html = '\t'*indent + (f'<{tag} {attributes}>\n' if len(attributes) else f'<{tag}>\n')
    for c in raw[1:]:
        if isinstance(c, str):
            html += '\t'*(indent+1) + c + '\n'
        else:
            html += render_html(c, indent+1)
    html += '\t'*indent + ('' if tag in self_closing_tags else f'</{tag}>') + '\n'
    return html

DATA_TIPPY_CONTENT = 'data-tippy-content'



script = """
tippy('["""+DATA_TIPPY_CONTENT+"""]', {
    allowHTML: true,
    theme: 'light',
    placement: 'top',
    interactive: true,
    // Add these for text wrapping:
    animation: 'fade',
    inlinePositioning: true,
});
"""

style = """
.hovery {
    /* Center the element */
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
"""

# https://atomiks.github.io/tippyjs/
raw = (
    'html',
    ('head',
        ('title', 'Tippy.js Demo'),
        ('link rel="stylesheet" href="https://unpkg.com/tippy.js@6/themes/light.css"', ''),
    ),
    ('body',
        ('style', style),
        (f'div class="hovery" {DATA_TIPPY_CONTENT}="Tippy.js is working!"', 'Hover over me'),
        ('script src="https://unpkg.com/@popperjs/core@2/dist/umd/popper.min.js"', ''),
        ('script src="https://unpkg.com/tippy.js@6/dist/tippy-bundle.umd.js"', ''),
        ('script src="https://code.jquery.com/jquery-3.6.0.min.js"', ''),
        ('script', script),
    )
)
    
    
html = render_html(raw)
print(html)
