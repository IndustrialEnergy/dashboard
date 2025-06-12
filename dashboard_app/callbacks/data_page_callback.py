from dash import callback, Output, Input, State, html


def toggle_emissions_collapse(app):
    @app.callback(
        [
            Output("collapse-emissions", "is_open"),
            Output("collapse-button-emissions", "children"),
        ],
        [Input("collapse-button-emissions", "n_clicks")],
        [State("collapse-emissions", "is_open")],
    )
    def _toggle_emissions_collapse(n, is_open):
        if n:
            if is_open:
                return False, [
                    html.I(className="fas fa-chevron-right me-2"),
                    "View Emission Factors Table",
                ]
            else:
                return True, [
                    html.I(className="fas fa-chevron-down me-2"),
                    "Hide Emission Factors Table",
                ]
        return is_open, [
            html.I(className="fas fa-chevron-right me-2"),
            "View Emission Factors Table",
        ]

    return _toggle_emissions_collapse


def toggle_diagram_modal(app):
    @app.callback(
        Output("diagram-modal", "is_open"),
        [
            Input("data-flow-diagram", "n_clicks"),
            Input("close-diagram-modal", "n_clicks"),
        ],
        [State("diagram-modal", "is_open")],
        prevent_initial_call=True,
    )
    def _toggle_diagram_modal(n_diagram, n_close, is_open):
        if n_diagram or n_close:
            return not is_open
        return is_open

    return _toggle_diagram_modal
