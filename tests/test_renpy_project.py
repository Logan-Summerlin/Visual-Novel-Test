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
        """The slider and vslider styles should be defined without deprecated bar/vbar variant syntax.

        In Ren'Py 8.5+, 'style slider bar:' raises 'style property bar is not known'.
        The correct form is simply 'style slider:' and 'style vslider:'.
        """
        # Must NOT use deprecated variant syntax that crashes Ren'Py 8.5+
        self.assertNotIn(
            "style slider bar:",
            self.screens,
            "CRITICAL: 'style slider bar:' is invalid in Ren'Py 8.5+ and causes a crash. "
            "Use 'style slider:' instead."
        )
        self.assertNotIn(
            "style vslider vbar:",
            self.screens,
            "CRITICAL: 'style vslider vbar:' is invalid in Ren'Py 8.5+ and causes a crash. "
            "Use 'style vslider:' instead."
        )
        # Must have the correct plain style definitions
        # Use re.search with MULTILINE so ^ matches line-starts inside the file
        self.assertIsNotNone(
            re.search(r'^style slider:', self.screens, re.MULTILINE),
            "style slider: must be defined (without 'bar' variant keyword)"
        )
        self.assertIsNotNone(
            re.search(r'^style vslider:', self.screens, re.MULTILINE),
            "style vslider: must be defined (without 'vbar' variant keyword)"
        )

    def test_no_conflicting_style_inheritance(self):
        """No style should be defined twice with different parents.

        For example, 'style choice_button is button' followed by
        'style choice_button is default:' would silently override the parent.
        """
        # Find all "style X is Y" declarations
        pattern = r'^style\s+(\w+)\s+is\s+(\w+)'
        declarations = re.findall(pattern, self.screens, re.MULTILINE)

        # Group by style name
        style_parents = {}
        conflicts = []
        for style_name, parent in declarations:
            if style_name in style_parents:
                if style_parents[style_name] != parent:
                    conflicts.append(
                        f"style {style_name}: first 'is {style_parents[style_name]}', "
                        f"then 'is {parent}'"
                    )
            else:
                style_parents[style_name] = parent

        self.assertEqual(
            conflicts, [],
            f"Conflicting style inheritance: {'; '.join(conflicts)}"
        )


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


################################################################################
## Test 18: Ren'Py Version-Specific Style Syntax
################################################################################


class TestRenpyVersionCompatibility(unittest.TestCase):
    """Test for syntax that changed between Ren'Py versions and causes crashes."""

    @classmethod
    def setUpClass(cls):
        cls.screens = read_file("screens.rpy")

    def test_no_deprecated_bar_variant_syntax(self):
        """Ren'Py 8.5+ rejects 'style X bar:' and 'style X vbar:' as unknown properties.

        The multi-style variant syntax (style slider bar:, style vslider vbar:) was
        removed in Ren'Py 8.5.  Plain 'style slider:' and 'style vslider:' must be
        used instead.
        """
        deprecated_patterns = [
            (r'^style\s+\w+\s+bar\s*:', "style X bar:"),
            (r'^style\s+\w+\s+vbar\s*:', "style X vbar:"),
        ]
        for pattern, description in deprecated_patterns:
            self.assertNotRegex(
                self.screens,
                pattern,
                f"Deprecated Ren'Py 7.x syntax '{description}' found in screens.rpy. "
                f"This causes 'style property X is not known' in Ren'Py 8.5+."
            )

    def test_slider_styles_use_correct_syntax(self):
        """slider and vslider must be defined as plain styles, not bar variants."""
        # Use re.search with MULTILINE so ^ matches line starts within the file
        self.assertIsNotNone(
            re.search(r'^style slider:\s*$', self.screens, re.MULTILINE),
            "style slider: must be defined as a simple colon definition (no 'bar' variant keyword)"
        )
        self.assertIsNotNone(
            re.search(r'^style vslider:\s*$', self.screens, re.MULTILINE),
            "style vslider: must be defined as a simple colon definition (no 'vbar' variant keyword)"
        )

    def test_slider_has_required_properties(self):
        """slider style must have base_bar and thumb properties."""
        match = re.search(
            r'^style slider:(.*?)(?=^style |\Z)',
            self.screens, re.MULTILINE | re.DOTALL
        )
        self.assertIsNotNone(match, "style slider: block not found")
        block = match.group(1)
        self.assertIn("base_bar", block, "style slider: must define base_bar")
        self.assertIn("thumb", block, "style slider: must define thumb")

    def test_vslider_has_required_properties(self):
        """vslider style must have base_bar and thumb properties."""
        match = re.search(
            r'^style vslider:(.*?)(?=^style |\Z)',
            self.screens, re.MULTILINE | re.DOTALL
        )
        self.assertIsNotNone(match, "style vslider: block not found")
        block = match.group(1)
        self.assertIn("base_bar", block, "style vslider: must define base_bar")
        self.assertIn("thumb", block, "style vslider: must define thumb")


################################################################################
## Test 19: Text Interpolation Safety
################################################################################


class TestTextInterpolation(unittest.TestCase):
    """Test that [var] interpolations in screen text refer to defined variables.

    Ren'Py substitutes [VarName] in text strings at runtime.  If VarName is not
    defined in any accessible scope, the game crashes with NameError.  This is
    especially treacherous when the variable name is capitalised differently from
    the defined store variable (e.g. [Knowledge] vs. knowledge).
    """

    # Variables that are legitimately defined (case-insensitive list built from
    # store defaults and Ren'Py built-ins used in our project).
    KNOWN_VARIABLES = {
        # Store variables (script.rpy defaults)
        "player_name", "trust_elara", "trust_kael", "trust_sirin",
        "knowledge", "duty", "freedom", "power", "true_route",
        # Ren'Py built-ins commonly interpolated
        "renpy", "config", "gui", "persistent",
        # Local screen variables
        "count", "page", "eid", "ename", "etheme", "slot",
        "screen_name", "lang",
    }

    # Ren'Py special modifiers (e.g. [config.name!t], [renpy.version_only])
    MODIFIER_PATTERN = re.compile(r'\[([a-zA-Z_]\w*(?:\.\w+)*)(?:![a-z]+)?\]')

    @classmethod
    def setUpClass(cls):
        cls.files = read_all_rpy_files()

    def _extract_interpolations(self, text):
        """Return list of (var_root, full_ref) tuples from [var] patterns."""
        results = []
        for m in self.MODIFIER_PATTERN.finditer(text):
            full_ref = m.group(1)
            root = full_ref.split(".")[0]
            results.append((root, full_ref))
        return results

    def test_no_undefined_capitalised_variables_in_screen_text(self):
        """Screen text must not interpolate capitalised names that shadow lowercase vars.

        A common error is writing {color=#aaa}[Knowledge]{/color} when only
        'knowledge' (lowercase) is defined — this crashes at runtime.
        """
        screens = self.files.get("screens.rpy", "")
        # Split into text-display contexts: text "...", label "...", etc.
        # We look for any quoted string containing [XxxXxx] where Xxx is uppercase
        # and NOT a known Ren'Py built-in with capital letters.
        suspicious_pattern = re.compile(r'"([^"]*\[[A-Z][a-zA-Z_]*\][^"]*)"')
        for m in suspicious_pattern.finditer(screens):
            string_content = m.group(1)
            # Check every interpolation in this string
            for root, full_ref in self._extract_interpolations(string_content):
                # Capitalised root that isn't a known built-in namespace
                if root[0].isupper() and root.lower() not in self.KNOWN_VARIABLES:
                    self.fail(
                        f"Possible undefined variable in screen text: [{full_ref}] — "
                        f"'{root}' is capitalised but only '{root.lower()}' is defined. "
                        f"Escape with [[{root}] to display a literal bracket, or define "
                        f"the variable."
                    )

    def test_ending_gallery_theme_strings_are_escaped(self):
        """The ending gallery theme strings must not contain unescaped [Variable] refs.

        Previously: '{color=#88aaff}[Knowledge]{/color}' — crashes on unlocked endings.
        Fixed:       '{color=#88aaff}[[Knowledge]{/color}' — displays '[Knowledge]'.
        """
        screens = self.files.get("screens.rpy", "")
        bad_patterns = [
            r'"\{color=[^}]+\}\[Knowledge\]',
            r'"\{color=[^}]+\}\[Duty\]',
            r'"\{color=[^}]+\}\[Freedom\]',
            r'"\{color=[^}]+\}\[Power\]',
        ]
        for pattern in bad_patterns:
            self.assertNotRegex(
                screens, pattern,
                f"Unescaped capitalised variable interpolation found matching {pattern}. "
                "Use [[ to produce a literal '[' character."
            )

    def test_script_interpolations_use_defined_variables(self):
        """All [var] interpolations in script.rpy must reference defined store variables."""
        script = self.files.get("script.rpy", "")
        defined_vars = set(re.findall(r'default\s+(\w+)\s*=', script))
        defined_vars.update(self.KNOWN_VARIABLES)
        # Ren'Py built-in namespaces and special forms
        builtin_roots = {"renpy", "config", "gui", "persistent", "store",
                         "player_name", "_", "h", "d", "i"}

        for m in re.finditer(r'"([^"]*)"', script):
            string_val = m.group(1)
            for root, full_ref in self._extract_interpolations(string_val):
                if root in builtin_roots:
                    continue
                if root.startswith("_"):
                    continue
                self.assertIn(
                    root, defined_vars,
                    f"Interpolation [{full_ref}] in script.rpy — '{root}' not in store defaults. "
                    f"Defined vars: {sorted(defined_vars)}"
                )


################################################################################
## Test 20: No Tabs In .rpy Files (Issue #4)
################################################################################


class TestNoTabsInRpyFiles(unittest.TestCase):
    """Test that .rpy files use spaces, not tabs, for indentation.

    Mixing tabs and spaces causes IndentationError parse failures in Ren'Py.
    This catches Issue #4 from the common-issues log.
    """

    def test_no_tab_indentation(self):
        """No .rpy file should contain tab characters."""
        for fname, content in read_all_rpy_files().items():
            lines_with_tabs = [
                (lineno + 1, repr(line))
                for lineno, line in enumerate(content.split("\n"))
                if "\t" in line
            ]
            self.assertEqual(
                lines_with_tabs, [],
                f"{fname} contains tab characters (tabs break Ren'Py indentation):\n"
                + "\n".join(f"  line {ln}: {ln_repr}" for ln, ln_repr in lines_with_tabs[:5])
            )


################################################################################
## Test 21: Text Tag Balance (Issue #13)
################################################################################


class TestTextTagBalance(unittest.TestCase):
    """Verify that styled text tags are properly balanced in script and screens.

    Unbalanced {b}, {i}, {color}, {u}, {s} tags cause rendering exceptions that
    are hard to spot during authoring but crash the game at the affected line.
    """

    # Pairs: open-tag regex → close tag string
    TAG_PAIRS = [
        (re.compile(r'\{b\}'), "{/b}"),
        (re.compile(r'\{i\}'), "{/i}"),
        (re.compile(r'\{u\}'), "{/u}"),
        (re.compile(r'\{s\}'), "{/s}"),
        (re.compile(r'\{color=[^}]+\}'), "{/color}"),
        (re.compile(r'\{a=[^}]+\}'), "{/a}"),
        (re.compile(r'\{outlinecolor=[^}]+\}'), "{/outlinecolor}"),
    ]

    def _check_tags_balanced(self, content, filename):
        """Check that every open tag in a quoted string has a matching close tag."""
        # Extract all double-quoted strings
        for str_match in re.finditer(r'"((?:[^"\\]|\\.)*)"', content):
            s = str_match.group(1)
            for open_re, close_tag in self.TAG_PAIRS:
                opens = len(open_re.findall(s))
                closes = s.count(close_tag)
                if opens != closes:
                    self.fail(
                        f"{filename}: Unbalanced text tag in string near "
                        f"position {str_match.start()}: "
                        f"found {opens} open(s) but {closes} close(s) for "
                        f"'{close_tag}' in: {s[:120]!r}"
                    )

    def test_script_text_tags_balanced(self):
        self._check_tags_balanced(read_file("script.rpy"), "script.rpy")

    def test_screens_text_tags_balanced(self):
        self._check_tags_balanced(read_file("screens.rpy"), "screens.rpy")


################################################################################
## Test 22: No Forbidden OS-specific Python (Issue #43)
################################################################################


class TestNoForbiddenPythonModules(unittest.TestCase):
    """Check that .rpy files do not import OS-specific modules that break on web/mobile.

    subprocess, os.system, ctypes, winreg, etc. are unavailable on Android/iOS/web.
    Their presence causes import errors or runtime crashes on non-PC platforms.
    """

    FORBIDDEN_IMPORTS = [
        "import subprocess",
        "import ctypes",
        "import winreg",
        "import _winapi",
        "os.system(",
        "subprocess.run(",
        "subprocess.Popen(",
        "subprocess.call(",
    ]

    def test_no_forbidden_imports(self):
        for fname, content in read_all_rpy_files().items():
            for forbidden in self.FORBIDDEN_IMPORTS:
                self.assertNotIn(
                    forbidden, content,
                    f"{fname} uses '{forbidden}' which is unavailable on web/mobile platforms."
                )


################################################################################
## Test 23: Unbalanced String Quotes (Issue #3)
################################################################################


class TestStringQuoteBalance(unittest.TestCase):
    """Basic check for unbalanced double-quotes within dialogue lines.

    A single stray quote in a dialogue string causes a parse error that can
    appear on a completely different line, making it hard to debug.
    """

    def test_no_lone_unescaped_quote_in_dialogue(self):
        """Dialogue lines should not contain raw unescaped double-quotes inside strings.

        Ren'Py allows \" inside strings to display a literal quote character.
        We strip escaped quotes before counting so they don't produce false positives.
        """
        script = read_file("script.rpy")
        # Find lines that look like dialogue: <indent><char> "<text>"
        dialogue_line_re = re.compile(r'^\s+\w+\s+"(.*)"$', re.MULTILINE)
        for m in dialogue_line_re.finditer(script):
            full_line = m.group(0).rstrip()
            # Remove escaped \" sequences before counting to avoid false positives
            clean_line = full_line.replace('\\"', "XX")
            quote_count = clean_line.count('"')
            self.assertEqual(
                quote_count % 2, 0,
                f"Possible unbalanced quotes on line (after removing \\\"): "
                f"{full_line[:120]!r}"
            )


################################################################################
## Test 24: Persistent Variable Access Safety (Issue #32, #37)
################################################################################


class TestPersistentAccessSafety(unittest.TestCase):
    """Check that persistent attributes are accessed safely.

    Accessing persistent.some_attr directly without getattr() risks AttributeError
    if the attribute was added in a later version and a player has an old save.
    The ending_gallery screen should use getattr(..., False) for all persistent checks.
    """

    @classmethod
    def setUpClass(cls):
        cls.screens = read_file("screens.rpy")

    def test_ending_gallery_uses_getattr_for_persistent(self):
        """ending_gallery should use getattr(persistent, ..., False) for safety."""
        gallery_match = re.search(
            r'screen ending_gallery\(\):(.*?)(?=^screen |\Z)',
            self.screens, re.MULTILINE | re.DOTALL
        )
        self.assertIsNotNone(gallery_match, "ending_gallery screen not found")
        gallery = gallery_match.group(1)
        # The per-ending unlock checks should use getattr
        self.assertIn(
            "getattr(persistent,",
            gallery,
            "ending_gallery should use getattr(persistent, eid, False) for safe access"
        )

    def test_persistent_defaults_defined_before_use(self):
        """All persistent attributes used in conditionals must have defaults.

        Direct reads of persistent.X in if/and/or expressions without a
        'default persistent.X = ...' will raise AttributeError on a fresh install
        (before the attribute is ever set).
        """
        script = read_file("script.rpy")
        screens = read_file("screens.rpy")
        combined = script + screens

        # Collect every persistent.X attribute name referenced anywhere
        all_attrs = set(re.findall(r'persistent\.(\w+)', combined))

        # Collect every persistent.X that has a default declaration
        defaulted = set(re.findall(r'default\s+persistent\.(\w+)\s*=', script))

        # Check: any attr used in a conditional that lacks a default is risky
        risky = set()
        for attr in all_attrs:
            if attr in defaulted:
                continue  # safe — has a default
            # Check whether this attr appears in a conditional context
            # (getattr() wraps are safe; direct if/and/or/not reads are not)
            cond_pattern = rf'(?:if|and|or|not)\b[^\n]*\bpersistent\.{re.escape(attr)}\b'
            if re.search(cond_pattern, combined):
                risky.add(attr)

        self.assertEqual(
            risky, set(),
            f"persistent attributes used in conditionals without defaults: "
            f"{sorted('persistent.' + a for a in risky)}"
        )


################################################################################
## Test 25: Save/Rollback Safety — Non-serialisable Store Values (Issue #37, #49)
################################################################################


class TestSaveLoadSafety(unittest.TestCase):
    """Check that store variables only hold serialisable, rollback-safe values.

    File handles, class instances with __slots__, and other non-picklable objects
    stored in the default store corrupt saves.  This test guards against the most
    common patterns.
    """

    DANGEROUS_PATTERNS = [
        (r'default\s+\w+\s*=\s*open\(', "open() file handle"),
        (r'default\s+\w+\s*=\s*threading\.', "threading object"),
        (r'define\s+\w+\s*=\s*open\(', "open() file handle in define"),
    ]

    def test_no_non_serialisable_defaults(self):
        for fname, content in read_all_rpy_files().items():
            for pattern, description in self.DANGEROUS_PATTERNS:
                self.assertNotRegex(
                    content, pattern,
                    f"{fname}: Found non-serialisable {description} in store variable. "
                    "This will corrupt saves."
                )

    def test_all_path_endings_set_persistent_flags(self):
        """Every non-true ending must set its persistent flag before return."""
        script = read_file("script.rpy")
        ending_flag_map = {
            "ending_scholar": "persistent.ending_scholar = True",
            "ending_guardian": "persistent.ending_guardian = True",
            "ending_liberator": "persistent.ending_liberator = True",
            "ending_shadow": "persistent.ending_shadow = True",
            "path_true": "persistent.ending_true = True",
        }
        for ending, flag_line in ending_flag_map.items():
            idx = script.find(f"label {ending}:")
            self.assertNotEqual(idx, -1, f"label {ending}: not found")
            # Find next label
            next_label = re.search(r'\nlabel \w+:', script[idx + 1:])
            section = script[idx: idx + 1 + (next_label.start() if next_label else len(script))]
            self.assertIn(
                flag_line, section,
                f"label {ending}: does not set {flag_line} before ending"
            )


################################################################################
## Test 26: Complete GUI Variable Coverage Audit
################################################################################


class TestGuiVariableCoverageAudit(unittest.TestCase):
    """Exhaustive audit: every gui.X property used anywhere must be defined somewhere.

    This extends Test 3 by scanning ALL .rpy files (not just screens.rpy) and
    checking against definitions in ALL .rpy files (not just gui.rpy).
    """

    # gui methods/callables and non-property identifiers that look like properties
    GUI_CALLABLES = frozenset({
        "text_properties", "button_properties", "button_text_properties",
        "preference", "init", "history_allow_tags",
        # File-extension matches: "gui.rpy", "gui.rpyc" etc. are filenames not properties
        "rpy", "rpyc", "rpyb",
    })

    def test_complete_gui_coverage(self):
        all_rpy = read_all_rpy_files()
        all_content = "\n".join(all_rpy.values())

        # Collect all gui.X references
        all_refs = set(re.findall(r'\bgui\.(\w+)', all_content))
        property_refs = all_refs - self.GUI_CALLABLES

        # Collect all definitions (define gui.X = ...)
        definitions = set(re.findall(r'define\s+gui\.(\w+)\s*=', all_content))

        missing = property_refs - definitions
        self.assertEqual(
            missing, set(),
            "gui properties referenced but never defined: "
            + ", ".join(sorted("gui." + m for m in missing))
        )


################################################################################
## Test 27: Config Variable Coverage Audit
################################################################################


class TestConfigVariableCoverageAudit(unittest.TestCase):
    """Every config.X used in screens/script must be defined or be a Ren'Py built-in."""

    # Ren'Py built-in config properties we reference but don't define ourselves
    RENPY_BUILTIN_CONFIG = frozenset({
        "has_autosave", "has_quicksave", "has_music", "has_sound",
        "thumbnail_width", "thumbnail_height",
    })

    def test_config_references_are_defined_or_builtin(self):
        all_rpy = read_all_rpy_files()
        all_content = "\n".join(all_rpy.values())

        refs = set(re.findall(r'\bconfig\.(\w+)', all_content))
        definitions = set(re.findall(r'define\s+config\.(\w+)\s*=', all_content))

        undefined = refs - definitions - self.RENPY_BUILTIN_CONFIG
        self.assertEqual(
            undefined, set(),
            "config properties referenced but not defined: "
            + ", ".join(sorted("config." + r for r in undefined))
        )


################################################################################
## Test 28: Ending Gallery Screen Safety
################################################################################


class TestEndingGalleryScreen(unittest.TestCase):
    """Detailed validation of the ending gallery screen."""

    @classmethod
    def setUpClass(cls):
        cls.screens = read_file("screens.rpy")
        # Extract the ending_gallery screen block
        m = re.search(
            r'^screen ending_gallery\(\):(.*?)(?=^screen |\Z)',
            cls.screens, re.MULTILINE | re.DOTALL
        )
        cls.gallery = m.group(1) if m else ""

    def test_gallery_screen_exists(self):
        self.assertNotEqual(self.gallery, "", "screen ending_gallery() not found")

    def test_all_four_endings_referenced_in_gallery(self):
        for ending in ["ending_scholar", "ending_guardian",
                       "ending_liberator", "ending_shadow"]:
            self.assertIn(ending, self.gallery, f"{ending} not referenced in gallery")

    def test_true_ending_slot_references_all_four(self):
        """True-ending slot must check that all 4 endings are discovered."""
        for ending in ["ending_scholar", "ending_guardian",
                       "ending_liberator", "ending_shadow"]:
            self.assertIn(
                f"persistent.{ending}", self.gallery,
                f"True ending check in gallery missing persistent.{ending}"
            )

    def test_no_bare_capital_interpolation_in_gallery(self):
        """Gallery must not contain unescaped [Capital] interpolations that crash on unlock.

        Ren'Py escapes a literal '[' with '[['.  An un-escaped '[Capital]' pattern
        causes a NameError at runtime because Ren'Py tries to substitute a variable
        named Capital that doesn't exist.  The negative lookbehind (?<!\\[) skips
        properly-escaped '[[Capital]' occurrences.
        """
        # (?<!\[) ensures we don't flag the second [ of a correctly escaped [[
        bad = re.findall(r'(?<!\[)\[(?!prefix_)[A-Z][a-zA-Z]*\]', self.gallery)
        self.assertEqual(
            bad, [],
            f"Unescaped capital-letter interpolations in ending_gallery: {bad}. "
            "These cause NameError at runtime when an ending is unlocked. "
            "Use [[ to display a literal '[' character."
        )

    def test_ending_count_variable_defined_before_use(self):
        """The [count] interpolation must be preceded by '$ count = ...'."""
        if "[count]" in self.gallery:
            # Find [count] usage
            count_idx = self.gallery.index("[count]")
            before = self.gallery[:count_idx]
            self.assertIn(
                "$ count =", before,
                "[count] used in ending_gallery but '$ count = ...' not found before it"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
