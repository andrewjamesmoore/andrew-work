import os
from dotenv import load_dotenv
from contentful import Client

load_dotenv()  # Load environment variables from .env file

client = Client(
    os.getenv('CONTENTFUL_SPACE_ID'),
    os.getenv('CONTENTFUL_ACCESS_TOKEN'),
    environment=os.getenv('CONTENTFUL_ENVIRONMENT', 'master')
)

def get_all_entries(content_type):
    """Fetch all entries of a specific content type from Contentful."""
    entries = client.entries({'content_type': content_type})
    result = []
    for entry in entries:
        fields = entry.fields()
        # Handle missing or empty fields
        title = fields.get('title', 'untitled')
        description = fields.get('description', '')
        body = fields.get('body')
        slug = fields.get('slug', title.replace(" ", "-").lower())  # Generate slug if not present
        if 'embedded-assets' in body:
            for embedded_asset in body['embedded-assets']:
                if embedded_asset['type'] == 'Link' and embedded_asset['linkType'] == 'Asset':
                    image_url = embedded_asset['url']
        thumbnail = None
        # If a thumbnail exists, extract its URL
        if 'thumbnail' in fields and fields['thumbnail']:
            thumbnail = fields['thumbnail'].url()
        result.append({
            "fields": {
                "title": title,
                "description": description,
                "slug": slug,
                "thumbnail": thumbnail,
            }
        })
    return result


def fetch_project_by_slug(slug):
    """Fetch a project entry by its slug from Contentful."""
    try:
        entries = client.entries({'content_type': 'projects', 'fields.slug': slug})  # Filter by slug
        if entries:
            return entries[0].fields()  # Return the fields of the first matching entry
        else:
            return None  # Return None if no matching project is found
    except Exception as e:
        print(f"Error fetching project with slug {slug}: {e}")
        return None

def fetch_experiment_by_slug(slug):
    """Fetch an experiment entry by its slug from Contentful."""
    try:
        entries = client.entries({'content_type': 'experiments', 'fields.slug': slug})  # Filter by slug
        if entries:
            return entries[0].fields()  # Return the fields of the first matching entry
        else:
            return None  # Return None if no matching project is found
    except Exception as e:
        print(f"Error fetching experiment with slug {slug}: {e}")
        return None