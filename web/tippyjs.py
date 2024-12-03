

from render_html import render_html

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
# Run: python tippyjs.py > tippyjs.html