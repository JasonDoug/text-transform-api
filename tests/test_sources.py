from fastapi.testclient import TestClient
from app.main import app
from app import sources

def test_reddit_endpoint_success(monkeypatch):
    mock_response = {
        "status": "ok",
        "feed": {
            "url": "https://www.reddit.com/r/python/hot.rss",
            "title": "hot scoring links : Python",
            "link": "https://www.reddit.com/r/python/hot",
            "author": "",
            "description": "...",
            "image": "..."
        },
        "items": [
            {
                "title": "Test Title",
                "pubDate": "2026-06-28 01:58:24",
                "link": "https://www.reddit.com/r/Python/comments/1uhkicg/test/",
                "guid": "t3_1uhkicg",
                "author": "/u/TestUser",
                "thumbnail": "",
                "description": "<!-- SC_OFF --><div class=\"md\"><p>Test self text body</p></div><!-- SC_ON --> submitted by /u/TestUser",
                "content": "..."
            }
        ]
    }

    called_url = []

    def fake_fetch_url_json(url):
        called_url.append(url)
        return mock_response

    monkeypatch.setattr(sources, "_fetch_url_json", fake_fetch_url_json)

    client = TestClient(app)
    response = client.get("/v1/sources/reddit/python?sort=top&time_period=week&limit=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "1uhkicg"
    assert data[0]["title"] == "Test Title"
    assert data[0]["body"] == "Test self text body"
    assert data[0]["author"] == "TestUser"
    assert data[0]["url"] == "https://www.reddit.com/r/Python/comments/1uhkicg/test/"
    assert data[0]["subreddit"] == "python"
    assert data[0]["source"] == "reddit"
    import urllib.parse
    decoded_url = urllib.parse.unquote(called_url[0])
    assert "https://www.reddit.com/r/python/top.rss" in decoded_url
    assert "t=week" in decoded_url


def test_reddit_endpoint_limit_validation():
    client = TestClient(app)
    response = client.get("/v1/sources/reddit/python?limit=60")
    assert response.status_code == 400
    assert "Limit must be between 1 and 50" in response.json()["detail"]


def test_hackernews_endpoint_success(monkeypatch):
    mock_response = {
        "hits": [
            {
                "title": "HN Title",
                "objectID": "12345",
                "author": "hn_user",
                "url": "https://example.com/art",
                "points": 100,
                "num_comments": 5,
                "story_text": "HN Body text",
                "created_at_i": 1782697200
            }
        ]
    }

    called_url = []

    def fake_fetch_url_json(url):
        called_url.append(url)
        return mock_response

    monkeypatch.setattr(sources, "_fetch_url_json", fake_fetch_url_json)

    client = TestClient(app)
    response = client.get("/v1/sources/hackernews?type=new&limit=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "12345"
    assert data[0]["title"] == "HN Title"
    assert data[0]["body"] == "HN Body text"
    assert data[0]["author"] == "hn_user"
    assert data[0]["url"] == "https://example.com/art"
    assert data[0]["score"] == 100
    assert data[0]["numComments"] == 5
    assert data[0]["source"] == "hackernews"
    assert "search_by_date" in called_url[0]


def test_devto_endpoint_success(monkeypatch):
    mock_response = [
        {
            "id": 99999,
            "title": "DevTo Title",
            "description": "DevTo Description",
            "user": {"username": "devto_user"},
            "url": "https://dev.to/devto_user/devto-title",
            "public_reactions_count": 42,
            "comments_count": 8,
            "published_at": "2026-06-28T01:58:24Z"
        }
    ]

    called_url = []

    def fake_fetch_url_json(url):
        called_url.append(url)
        return mock_response

    monkeypatch.setattr(sources, "_fetch_url_json", fake_fetch_url_json)

    client = TestClient(app)
    response = client.get("/v1/sources/devto?tag=python&limit=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "99999"
    assert data[0]["title"] == "DevTo Title"
    assert data[0]["body"] == "DevTo Description"
    assert data[0]["author"] == "devto_user"
    assert data[0]["url"] == "https://dev.to/devto_user/devto-title"
    assert data[0]["score"] == 42
    assert data[0]["numComments"] == 8
    assert data[0]["source"] == "devto"
    assert "tag=python" in called_url[0]
