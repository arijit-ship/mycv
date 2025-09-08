# CV Themes

This folder contains **themes/templates** for the modular CV system.  
Each theme defines the **look and layout** of the CV when rendered from YAML/JSON data.  

---

## Folder Structure

```

themes/
├── classic/
│   └── template.tex
├── modern/
│   └── template.tex
├── fancy/
│   └── template.html
└── minimal/
└── template.md

````

- Each subfolder represents a **theme**.
- The `template.*` file can be in **any format** (LaTeX, HTML, Markdown, plain text, etc.).
- The **CV data** comes from `mycv.yaml` or `mycv.json` and is filled into the template using **Jinja2 placeholders**.

---

## How to Create a New Theme

1. Create a new folder under `themes/`, e.g., `themes/professional/`.
2. Add a template file (`template.tex`, `template.html`, etc.) inside the folder.
3. Use **Jinja2 placeholders** to insert CV data. Example for LaTeX:

```latex
\section*{Personal Info}
Name: {{ cv.personal_info.name }} \\
Email: {{ cv.personal_info.email }} \\
Phone: {{ cv.personal_info.phone }}
````

4. Loop over lists using `{% for ... %}`:

```latex
\section*{Education}
{% for edu in cv.education %}
- {{ edu.degree }} | {{ edu.institution }} | {{ edu.period }}
  {% if edu.notes %}
    {% for note in edu.notes %}
      \newline {{ note }}
    {% endfor %}
  {% endif %}
{% endfor %}
```

5. Use conditionals to check optional sections:

```latex
{% if cv.about.summary %}
\section*{About}
{{ cv.about.summary }}
{% endif %}
```

---

## Available CV Data Fields

Your template can access the following fields from `cv`:

* `cv.personal_info` – dictionary with name, email, phone, github, linkedin, address
* `cv.about` – dictionary with summary
* `cv.education` – list of dictionaries
* `cv.experience` – list of dictionaries
* `cv.skills` – dictionary with `languages` and `technologies`
* `cv.projects` – list of dictionaries
* `cv.certificates` – list of dictionaries
* `cv.presentations` – list of dictionaries

You can also fetch any **custom section** using:

```jinja
{{ cv.get_section('section_name') }}
```

---

## Notes

* Templates are **fully flexible**. You can use any valid LaTeX, HTML, Markdown, or plain text formatting.
* Keep your template clean and organized; all dynamic data should be inserted via Jinja2 placeholders.
* If using LaTeX, the `CVRenderer` class can compile the rendered `.tex` file into PDF automatically.

---

## Example

```bash
python mycv/src/render.py --template themes/classic/template.tex
```

This will:

1. Load the CV data from `mycv.yaml`.
2. Render the LaTeX template with placeholders replaced.
3. Output `cv.tex` and compile it into `cv.pdf` (if LaTeX).

```
```
