## options.rpy
## Configuration options for the visual novel.

define config.name = _("Echoes of the Forgotten Tower")
define config.version = "1.0"

define gui.show_name = True
define config.window_title = "Echoes of the Forgotten Tower"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.main_menu_music = None

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

default preferences.text_cps = 40
default preferences.afm_time = 15

define config.save_directory = "EchoesOfTheForgottenTower-1702"

define config.window_icon = None
