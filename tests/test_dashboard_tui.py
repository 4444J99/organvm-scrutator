"""Tests for Dashboard TUI rendering."""

from io import StringIO
import pytest
from rich.console import Console

from organvm_scrutator.viz.dashboard import Dashboard


def test_render_tui_empty_analyses():
    """Verify render_tui succeeds with empty analyses kwargs."""
    dashboard = Dashboard()
    output_io = StringIO()
    dashboard.console = Console(file=output_io, width=120, color_system=None)

    dashboard.render_tui()

    output = output_io.getvalue()
    assert "ORGANVM SCRUTATOR" in output
    assert "Plans" in output
    assert "Questions" in output
    assert "Suggestions" in output
    assert "Atoms" in output


def test_render_tui_populated_analyses():
    """Verify render_tui succeeds and renders all sections with populated analyses."""
    dashboard = Dashboard()
    output_io = StringIO()
    dashboard.console = Console(file=output_io, width=120, color_system=None)

    analyses = {
        'plans': {'total_plans': 5},
        'questions': {
            'total_questions': 12,
            'answered': 8,
            'unanswered': 4,
            'answer_rate': 0.667,
        },
        'suggestions': {
            'total_suggestions': 10,
            'accepted': 7,
            'rejected': 3,
            'acceptance_rate': 0.7,
        },
        'atoms': {
            'total_atoms': 20,
            'completion_rate': 0.85,
        },
        'energy': {
            'total_sessions': 4,
            'total_input_energy': 22,
            'total_output_energy': 25,
            'system_efficiency': 1.14,
            'metabolic_state': 'CATABOLIC',
        },
        'gaps': [
            {
                'gap_id': 'GAP-001',
                'category': 'governance',
                'severity': 'HIGH',
                'research_priority': 'P1',
            }
        ],
    }

    dashboard.render_tui(**analyses)

    output = output_io.getvalue()
    assert "ORGANVM SCRUTATOR" in output
    assert "Question Analysis" in output
    assert "Suggestion Analysis" in output
    assert "Energy Analysis" in output
    assert "Top Research Gaps" in output
    assert "CATABOLIC" in output
    assert "GAP-001" in output
