from __future__ import annotations

from gesture_control.backends.macos import _normalized_to_screen_position


def test_macos_cursor_mapping_flips_x_to_user_perspective() -> None:
    screen_width = 1000
    screen_height = 500

    user_left = _normalized_to_screen_position(
        (0.80, 0.50),
        screen_width=screen_width,
        screen_height=screen_height,
    )
    user_right = _normalized_to_screen_position(
        (0.20, 0.50),
        screen_width=screen_width,
        screen_height=screen_height,
    )

    assert user_left[0] < user_right[0]
    assert user_left[1] == user_right[1]


def test_macos_cursor_mapping_keeps_y_direction_and_bounds() -> None:
    screen_width = 1000
    screen_height = 500

    up = _normalized_to_screen_position(
        (0.50, 0.20),
        screen_width=screen_width,
        screen_height=screen_height,
    )
    down = _normalized_to_screen_position(
        (0.50, 0.80),
        screen_width=screen_width,
        screen_height=screen_height,
    )
    bounded = _normalized_to_screen_position(
        (-1.0, 2.0),
        screen_width=screen_width,
        screen_height=screen_height,
    )

    assert up[1] < down[1]
    assert bounded == (999, 499)
