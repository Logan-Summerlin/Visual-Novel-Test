#!/usr/bin/env python3
"""
Comprehensive test suite for "Echoes of the Forgotten Tower" Ren'Py visual novel.

Tests validate:
- No recursive/circular style inheritance (the original crash)
- All GUI properties referenced in screens.rpy are defined in gui.rpy
- All image assets referenced in screens exist on disk
- All bar, scrollbar, and slider images exist
- All labels referenced in jump/call statements exist
- All screens referenced in ShowMenu/use statements exist
- All character definitions are valid
- Script structure completeness (every path reaches an ending)
- No broken Ren'Py syntax patterns
- Persistent variable consistency
- Style definition correctness
- End-to-end path simulation
"""

import os
import re
import unittest

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME_DIR = os.path.join(PROJECT_ROOT, "game")
GUI_DIR = os.path.join(GAME_DIR, "gui")


def read_file(filename):
    """Read a file from the game directory."""
    filepath = os.path.join(GAME_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def read_all_rpy_files():
    """Read and return contents of all .rpy files."""
    files = {}
    for fname in os.listdir(GAME_DIR):
        if fname.endswith(".rpy"):
            files[fname] = read_file(fname)
    return files


################################################################################
## Test 1: Recursive Style Fix (The Original Crash)
################################################################################


class TestNoRecursiveStyles(unittest.TestCase):
    """Test that no style creates a circular inheritance loop.

    The original crash was caused by:
        style bar is gui_bar
    Since gui_bar inherits from bar (built-in), this created:
        bar -> gui_bar -> bar -> ... (infinite loop)
    """

    # In Ren'Py, these are the base styles and the gui_ variants that inherit
    # from them. A base style must NEVER inherit from its own gui_ variant.
    BASE_TO_GUI = {
        "bar": "gui_bar",
        "vbar": "gui_vbar",
        "scrollbar": "gui_scrollbar",
        "vscrollbar": "gui_vscrollbar",
        "slider": "gui_slider",
        "vslider": "gui_vslider",
        "button": "gui_button",
        "label": "gui_label",
        "frame": "gui_frame",
    }

    @classmethod
    def setUpClass(cls):
        cls.screens = read_file("screens.rpy")

    def test_no_bar_is_gui_bar(self):
        """style bar must NOT inherit from gui_bar (creates circular loop)."""
        self.assertNotRegex(
            self.screens,
            r'^style\s+bar\s+is\s+gui_bar',
            "CRITICAL: 'style bar is gui_bar' creates a recursive style loop!"
        )

    def test_no_vbar_is_gui_vbar(self):
        """style vbar must NOT inherit from gui_vbar."""
        self.assertNotRegex(
            self.screens,
            r'^style\s+vbar\s+is\s+gui_vbar',
            "CRITICAL: 'style vbar is gui_vbar' creates a recursive style loop!"
        )

    def test_no_scrollbar_is_gui_scrollbar(self):
        """style scrollbar must NOT inherit from gui_scrollbar."""
        self.assertNotRegex(
            self.screens,
            r'^style\s+scrollbar\s+is\s+gui_scrollbar',
            "CRITICAL: 'style scrollbar is gui_scrollbar' creates a recursive style loop!"
        )

    def test_no_vscrollbar_is_gui_vscrollbar(self):
        """style vscrollbar must NOT inherit from gui_vscrollbar."""
        self.assertNotRegex(
            self.screens,
            r'^style\s+vscrollbar\s+is\s+gui_vscrollbar',
            "CRITICAL: 'style vscrollbar is gui_vscrollbar' creates a recursive style loop!"
        )

    def test_no_base_style_inherits_from_own_gui_variant(self):
        """Comprehensive check: no base style inherits from its gui_ variant."""
        for base, gui_variant in self.BASE_TO_GUI.items():
            pattern = rf'^style\s+{re.escape(base)}\s+is\s+{re.escape(gui_variant)}\b'
            match = re.search(pattern, self.screens, re.MULTILINE)
            self.assertIsNone(
                match,
                f"CRITICAL: 'style {base} is {gui_variant}' creates a recursive style loop! "
                f"The gui_ variant inherits from the base style, so this creates a circle."
            )

    def test_bar_style_has_proper_definition(self):
        """Bar style should be properly defined with image references, not circular inheritance."""
        match = re.search(r'^style bar:$(.*?)(?=^style \w)', self.screens, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match, "style bar: should be defined with a colon (property block)")
        bar_block = match.group(1)
        self.assertIn("left_bar", bar_block, "Bar style should define left_bar property")
        self.assertIn("right_bar", bar_block, "Bar style should define right_bar property")

    def test_vbar_style_has_proper_definition(self):
        """Vbar style should be properly defined."""
        match = re.search(r'^style vbar:$(.*?)(?=^style \w)', self.screens, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match, "style vbar: should be defined with a colon (property block)")
        vbar_block = match.group(1)
        self.assertIn("top_bar", vbar_block, "Vbar style should define top_bar property")
        self.assertIn("bottom_bar", vbar_block, "Vbar style should define bottom_bar property")

    def test_scrollbar_style_has_proper_definition(self):
        """Scrollbar style should be properly defined."""
        match = re.search(r'^style scrollbar:$(.*?)(?=^style \w)', self.screens, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match, "style scrollbar: should be defined with a colon")
        block = match.group(1)
        self.assertIn("base_bar", block, "Scrollbar style should define base_bar property")
        self.assertIn("thumb", block, "Scrollbar style should define thumb property")

    def test_vscrollbar_style_has_proper_definition(self):
        """Vscrollbar style should be properly defined."""
        match = re.search(r'^style vscrollbar:$(.*?)(?=^style \w)', self.screens, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match, "style vscrollbar: should be defined with a colon")
        block = match.group(1)
        self.assertIn("base_bar", block, "Vscrollbar style should define base_bar property")
        self.assertIn("thumb", block, "Vscrollbar style should define thumb property")


################################################################################
## Test 2: Startup Crash Prevention
################################################################################


class TestStartupCrashFix(unittest.TestCase):
    """Test that known startup crashes are prevented."""

    def test_no_language_preference_without_default(self):
        """gui.preference('language') without a default causes a crash."""
        screens = read_file("screens.rpy")
        pattern = r'gui\.preference\(\s*["\']language["\']\s*\)'
        matches = re.findall(pattern, screens)
        self.assertEqual(
            len(matches), 0,
            "screens.rpy contains gui.preference('language') without a default value."
        )

    def test_no_gui_preference_without_default_anywhere(self):
        """No gui.preference() call should be missing a default value."""
        for fname, content in read_all_rpy_files().items():
            calls = re.findall(r'gui\.preference\(([^)]+)\)', content)
            for call in calls:
                args = [a.strip() for a in call.split(",")]
                self.assertGreaterEqual(
                    len(args), 2,
                    f"In {fname}: gui.preference({call}) has no default value."
                )


################################################################################
## Test 3: GUI Property Definitions
################################################################################


class TestGuiPropertyDefinitions(unittest.TestCase):
    """Test that all GUI properties referenced in screens.rpy are defined."""

    @classmethod
    def setUpClass(cls):
        cls.gui_content = read_file("gui.rpy")
        cls.screens_content = read_file("screens.rpy")

    def _assert_gui_property_defined(self, prop_name):
        """Assert that a gui property is defined in gui.rpy."""
        pattern = rf'define\s+gui\.{re.escape(prop_name)}\s*='
        self.assertRegex(
            self.gui_content, pattern,
            f"gui.{prop_name} is used in screens.rpy but not defined in gui.rpy"
        )

    # Core properties
    def test_text_size(self):
        self._assert_gui_property_defined("text_size")

    def test_name_text_size(self):
        self._assert_gui_property_defined("name_text_size")

    def test_interface_text_size(self):
        self._assert_gui_property_defined("interface_text_size")

    def test_label_text_size(self):
        self._assert_gui_property_defined("label_text_size")

    def test_title_text_size(self):
        self._assert_gui_property_defined("title_text_size")

    # Frame properties
    def test_frame_borders(self):
        self._assert_gui_property_defined("frame_borders")

    def test_frame_tile(self):
        self._assert_gui_property_defined("frame_tile")

    def test_confirm_frame_borders(self):
        self._assert_gui_property_defined("confirm_frame_borders")

    def test_skip_frame_borders(self):
        self._assert_gui_property_defined("skip_frame_borders")

    def test_notify_frame_borders(self):
        self._assert_gui_property_defined("notify_frame_borders")

    # Background properties
    def test_main_menu_background(self):
        self._assert_gui_property_defined("main_menu_background")

    def test_game_menu_background(self):
        self._assert_gui_property_defined("game_menu_background")

    # Bar and scrollbar properties
    def test_bar_size(self):
        self._assert_gui_property_defined("bar_size")

    def test_bar_tile(self):
        self._assert_gui_property_defined("bar_tile")

    def test_bar_borders(self):
        self._assert_gui_property_defined("bar_borders")

    def test_scrollbar_size(self):
        self._assert_gui_property_defined("scrollbar_size")

    def test_scrollbar_borders(self):
        self._assert_gui_property_defined("scrollbar_borders")

    def test_vscrollbar_borders(self):
        self._assert_gui_property_defined("vscrollbar_borders")

    def test_slider_borders(self):
        self._assert_gui_property_defined("slider_borders")

    def test_vslider_borders(self):
        self._assert_gui_property_defined("vslider_borders")

    def test_unscrollable(self):
        self._assert_gui_property_defined("unscrollable")

    # Dialogue properties
    def test_textbox_height(self):
        self._assert_gui_property_defined("textbox_height")

    def test_textbox_yalign(self):
        self._assert_gui_property_defined("textbox_yalign")

    def test_dialogue_xpos(self):
        self._assert_gui_property_defined("dialogue_xpos")

    def test_dialogue_ypos(self):
        self._assert_gui_property_defined("dialogue_ypos")

    def test_dialogue_width(self):
        self._assert_gui_property_defined("dialogue_width")

    def test_dialogue_text_xalign(self):
        self._assert_gui_property_defined("dialogue_text_xalign")

    # Navigation and spacing
    def test_navigation_xpos(self):
        self._assert_gui_property_defined("navigation_xpos")

    def test_navigation_spacing(self):
        self._assert_gui_property_defined("navigation_spacing")

    def test_pref_spacing(self):
        self._assert_gui_property_defined("pref_spacing")

    def test_pref_button_spacing(self):
        self._assert_gui_property_defined("pref_button_spacing")

    def test_choice_spacing(self):
        self._assert_gui_property_defined("choice_spacing")

    def test_page_spacing(self):
        self._assert_gui_property_defined("page_spacing")

    def test_slot_spacing(self):
        self._assert_gui_property_defined("slot_spacing")

    # History properties
    def test_history_height(self):
        self._assert_gui_property_defined("history_height")

    def test_history_name_xpos(self):
        self._assert_gui_property_defined("history_name_xpos")

    def test_history_name_ypos(self):
        self._assert_gui_property_defined("history_name_ypos")

    def test_history_name_width(self):
        self._assert_gui_property_defined("history_name_width")

    def test_history_name_xalign(self):
        self._assert_gui_property_defined("history_name_xalign")

    def test_history_text_xpos(self):
        self._assert_gui_property_defined("history_text_xpos")

    def test_history_text_ypos(self):
        self._assert_gui_property_defined("history_text_ypos")

    def test_history_text_width(self):
        self._assert_gui_property_defined("history_text_width")

    def test_history_text_xalign(self):
        self._assert_gui_property_defined("history_text_xalign")

    # File slots
    def test_file_slot_cols(self):
        self._assert_gui_property_defined("file_slot_cols")

    def test_file_slot_rows(self):
        self._assert_gui_property_defined("file_slot_rows")


class TestGuiPropertyReferencesComplete(unittest.TestCase):
    """Exhaustively check every gui.* reference in screens.rpy has a definition."""

    def test_all_gui_references_are_defined(self):
        screens = read_file("screens.rpy")
        gui_content = read_file("gui.rpy")

        gui_methods = {
            "text_properties", "button_properties", "button_text_properties",
            "preference", "init", "history_allow_tags"
        }

        refs = re.findall(r'gui\.(\w+)', screens)
        property_refs = set(r for r in refs if r not in gui_methods)

        all_rpy = read_all_rpy_files()
        definitions = set()
        for content in all_rpy.values():
            definitions.update(re.findall(r'define\s+gui\.(\w+)\s*=', content))

        missing = property_refs - definitions
        self.assertEqual(
            missing, set(),
            f"gui properties referenced but never defined: "
            f"{', '.join(sorted('gui.' + m for m in missing))}"
        )


################################################################################
## Test 4: Image Assets
################################################################################


class TestImageAssets(unittest.TestCase):
    """Test that all image files referenced in screens exist on disk."""

    def test_textbox_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "textbox.png")))

    def test_frame_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "frame.png")))

    def test_namebox_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "namebox.png")))

    def test_nvl_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "nvl.png")))

    def test_skip_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "skip.png")))

    def test_notify_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "notify.png")))

    def test_main_menu_background(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "main_menu.png")))

    def test_game_menu_background(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "game_menu.png")))

    def test_overlay_main_menu(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "overlay", "main_menu.png")))

    def test_overlay_game_menu(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "overlay", "game_menu.png")))

    def test_overlay_confirm(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "overlay", "confirm.png")))

    def test_radio_button_foregrounds(self):
        for prefix in ["idle", "hover", "selected_idle", "selected_hover"]:
            path = os.path.join(GUI_DIR, "button", f"radio_{prefix}_foreground.png")
            self.assertTrue(os.path.isfile(path), f"gui/button/radio_{prefix}_foreground.png missing")

    def test_check_button_foregrounds(self):
        for prefix in ["idle", "hover", "selected_idle", "selected_hover"]:
            path = os.path.join(GUI_DIR, "button", f"check_{prefix}_foreground.png")
            self.assertTrue(os.path.isfile(path), f"gui/button/check_{prefix}_foreground.png missing")


class TestBarScrollbarSliderImages(unittest.TestCase):
    """Test that all bar, scrollbar, and slider images exist."""

    def test_bar_left_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "bar", "left.png")))

    def test_bar_right_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "bar", "right.png")))

    def test_bar_top_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "bar", "top.png")))

    def test_bar_bottom_png(self):
        self.assertTrue(os.path.isfile(os.path.join(GUI_DIR, "bar", "bottom.png")))

    def test_horizontal_scrollbar_images(self):
        for state in ["idle", "hover"]:
            for part in ["bar", "thumb"]:
                path = os.path.join(GUI_DIR, "scrollbar", f"horizontal_{state}_{part}.png")
                self.assertTrue(
                    os.path.isfile(path),
                    f"gui/scrollbar/horizontal_{state}_{part}.png missing"
                )

    def test_vertical_scrollbar_images(self):
        for state in ["idle", "hover"]:
            for part in ["bar", "thumb"]:
                path = os.path.join(GUI_DIR, "scrollbar", f"vertical_{state}_{part}.png")
                self.assertTrue(
                    os.path.isfile(path),
                    f"gui/scrollbar/vertical_{state}_{part}.png missing"
                )

    def test_horizontal_slider_images(self):
        for state in ["idle", "hover"]:
            for part in ["bar", "thumb"]:
                path = os.path.join(GUI_DIR, "slider", f"horizontal_{state}_{part}.png")
                self.assertTrue(
                    os.path.isfile(path),
                    f"gui/slider/horizontal_{state}_{part}.png missing"
                )

    def test_vertical_slider_images(self):
        for state in ["idle", "hover"]:
            for part in ["bar", "thumb"]:
                path = os.path.join(GUI_DIR, "slider", f"vertical_{state}_{part}.png")
                self.assertTrue(
                    os.path.isfile(path),
                    f"gui/slider/vertical_{state}_{part}.png missing"
                )

    def test_all_image_files_are_valid_pngs(self):
        """Verify every PNG in gui/ starts with the PNG signature."""
        png_sig = b'\x89PNG\r\n\x1a\n'
        for dirpath, _dirs, files in os.walk(GUI_DIR):
            for fname in files:
                if fname.endswith(".png"):
                    fpath = os.path.join(dirpath, fname)
                    with open(fpath, "rb") as f:
                        header = f.read(8)
                    rel = os.path.relpath(fpath, GAME_DIR)
                    self.assertEqual(
                        header, png_sig,
                        f"{rel} is not a valid PNG file (bad signature)"
                    )


################################################################################
## Test 5: Label Integrity
################################################################################


class TestLabelIntegrity(unittest.TestCase):
    """Test that all jump/call targets reference existing labels."""

    @classmethod
    def setUpClass(cls):
        cls.all_content = ""
        cls.files = read_all_rpy_files()
        for content in cls.files.values():
            cls.all_content += content + "\n"

        cls.defined_labels = set(re.findall(r'^label\s+(\w+)\s*:', cls.all_content, re.MULTILINE))
        cls.jump_targets = set(re.findall(r'jump\s+(\w+)', cls.all_content))
        cls.call_targets = set(re.findall(r'^\s+call\s+(\w+)', cls.all_content, re.MULTILINE))
        cls.call_targets -= {"me", "after", "it", "the", "this", "that", "them"}

    def test_all_jump_targets_exist(self):
        missing = self.jump_targets - self.defined_labels
        self.assertEqual(
            missing, set(),
            f"Jump targets reference undefined labels: {', '.join(sorted(missing))}"
        )

    def test_all_call_targets_exist(self):
        missing = self.call_targets - self.defined_labels
        self.assertEqual(
            missing, set(),
            f"Call targets reference undefined labels: {', '.join(sorted(missing))}"
        )

    def test_start_label_exists(self):
        self.assertIn("start", self.defined_labels)

    def test_all_chapter_labels_exist(self):
        for label in ["chapter_1", "chapter_2", "chapter_3"]:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_all_path_labels_exist(self):
        for label in ["path_knowledge", "path_duty", "path_freedom", "path_power", "path_true"]:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_all_ending_labels_exist(self):
        for label in ["ending_scholar", "ending_guardian", "ending_liberator", "ending_shadow"]:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_convergence_labels_exist(self):
        for label in ["ch1_convergence", "ch2_convergence"]:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_branch_labels_exist(self):
        for label in ["ch1_library", "ch1_underground", "ch2_elara", "ch2_kael", "ch2_sirin"]:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_no_duplicate_label_definitions(self):
        """Labels should not be defined more than once."""
        all_labels = []
        for fname, content in self.files.items():
            labels = re.findall(r'^label\s+(\w+)\s*:', content, re.MULTILINE)
            for label in labels:
                all_labels.append((label, fname))

        seen = {}
        duplicates = []
        for label, fname in all_labels:
            if label in seen:
                duplicates.append(f"'{label}' in both {seen[label]} and {fname}")
            seen[label] = fname

        self.assertEqual(duplicates, [], f"Duplicate labels: {'; '.join(duplicates)}")


################################################################################
## Test 6: Screen Definitions
################################################################################


class TestScreenDefinitions(unittest.TestCase):
    """Test that all screens referenced in the code are defined."""

    @classmethod
    def setUpClass(cls):
        cls.files = read_all_rpy_files()
        cls.all_content = "\n".join(cls.files.values())

        cls.defined_screens = set(
            re.findall(r'^screen\s+(\w+)', cls.all_content, re.MULTILINE)
        )
        cls.showmenu_refs = set(
            re.findall(r'ShowMenu\([\'"](\w+)[\'"]\)', cls.all_content)
        )
        cls.use_refs = set(
            re.findall(r'^\s+use\s+(\w+)', cls.all_content, re.MULTILINE)
        )
        cls.use_refs -= {"it", "the", "this", "that", "them"}

    def test_required_screens_exist(self):
        required = [
            "say", "input", "choice", "quick_menu", "navigation",
            "main_menu", "game_menu", "about", "save", "load",
            "file_slots", "preferences", "history", "help",
            "keyboard_help", "mouse_help", "confirm", "skip_indicator",
            "notify", "nvl", "ending_gallery"
        ]
        for screen in required:
            self.assertIn(screen, self.defined_screens, f"Screen '{screen}' not defined")

    def test_showmenu_targets_exist(self):
        for target in self.showmenu_refs:
            self.assertIn(target, self.defined_screens, f"ShowMenu('{target}') -> undefined screen")

    def test_use_targets_exist(self):
        for target in self.use_refs:
            self.assertIn(target, self.defined_screens, f"'use {target}' -> undefined screen")


################################################################################
## Test 7: Character Definitions
################################################################################


class TestCharacterDefinitions(unittest.TestCase):
    """Test that all character definitions are valid."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")

    def test_all_characters_defined(self):
        for char in ["mc", "elara", "kael", "sirin", "vesper", "narrator", "unknown"]:
            self.assertRegex(
                self.script, rf'define\s+{char}\s*=',
                f"Character '{char}' is not defined"
            )

    def test_narrator_is_not_nvl(self):
        """Narrator should NOT be NVL mode (no nvl clear in script)."""
        narrator_match = re.search(r'define\s+narrator\s*=\s*Character\(([^)]+)\)', self.script)
        self.assertIsNotNone(narrator_match)
        self.assertNotIn("nvl", narrator_match.group(1))

    def test_characters_used_in_dialogue_are_defined(self):
        """Every character tag used in dialogue should be defined."""
        dialogue_chars = set(re.findall(r'^    (\w+)\s+"', self.script, re.MULTILINE))
        renpy_keywords = {
            "if", "else", "elif", "for", "while", "return", "jump", "call",
            "scene", "show", "hide", "with", "play", "stop", "define",
            "default", "label", "menu", "python", "style", "screen", "text"
        }
        dialogue_chars -= renpy_keywords

        defined_chars = set(re.findall(r'define\s+(\w+)\s*=\s*Character', self.script))
        undefined = dialogue_chars - defined_chars
        self.assertEqual(undefined, set(), f"Undefined characters in dialogue: {sorted(undefined)}")


################################################################################
## Test 8: Game Flow Completeness
################################################################################


class TestGameFlowCompleteness(unittest.TestCase):
    """Test that game flow is complete and all paths reach endings."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")

    def test_start_leads_to_chapter_1(self):
        start_section = self.script[self.script.index("label start:"):]
        self.assertIn("jump chapter_1", start_section[:start_section.index("label chapter_1:")])

    def test_chapter_1_has_two_choices(self):
        ch1 = self.script[self.script.index("label chapter_1:"):]
        ch1 = ch1[:ch1.index("label ch1_library:")]
        self.assertIn("jump ch1_library", ch1)
        self.assertIn("jump ch1_underground", ch1)

    def test_chapter_1_branches_converge(self):
        library = self.script[self.script.index("label ch1_library:"):]
        library = library[:library.index("label ch1_underground:")]
        self.assertIn("jump ch1_convergence", library)

        underground = self.script[self.script.index("label ch1_underground:"):]
        underground = underground[:underground.index("label ch1_convergence:")]
        self.assertIn("jump ch1_convergence", underground)

    def test_chapter_1_convergence_leads_to_chapter_2(self):
        convergence = self.script[self.script.index("label ch1_convergence:"):]
        convergence = convergence[:convergence.index("label chapter_2:")]
        self.assertIn("jump chapter_2", convergence)

    def test_chapter_2_has_three_choices(self):
        ch2 = self.script[self.script.index("label chapter_2:"):]
        ch2 = ch2[:ch2.index("label ch2_elara:")]
        self.assertIn("jump ch2_elara", ch2)
        self.assertIn("jump ch2_kael", ch2)
        self.assertIn("jump ch2_sirin", ch2)

    def test_chapter_2_branches_converge(self):
        for branch in ["ch2_elara", "ch2_kael", "ch2_sirin"]:
            section_start = self.script.index(f"label {branch}:")
            remaining = self.script[section_start:]
            lines = remaining.split("\n")
            branch_text = ""
            for i, line in enumerate(lines):
                if i > 0 and re.match(r'^label\s+\w+:', line):
                    break
                branch_text += line + "\n"
            self.assertIn(
                "jump ch2_convergence", branch_text,
                f"Branch '{branch}' does not converge"
            )

    def test_chapter_2_convergence_leads_to_chapter_3(self):
        convergence = self.script[self.script.index("label ch2_convergence:"):]
        convergence = convergence[:convergence.index("label chapter_3:")]
        self.assertIn("jump chapter_3", convergence)

    def test_chapter_3_has_all_path_choices(self):
        ch3 = self.script[self.script.index("label chapter_3:"):]
        ch3 = ch3[:ch3.index("label path_knowledge:")]
        self.assertIn("jump path_knowledge", ch3)
        self.assertIn("jump path_duty", ch3)
        self.assertIn("jump path_freedom", ch3)
        self.assertIn("jump path_power", ch3)
        self.assertIn("jump path_true", ch3)

    def test_each_path_leads_to_ending(self):
        path_ending_map = {
            "path_knowledge": "ending_scholar",
            "path_duty": "ending_guardian",
            "path_freedom": "ending_liberator",
            "path_power": "ending_shadow",
        }
        for path, ending in path_ending_map.items():
            section_start = self.script.index(f"label {path}:")
            remaining = self.script[section_start:]
            next_label_match = re.search(r'\nlabel (?!{})\w+:'.format(ending), remaining[1:])
            if next_label_match:
                section = remaining[:next_label_match.start() + 1]
            else:
                section = remaining
            self.assertIn(f"jump {ending}", section, f"Path '{path}' -> missing ending '{ending}'")

    def test_all_endings_have_return(self):
        for ending in ["ending_scholar", "ending_guardian", "ending_liberator", "ending_shadow"]:
            section_start = self.script.index(f"label {ending}:")
            remaining = self.script[section_start:]
            next_match = re.search(r'\nlabel \w+:', remaining[1:])
            section = remaining[:next_match.start() + 1] if next_match else remaining
            self.assertIn("return", section, f"Ending '{ending}' has no return")

    def test_true_ending_has_return(self):
        section = self.script[self.script.index("label path_true:"):]
        self.assertIn("return", section)

    def test_true_route_conditional_gate(self):
        ch3 = self.script[self.script.index("label chapter_3:"):]
        ch3 = ch3[:ch3.index("label path_knowledge:")]
        self.assertIn("if true_route", ch3)


################################################################################
## Test 9: Persistent Variables
################################################################################


class TestPersistentVariables(unittest.TestCase):
    """Test persistent variable handling is consistent."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")
        cls.screens = read_file("screens.rpy")

    def test_all_ending_flags_have_defaults(self):
        for ending in ["ending_scholar", "ending_guardian", "ending_liberator",
                        "ending_shadow", "ending_true"]:
            self.assertIn(
                f"default persistent.{ending} = False", self.script,
                f"persistent.{ending} default is missing"
            )

    def test_all_ending_flags_are_set_in_endings(self):
        for ending in ["ending_scholar", "ending_guardian", "ending_liberator", "ending_shadow"]:
            self.assertIn(f"persistent.{ending} = True", self.script)

    def test_true_ending_flag_is_set(self):
        self.assertIn("persistent.ending_true = True", self.script)

    def test_ending_gallery_references_all_endings(self):
        for ending in ["ending_scholar", "ending_guardian", "ending_liberator", "ending_shadow"]:
            self.assertIn(ending, self.screens, f"Gallery missing {ending}")

    def test_true_route_unlock_logic(self):
        self.assertIn("persistent.ending_scholar and persistent.ending_guardian", self.script)
        self.assertIn("persistent.ending_liberator and persistent.ending_shadow", self.script)


################################################################################
## Test 10: Game Variables
################################################################################


class TestGameVariables(unittest.TestCase):
    """Test that all game variables are properly initialized."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")

    def test_default_variables_exist(self):
        required = [
            "player_name", "trust_elara", "trust_kael", "trust_sirin",
            "knowledge", "duty", "freedom", "power", "true_route"
        ]
        for var in required:
            self.assertRegex(self.script, rf'default\s+{var}\s*=', f"Missing default for '{var}'")

    def test_player_name_has_default(self):
        self.assertIn('default player_name = "Aiden"', self.script)


################################################################################
## Test 11: Transform Definitions
################################################################################


class TestTransformDefinitions(unittest.TestCase):
    """Test that all transforms used in screens and script are defined."""

    @classmethod
    def setUpClass(cls):
        cls.screens = read_file("screens.rpy")
        cls.script = read_file("script.rpy")

    def test_delayed_blink_defined(self):
        self.assertIn("transform delayed_blink", self.screens)

    def test_notify_appear_defined(self):
        self.assertIn("transform notify_appear", self.screens)

    def test_script_transitions_defined(self):
        for transition in ["flash", "slow_dissolve", "fade_to_black"]:
            self.assertRegex(self.script, rf'define\s+{transition}\s*=')


################################################################################
## Test 12: Ren'Py Syntax
################################################################################


class TestRenpySyntax(unittest.TestCase):
    """Test for common Ren'Py syntax issues."""

    @classmethod
    def setUpClass(cls):
        cls.files = read_all_rpy_files()

    def test_menu_choices_have_jumps(self):
        """Verify all menu blocks contain at least one jump."""
        for fname, content in self.files.items():
            blocks = content.split("\n    menu:\n")
            for i, block in enumerate(blocks[1:], 1):
                # Get text until the next non-indented line
                menu_text = ""
                for line in block.split("\n"):
                    if line and not line.startswith("    ") and not line.startswith("\t"):
                        break
                    menu_text += line + "\n"
                self.assertIn(
                    "jump", menu_text,
                    f"Menu block #{i} in {fname} has no jump statement"
                )


################################################################################
## Test 13: Options Configuration
################################################################################


class TestOptionsConfiguration(unittest.TestCase):
    """Test that options.rpy has all required configurations."""

    @classmethod
    def setUpClass(cls):
        cls.options = read_file("options.rpy")

    def test_config_name_set(self):
        self.assertIn("config.name", self.options)

    def test_config_version_set(self):
        self.assertIn("config.version", self.options)

    def test_config_save_directory_set(self):
        self.assertIn("config.save_directory", self.options)

    def test_transitions_defined(self):
        self.assertIn("config.enter_transition", self.options)
        self.assertIn("config.exit_transition", self.options)

    def test_window_config_set(self):
        self.assertIn('config.window = "auto"', self.options)

    def test_text_speed_default(self):
        self.assertIn("preferences.text_cps", self.options)

    def test_auto_forward_default(self):
        self.assertIn("preferences.afm_time", self.options)


################################################################################
## Test 14: End-to-End Path Simulation
################################################################################


class TestEndToEndPaths(unittest.TestCase):
    """Simulate walking through each game path to verify completeness."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")
        cls.labels = {}
        label_starts = [
            (m.start(), m.group(1))
            for m in re.finditer(r'^label\s+(\w+)\s*:', cls.script, re.MULTILINE)
        ]
        for i, (start, name) in enumerate(label_starts):
            end = label_starts[i + 1][0] if i + 1 < len(label_starts) else len(cls.script)
            cls.labels[name] = cls.script[start:end]

    def _walk_path(self, start_label, choices):
        """Simulate walking from start_label, making specified choices."""
        visited = [start_label]
        current = start_label
        choice_idx = 0
        max_steps = 50

        for _ in range(max_steps):
            if current not in self.labels:
                return visited, False, f"Label '{current}' not found"

            content = self.labels[current]
            has_return = bool(re.search(r'^\s+return\s*$', content, re.MULTILINE))
            jumps = re.findall(r'jump\s+(\w+)', content)

            if not jumps:
                return visited, has_return, None

            if "menu:" in content and choice_idx < len(choices):
                current = choices[choice_idx]
                choice_idx += 1
            else:
                current = jumps[-1]

            visited.append(current)

        return visited, False, "Max steps exceeded"

    def test_path_scholar(self):
        visited, has_return, error = self._walk_path("start", [
            "chapter_1", "ch1_library", "ch1_convergence",
            "chapter_2", "ch2_elara", "ch2_convergence",
            "chapter_3", "path_knowledge", "ending_scholar"
        ])
        self.assertIsNone(error, f"Error: {error}")
        self.assertIn("ending_scholar", visited)

    def test_path_guardian(self):
        visited, has_return, error = self._walk_path("start", [
            "chapter_1", "ch1_underground", "ch1_convergence",
            "chapter_2", "ch2_kael", "ch2_convergence",
            "chapter_3", "path_duty", "ending_guardian"
        ])
        self.assertIsNone(error, f"Error: {error}")
        self.assertIn("ending_guardian", visited)

    def test_path_liberator(self):
        visited, has_return, error = self._walk_path("start", [
            "chapter_1", "ch1_library", "ch1_convergence",
            "chapter_2", "ch2_sirin", "ch2_convergence",
            "chapter_3", "path_freedom", "ending_liberator"
        ])
        self.assertIsNone(error, f"Error: {error}")
        self.assertIn("ending_liberator", visited)

    def test_path_shadow(self):
        visited, has_return, error = self._walk_path("start", [
            "chapter_1", "ch1_underground", "ch1_convergence",
            "chapter_2", "ch2_kael", "ch2_convergence",
            "chapter_3", "path_power", "ending_shadow"
        ])
        self.assertIsNone(error, f"Error: {error}")
        self.assertIn("ending_shadow", visited)

    def test_true_ending_path_exists(self):
        self.assertIn("path_true", self.labels)
        content = self.labels["path_true"]
        self.assertIn("return", content)
        self.assertIn("persistent.ending_true = True", content)


################################################################################
## Test 15: Story Graph Integrity
################################################################################


class TestStoryGraphIntegrity(unittest.TestCase):
    """Validate the story graph is structurally complete."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")
        cls.labels = {}
        cls.transitions = {}

        label_starts = [
            (m.start(), m.group(1))
            for m in re.finditer(r'^label\s+(\w+)\s*:', cls.script, re.MULTILINE)
        ]
        for i, (start, name) in enumerate(label_starts):
            end = label_starts[i + 1][0] if i + 1 < len(label_starts) else len(cls.script)
            block = cls.script[start:end]
            cls.labels[name] = block
            cls.transitions[name] = set(re.findall(r'jump\s+(\w+)', block))

    def test_all_endings_reachable_from_start(self):
        required_endings = {
            "ending_scholar", "ending_guardian",
            "ending_liberator", "ending_shadow", "path_true",
        }
        visited = set()
        stack = ["start"]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            stack.extend(self.transitions.get(current, set()) - visited)

        missing = required_endings - visited
        self.assertEqual(missing, set(), f"Unreachable endings: {sorted(missing)}")

    def test_no_dead_end_labels(self):
        for label, content in self.labels.items():
            has_jump = bool(re.search(r'\bjump\s+\w+', content))
            has_return = bool(re.search(r'^\s+return\s*$', content, re.MULTILINE))
            self.assertTrue(
                has_jump or has_return,
                f"Label '{label}' is a dead end (no jump or return)"
            )

    def test_true_route_choice_is_conditionally_gated(self):
        ch3_start = self.script.index("label chapter_3:")
        ch3_end = self.script.index("label path_knowledge:")
        ch3 = self.script[ch3_start:ch3_end]
        self.assertIn(
            '"The hidden path — Step onto the glowing circle." if true_route:',
            ch3,
            "True route choice must be gated with `if true_route`"
        )


################################################################################
## Test 16: Style Consistency
################################################################################


class TestStyleConsistency(unittest.TestCase):
    """Test for style definition consistency and correctness."""

    @classmethod
    def setUpClass(cls):
        cls.screens = read_file("screens.rpy")

    def test_show_name_defined(self):
        """gui.show_name should be defined."""
        all_rpy = read_all_rpy_files()
        all_content = "\n".join(all_rpy.values())
        self.assertIn("gui.show_name", all_content)

    def test_no_style_inherits_from_undefined_custom_parent(self):
        """Styles inheriting from 'is X' should reference known styles.

        Ren'Py built-in gui_ styles are: gui_text, gui_button, gui_button_text,
        gui_label, gui_label_text, gui_frame, gui_prompt, gui_prompt_text,
        gui_medium_button, gui_medium_button_text, gui_bar, gui_vbar,
        gui_scrollbar, gui_vscrollbar, gui_slider, gui_vslider, gui_viewport,
        gui_side. These are valid parents for NON-base styles.
        """
        # Extract all "style X is Y" patterns
        inheritance_patterns = re.findall(
            r'^style\s+(\w+)\s+(?:is\s+)?(\w+)\s*(?::|\s*$)',
            self.screens, re.MULTILINE
        )
        # We're specifically checking that no base widget style inherits from itself
        # via a gui_ variant, which was the original bug
        base_styles = {"bar", "vbar", "scrollbar", "vscrollbar", "slider", "vslider"}
        for child, parent in inheritance_patterns:
            if child in base_styles:
                self.assertNotEqual(
                    parent, f"gui_{child}",
                    f"CRITICAL: style {child} is {parent} creates circular inheritance!"
                )

    def test_slider_bar_styles_defined(self):
        """The slider and vslider styles should be defined."""
        self.assertIn("style slider bar:", self.screens)
        self.assertIn("style vslider vbar:", self.screens)


################################################################################
## Test 17: Comprehensive Image Reference Check
################################################################################


class TestAllImageReferences(unittest.TestCase):
    """Verify every image path referenced in .rpy files exists on disk."""

    def test_all_static_image_paths_exist(self):
        """Check all literal image paths (non-interpolated) in .rpy files."""
        all_rpy = read_all_rpy_files()
        all_content = "\n".join(all_rpy.values())

        # Find all string image references that don't contain [prefix_] interpolation
        image_refs = re.findall(r'"(gui/[^"]*\.png)"', all_content)
        static_refs = [ref for ref in image_refs if "[" not in ref]

        for ref in static_refs:
            path = os.path.join(GAME_DIR, ref)
            self.assertTrue(
                os.path.isfile(path),
                f"Image referenced in .rpy files does not exist: {ref}"
            )

    def test_all_interpolated_image_paths_exist(self):
        """Check that interpolated image paths (with [prefix_]) have idle/hover variants."""
        all_rpy = read_all_rpy_files()
        all_content = "\n".join(all_rpy.values())

        # Find all [prefix_] interpolated image references
        interp_refs = re.findall(r'"(gui/[^"]*\[prefix_\][^"]*\.png)"', all_content)

        for ref in interp_refs:
            for prefix in ["idle_", "hover_"]:
                resolved = ref.replace("[prefix_]", prefix)
                path = os.path.join(GAME_DIR, resolved)
                self.assertTrue(
                    os.path.isfile(path),
                    f"Interpolated image missing: {resolved} (from {ref})"
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
