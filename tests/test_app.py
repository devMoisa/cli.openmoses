import pytest
from textual.widgets import Input

from openmoses.app import OpenMosesApp
from openmoses.widgets import MessageCard


@pytest.mark.asyncio
async def test_app_mounts_and_accepts_a_message() -> None:
    app = OpenMosesApp()

    async with app.run_test(size=(140, 42)) as pilot:
        composer = app.query_one("#composer", Input)
        assert composer.has_focus
        initial_messages = len(app.query(MessageCard))

        await pilot.press("h", "e", "l", "l", "o", "enter")
        await pilot.pause()

        assert composer.value == ""
        assert len(app.query(MessageCard)) == initial_messages + 1
