from fastapi.testclient import TestClient

from app.main import app


class FakeChoice:
    def __init__(self, message):
        self.message = message


class FakeMessage:
    def __init__(self, content):
        self.content = content


class FakeCompletion:
    def __init__(self, content):
        self.choices = [FakeChoice(FakeMessage(content))]


def test_named_podcast_endpoint_uses_podcast_prompt(monkeypatch):
    monkeypatch.setenv("TRANSFORMATION_PROVIDER", "openai-compatible")
    monkeypatch.setenv("TRANSFORMATION_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("TRANSFORMATION_API_KEY", "ollama")
    monkeypatch.setenv("TRANSFORMATION_MODEL", "llama3.1:8b")

    calls = {}

    def fake_completion(**kwargs):
        calls.update(kwargs)
        return FakeCompletion("Host 1: Welcome.")

    monkeypatch.setattr("litellm.completion", fake_completion)

    client = TestClient(app)
    response = client.post(
        "/v1/transformations/podcast",
        json={
            "text": "FastAPI makes APIs simple.",
            "options": {
                "length": "short",
                "format": "json",
                "tone": "friendly",
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["id"].startswith("pod_")
    assert "podcast script" in calls["messages"][1]["content"]
    assert "friendly" in calls["messages"][1]["content"]
    assert "valid JSON" in calls["messages"][1]["content"]


def test_named_explainer_endpoint_uses_explainer_prompt(monkeypatch):
    monkeypatch.setenv("TRANSFORMATION_PROVIDER", "openai-compatible")
    monkeypatch.setenv("TRANSFORMATION_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("TRANSFORMATION_API_KEY", "ollama")
    monkeypatch.setenv("TRANSFORMATION_MODEL", "llama3.1:8b")

    calls = {}

    def fake_completion(**kwargs):
        calls.update(kwargs)
        return FakeCompletion("Here is the explanation.")

    monkeypatch.setattr("litellm.completion", fake_completion)

    client = TestClient(app)
    response = client.post(
        "/v1/transformations/explainer",
        json={
            "text": "FastAPI makes APIs simple.",
            "options": {
                "length": "medium",
                "format": "plain",
                "tone": "professional",
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["id"].startswith("exp_")
    assert "beginner-friendly explainer" in calls["messages"][1]["content"]
    assert "professional" in calls["messages"][1]["content"]
