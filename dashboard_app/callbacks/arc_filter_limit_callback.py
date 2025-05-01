from dash import Input, Output, State
import dash_bootstrap_components as dbc


def arc_filter_limit_callback(app):
    @app.callback(
        Output("arc-filter", "value"),
        Output("warning-message", "children"),
        Input("arc-filter", "value"),
        State("arc-filter", "value"),
        prevent_initial_call=True,
    )
    def limit_dropdown_selection(new_selection, current_selection):
        max_selections = 4

        # handle initial state
        if new_selection is None:
            return new_selection, ""

        # if trying to select more than max, keep current selection
        if len(new_selection) > max_selections:
            warning = dbc.Alert(
                f"⚠️ Select Maximum {max_selections} ARC for optimal performance.",
                color="warning",
                dismissable=True,
                style={"margin-top": "10px"},
            )
            return current_selection, warning

        return new_selection, ""
