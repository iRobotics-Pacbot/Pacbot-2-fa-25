import pytest
import json
# Assuming your library is named 'my_game_library'
from pacbot_rs import PyGameEngine

@pytest.fixture
def engine():
    """Fixture to provide a fresh engine for each test."""
    return PyGameEngine(clock_rate=24)

def test_initial_state(engine):
    """Verify the default starting values."""
    assert engine.get_score() == 0
    assert engine.get_lives() > 0
    assert engine.get_level() == 1
    assert engine.is_paused() is False

def test_repr(engine):
    """Check the string representation."""
    rep = repr(engine)
    assert "PyGameEngine" in rep
    assert "score=0" in rep

def test_engine_stepping(engine):
    """Verify that the tick count increases when stepping."""
    # Check JSON state for tick count
    state_before = json.loads(engine.get_state_json())
    ticks_before = state_before.get("curr_ticks", 0)
    
    engine.step()
    
    state_after = json.loads(engine.get_state_json())
    assert state_after["curr_ticks"] == ticks_before + 1

def test_reset(engine):
    """Test that the reset method clears the state."""
    # Manually tick a few times
    for _ in range(5):
        engine.step()
    
    engine.reset()
    assert engine.get_score() == 0
    # Assuming reset puts ticks back to 0
    state = json.loads(engine.get_state_json())
    assert state["curr_ticks"] == 0

def test_send_command(engine):
    """Test sending a byte command (e.g., a move command)."""
    # Create a dummy command as bytes (matching Vec<u8> in Rust)
    # The actual bytes depend on your interpret_command logic
    move_up_command = b"\x01\x02" 
    
    result = engine.send_command(move_up_command)
    assert isinstance(result, bool)

def test_pause_toggle(engine):
    """Test if the engine correctly reflects pause states."""
    # This depends on your interpret_command supporting a pause toggle
    pause_command = b"PAUSE" # Example command
    engine.send_command(pause_command)
    
    # Check if tick count stops increasing
    ticks_start = json.loads(engine.get_state_json())["curr_ticks"]
    engine.step()
    ticks_end = json.loads(engine.get_state_json())["curr_ticks"]
    
    assert ticks_start == ticks_end