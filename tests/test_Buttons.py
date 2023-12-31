from Buttons import Button


def test_check_if_mouse_on_button():
    button = Button(
        position=(20, 30), height=100, width=50, image="for_testing_not_image"
    )
    assert button.check_if_mouse_on_button((30, 40))
    assert not button.check_if_mouse_on_button((15, 15))
    assert not button.check_if_mouse_on_button((200, 15))
    assert not button.check_if_mouse_on_button((15, 200))


def test_check_if_mouse_on_button_corners():
    button = Button(
        position=(0, 0), height=100, width=50, image="for_testing_not_image"
    )
    assert button.check_if_mouse_on_button((0, 0))
    assert button.check_if_mouse_on_button((0, 100))
    assert button.check_if_mouse_on_button((50, 100))
    assert button.check_if_mouse_on_button((50, 0))
