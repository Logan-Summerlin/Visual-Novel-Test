## gui.rpy
## GUI configuration for the visual novel.

init python:
    gui.init(1920, 1080)

## Colors
define gui.accent_color = '#6b4c8a'
define gui.idle_color = '#aaaaaa'
define gui.idle_small_color = '#999999'
define gui.hover_color = '#c0a0e0'
define gui.selected_color = '#ffffff'
define gui.insensitive_color = '#55555580'
define gui.muted_color = '#3a3a5c'
define gui.hover_muted_color = '#4a4a6c'

define gui.text_color = '#ffffff'
define gui.interface_text_color = '#ffffff'

## Fonts
define gui.text_font = gui.preference("font_family", "DejaVuSans.ttf")
define gui.name_text_font = gui.preference("font_family", "DejaVuSans.ttf")
define gui.interface_text_font = gui.preference("font_family", "DejaVuSans.ttf")

define gui.text_size = 28
define gui.name_text_size = 36
define gui.interface_text_size = 28
define gui.label_text_size = 36
define gui.notify_text_size = 24
define gui.title_text_size = 64

## Main Menu
define gui.main_menu_background_size_group = None

## Dialogue
define gui.dialogue_text_xalign = 0.0

define gui.textbox_height = 278
define gui.textbox_yalign = 1.0

define gui.name_xpos = 360
define gui.name_ypos = 0
define gui.name_xalign = 0.0

define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(5, 5, 5, 5)
define gui.namebox_tile = False

define gui.dialogue_xpos = 402
define gui.dialogue_ypos = 75
define gui.dialogue_width = 1116

## Buttons
define gui.button_width = None
define gui.button_height = None
define gui.button_borders = Borders(6, 6, 6, 6)
define gui.button_tile = False
define gui.button_text_font = gui.interface_text_font
define gui.button_text_size = gui.interface_text_size
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color
define gui.button_text_xalign = 0.0

## Choice Buttons
define gui.choice_button_width = 1185
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(150, 8, 150, 8)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = "#cccccc"
define gui.choice_button_text_hover_color = "#ffffff"
define gui.choice_button_text_insensitive_color = "#444444"

## Slots
define gui.slot_button_width = 414
define gui.slot_button_height = 309
define gui.slot_button_borders = Borders(15, 15, 15, 15)
define gui.slot_button_text_size = 21
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color
define gui.slot_button_text_selected_idle_color = gui.selected_color
define gui.slot_button_text_selected_hover_color = gui.hover_color

define config.thumbnail_width = 384
define config.thumbnail_height = 216

define gui.file_slot_cols = 3
define gui.file_slot_rows = 2

## Navigation
define gui.navigation_xpos = 60
define gui.skip_ypos = 15

## Scrollbar
define gui.scrollbar_size = 18
define gui.unscrollable = "hide"

define gui.bar_size = 38
define gui.bar_tile = False
define gui.bar_borders = Borders(6, 6, 6, 6)

## NVL
define gui.nvl_borders = Borders(0, 15, 0, 30)
define gui.nvl_height = 173
define gui.nvl_spacing = 15
define gui.nvl_name_xpos = 645
define gui.nvl_name_ypos = 0
define gui.nvl_name_width = 225
define gui.nvl_name_xalign = 1.0
define gui.nvl_text_xpos = 675
define gui.nvl_text_ypos = 12
define gui.nvl_text_width = 885
define gui.nvl_text_xalign = 0.0
define gui.nvl_thought_xpos = 360
define gui.nvl_thought_ypos = 0
define gui.nvl_thought_width = 1170
define gui.nvl_thought_xalign = 0.0
define gui.nvl_button_xpos = 675
define gui.nvl_button_xalign = 0.0
