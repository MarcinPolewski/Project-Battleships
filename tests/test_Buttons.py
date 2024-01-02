from Buttons import Button


class fake_image:
    def get_height():
        return 100

    def get_width():
        return 50


def test_check_if_mouse_on_button():
    button = Button(position=(20, 30), screen="this is screen", image=fake_image)
    assert button.check_if_mouse_on_button((30, 40))
    assert button.check_if_mouse_on_button((21, 32))
    assert button.check_if_mouse_on_button((50, 60))
    assert not button.check_if_mouse_on_button((15, 15))
    assert not button.check_if_mouse_on_button((200, 15))
    assert not button.check_if_mouse_on_button((15, 200))


def test_check_if_mouse_on_button_corners():
    button = Button(position=(0, 0), screen="this is screen", image=fake_image)
    assert button.check_if_mouse_on_button((0, 0))
    assert button.check_if_mouse_on_button((0, 100))
    assert button.check_if_mouse_on_button((50, 100))
    assert button.check_if_mouse_on_button((50, 0))
