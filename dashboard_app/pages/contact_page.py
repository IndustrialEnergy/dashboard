from dash import html
from layouts.base_layout import create_base_layout

def create_contact_page():
    content = html.H4(
        "Coming soon...",
        style={
            'width': '50%',          
            'margin': '0 auto',    
            'textAlign': 'center',    
            'paddingTop': '50px'
        }
    )
    
    return create_base_layout(content)