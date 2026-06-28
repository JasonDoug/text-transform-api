import urllib.request
import urllib.parse
import json
import re
import html
from datetime import datetime, timezone
import asyncio
from typing import Any
from app.schemas import SourceItem

def clean_reddit_html(html_content: str) -> str:
    # Find content between the markdown divs
    match = re.search(r'<!-- SC_OFF --><div class="md">(.*?)</div>\s*<!-- SC_ON -->', html_content, re.DOTALL)
    if match:
        content = match.group(1)
    else:
        # Fallback: remove everything from "submitted by" onwards
        content = re.split(r'\s*submitted by\s*', html_content, flags=re.IGNORECASE)[0]
    
    # Strip HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    # Decode HTML entities
    content = html.unescape(content)
    return content.strip()

def _fetch_url_json(url: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))

def _fetch_url_raw(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read()

def parse_reddit_atom(xml_content: bytes, subreddit: str, limit: int) -> list[SourceItem]:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    
    source_items = []
    entries = root.findall("atom:entry", ns)
    
    for entry in entries[:limit]:
        title_el = entry.find("atom:title", ns)
        title = title_el.text if title_el is not None else ""
        
        id_el = entry.find("atom:id", ns)
        guid = id_el.text if id_el is not None else ""
        post_id = guid.split("_")[-1] if "_" in guid else guid
        if post_id.startswith("t3:"):
            post_id = post_id[3:]
        elif post_id.startswith("t3"):
            post_id = post_id[2:]
            
        author_name_el = entry.find("atom:author/atom:name", ns)
        author = author_name_el.text if author_name_el is not None else ""
        if author.startswith("/u/"):
            author = author[3:]
            
        link_el = entry.find("atom:link", ns)
        link = link_el.attrib.get("href", "") if link_el is not None else ""
        
        content_el = entry.find("atom:content", ns)
        description = content_el.text if content_el is not None else ""
        body = clean_reddit_html(description)
        
        updated_el = entry.find("atom:updated", ns)
        updated_str = updated_el.text if updated_el is not None else ""
        try:
            created_at = datetime.fromisoformat(updated_str.replace("Z", "+00:00"))
        except Exception:
            created_at = datetime.now(timezone.utc)
            
        source_items.append(
            SourceItem(
                id=post_id,
                title=title,
                body=body if body else None,
                author=author,
                url=link,
                score=None,
                numComments=None,
                createdAt=created_at,
                subreddit=subreddit,
                source="reddit",
            )
        )
    return source_items

async def fetch_reddit(subreddit: str, sort: str, time_period: str | None, limit: int) -> list[SourceItem]:
    sort_mapped = "hot" if sort == "best" else sort
    rss_url = f"https://www.reddit.com/r/{subreddit}/{sort_mapped}.rss"
    if sort == "top" and time_period:
        rss_url += f"?t={time_period}"
    
    url = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote_plus(rss_url)}"
    
    try:
        data = await asyncio.to_thread(_fetch_url_json, url)
        if data.get("status") != "ok":
            raise ValueError(f"rss2json status: {data.get('status')}")
            
        items = data.get("items", [])
        source_items = []
        
        for item in items[:limit]:
            title = item.get("title", "")
            pub_date_str = item.get("pubDate", "")
            try:
                created_at = datetime.fromisoformat(pub_date_str.replace(" ", "T")).replace(tzinfo=timezone.utc)
            except Exception:
                created_at = datetime.now(timezone.utc)
                
            link = item.get("link", "")
            guid = item.get("guid", "")
            post_id = guid.split("_")[-1] if "_" in guid else guid
            if post_id.startswith("t3:"):
                post_id = post_id[3:]
            elif post_id.startswith("t3"):
                post_id = post_id[2:]
                
            author = item.get("author", "")
            if author.startswith("/u/"):
                author = author[3:]
                
            description = item.get("description", "")
            body = clean_reddit_html(description)
            
            source_items.append(
                SourceItem(
                    id=post_id,
                    title=title,
                    body=body if body else None,
                    author=author,
                    url=link,
                    score=None,
                    numComments=None,
                    createdAt=created_at,
                    subreddit=subreddit,
                    source="reddit",
                )
            )
        return source_items
    except Exception as exc:
        # Fallback to direct Atom RSS fetch
        try:
            xml_content = await asyncio.to_thread(_fetch_url_raw, rss_url)
            return parse_reddit_atom(xml_content, subreddit, limit)
        except Exception as fallback_exc:
            raise RuntimeError(f"Reddit fetch failed. rss2json error: {str(exc)}, direct fallback error: {str(fallback_exc)}")

async def fetch_hackernews(type: str, query: str | None, limit: int) -> list[SourceItem]:
    if query:
        url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote_plus(query)}&tags=story"
    elif type == "new":
        url = "https://hn.algolia.com/api/v1/search_by_date?tags=story"
    else:  # top / default
        url = "https://hn.algolia.com/api/v1/search?tags=front_page"
    
    data = await asyncio.to_thread(_fetch_url_json, url)
    hits = data.get("hits", [])
    source_items = []
    
    for hit in hits[:limit]:
        title = hit.get("title") or hit.get("story_title") or ""
        story_id = str(hit.get("objectID") or "")
        author = hit.get("author") or ""
        url_field = hit.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
        score = hit.get("points")
        num_comments = hit.get("num_comments")
        body = hit.get("story_text")
        
        created_at_i = hit.get("created_at_i")
        if created_at_i:
            created_at = datetime.fromtimestamp(created_at_i, timezone.utc)
        else:
            created_at = datetime.now(timezone.utc)
            
        source_items.append(
            SourceItem(
                id=story_id,
                title=title,
                body=body if body else None,
                author=author,
                url=url_field,
                score=score,
                numComments=num_comments,
                createdAt=created_at,
                subreddit=None,
                source="hackernews",
            )
        )
    return source_items

async def fetch_devto(tag: str | None, limit: int) -> list[SourceItem]:
    url = f"https://dev.to/api/articles?per_page={limit}"
    if tag:
        url += f"&tag={urllib.parse.quote_plus(tag)}"
        
    data = await asyncio.to_thread(_fetch_url_json, url)
    source_items = []
    
    if not isinstance(data, list):
        return []
        
    for item in data:
        article_id = str(item.get("id") or "")
        title = item.get("title") or ""
        body = item.get("description") or ""
        author = item.get("user", {}).get("username") or ""
        url_field = item.get("url") or ""
        score = item.get("public_reactions_count")
        num_comments = item.get("comments_count")
        
        published_at_str = item.get("published_at")
        try:
            created_at = datetime.fromisoformat(published_at_str.replace("Z", "+00:00"))
        except Exception:
            created_at = datetime.now(timezone.utc)
            
        source_items.append(
            SourceItem(
                id=article_id,
                title=title,
                body=body if body else None,
                author=author,
                url=url_field,
                score=score,
                numComments=num_comments,
                createdAt=created_at,
                subreddit=None,
                source="devto",
            )
        )
    return source_items
