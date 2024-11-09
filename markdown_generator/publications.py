import pandas as pd
import os

# Read the TSV file
publications = pd.read_csv("publications.tsv", sep="\t", header=0)

# Function to escape special characters for YAML
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c, c) for c in text)

# Iterate over each row in the DataFrame
for row, item in publications.iterrows():
    md_filename = str(item.pub_date) + "-" + item.url_slug + ".md"
    html_filename = str(item.pub_date) + "-" + item.url_slug
    year = item.pub_date[:4]

    ## YAML variables
    md = "---\ntitle: \"" + item.title + '"\n'
    
    # Add the type field
    if 'type' in item and pd.notna(item['type']):
        md += "type: \"" + item['type'] + "\"\n"
    
    md += "collection: publications"
    md += "\npermalink: /publication/" + html_filename
    
    if len(str(item.excerpt)) > 5:
        md += "\nexcerpt: '" + html_escape(item.excerpt) + "'"
    
    md += "\ndate: " + str(item.pub_date)
    md += "\nvenue: '" + html_escape(item.venue) + "'"
    
    if len(str(item.paper_url)) > 5:
        md += "\npaperurl: '" + item.paper_url + "'"
    
    md += "\ncitation: '" + html_escape(item.citation) + "'"
    md += "\n---"
    
    ## Markdown description for individual page
    if len(str(item.paper_url)) > 5:
        md += "\n\n<a href='" + item.paper_url + "'>Download paper here</a>\n"
    
    if len(str(item.excerpt)) > 5:
        md += "\n" + html_escape(item.excerpt) + "\n"
    
    # Add the "Submitted" or "Published" line based on type
    if item['type'].lower() == "manuscripts":
        md += f"\nSubmitted to {item.venue}, {year}."
    else:
        md += f"\nPublished in {item.venue}, {year}."
    
    md += "\nRecommended citation: " + item.citation
    
    # Write to the Markdown file
    md_filename = os.path.basename(md_filename)
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)
