## Documentation

Source files for dashboard documentation written in Quarto (.qmd files).

### File Structure

```
docs/
├── _quarto.yml                        # Quarto configuration
├── index.qmd                          # Documentation index
├── dashboard_installation_guide.qmd   # Installation guide
├── data_update_guide.qmd              # Data pipeline guide
└── update_dashboard_guide.qmd         # Dashboard update guide
```

### Update Documentation

1. **Edit** any `.qmd` file in this folder
2. **Render** to dashboard:

   ```bash
   cd docs
   quarto render
   ```
3. **Check** changes at `dashboard/docs` page

### Files

- `index.qmd` - Documentation hub
- `dashboard_installation_guide.qmd` - Installation guide  
- `data_update_guide.qmd` - Data pipeline guide
- `update_dashboard_guide.qmd` - Dashboard update guide

Rendered files are automatically saved to `dashboard_app/assets/docs/` and are served at `/assets/docs/`. 