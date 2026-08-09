import pytest
from textual.widgets import Input, ListView

from openmoses.app import DashboardScreen, OpenMosesApp, SettingsScreen
from openmoses.widgets import MessageCard


@pytest.mark.asyncio
async def test_app_opens_on_the_dashboard() -> None:
    app = OpenMosesApp()

    async with app.run_test(size=(140, 42)) as pilot:
        assert isinstance(app.screen, DashboardScreen)
        menu = app.screen.query_one("#dashboard-menu", ListView)
        assert menu.has_focus
        assert menu.index == 0
        assert menu.highlighted_child is not None
        assert menu.highlighted_child.has_class("-highlight")
        await pilot.pause()


@pytest.mark.asyncio
async def test_chat_accepts_slash_commands() -> None:
    app = OpenMosesApp()

    async with app.run_test(size=(140, 42)) as pilot:
        await pilot.press("enter")
        await pilot.pause()

        composer = app.screen.query_one("#composer", Input)
        assert composer.has_focus

        await pilot.press("/", "a", "g", "e", "n", "t", "s", "enter")
        await pilot.pause()

        assert composer.value == ""
        assert len(app.screen.query(MessageCard)) == 1


@pytest.mark.asyncio
async def test_dashboard_supports_arrow_navigation() -> None:
    app = OpenMosesApp()

    async with app.run_test(size=(140, 42)) as pilot:
        await pilot.press("down", "enter")
        await pilot.pause()

        assert isinstance(app.screen, SettingsScreen)
        assert app.screen.section == "agents"
