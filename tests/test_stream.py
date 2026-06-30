"""Tests for stream data generation."""

def test_import():
    import stream
    assert hasattr(stream, "generate_stream_item")

def test_messages_not_empty():
    from stream import MESSAGES
    assert len(MESSAGES) > 0
