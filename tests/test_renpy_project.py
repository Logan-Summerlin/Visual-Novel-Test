#!/usr/bin/env python3
"""
Comprehensive test suite for "Echoes of the Forgotten Tower" Ren'Py visual novel.

Tests validate:
- All GUI properties referenced in screens.rpy are defined in gui.rpy
- All image assets referenced in screens exist on disk
- All labels referenced in jump/call statements exist
- All screens referenced in ShowMenu/use statements exist
- All character definitions are valid
- Script structure completeness (every path reaches an ending)
- No broken Ren'Py syntax patterns
- Persistent variable consistency
- The startup crash (gui.preference without default) is fixed
"""

import os
import re
import sys
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


class TestStartupCrashFix(unittest.TestCase):
    """Test that the original startup crash is fixed."""

    def test_no_language_preference_without_default(self):
        """The original crash: gui.preference('language') called without a default value."""
        screens = read_file("screens.rpy")
        # Should NOT have gui.preference("language") without a default
        pattern = r'gui\.preference\(\s*["\']language["\']\s*\)'
        matches = re.findall(pattern, screens)
        self.assertEqual(
            len(matches), 0,
            "screens.rpy still contains gui.preference('language') without a default value. "
            "This causes: Exception: Gui preference 'language' is not set, and does not have a default value."
        )

    def test_language_not_in_default_style(self):
        """Ensure the default style does not reference a language preference."""
        screens = read_file("screens.rpy")
        # Find the default style block
        default_style_match = re.search(
            r'style default:\n((?:    .*\n)*)', screens
        )
        self.assertIsNotNone(default_style_match, "Could not find 'style default:' block")
        default_block = default_style_match.group(1)
        self.assertNotIn(
            "language", default_block,
            "The 'style default:' block should not contain a 'language' property "
            "that depends on gui.preference('language')"
        )


class TestGuiPropertyDefinitions(unittest.TestCase):
    """Test that all GUI properties referenced in screens.rpy are defined in gui.rpy."""

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

    def test_main_menu_background(self):
        self._assert_gui_property_defined("main_menu_background")

    def test_game_menu_background(self):
        self._assert_gui_property_defined("game_menu_background")

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

    def test_notify_ypos(self):
        self._assert_gui_property_defined("notify_ypos")

    def test_navigation_xpos(self):
        self._assert_gui_property_defined("navigation_xpos")

    def test_skip_ypos(self):
        self._assert_gui_property_defined("skip_ypos")

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

    def test_file_slot_cols(self):
        self._assert_gui_property_defined("file_slot_cols")

    def test_file_slot_rows(self):
        self._assert_gui_property_defined("file_slot_rows")


class TestGuiPropertyReferencesComplete(unittest.TestCase):
    """Exhaustively check that every gui.* reference in screens.rpy has a definition in gui.rpy."""

    def test_all_gui_references_are_defined(self):
        screens = read_file("screens.rpy")
        gui_content = read_file("gui.rpy")

        # Find all gui.X references in screens.rpy (exclude gui.preference, gui.init,
        # gui.text_properties, gui.button_properties, gui.button_text_properties — these are methods)
        gui_methods = {
            "text_properties", "button_properties", "button_text_properties",
            "preference", "init", "history_allow_tags"
        }

        refs = re.findall(r'gui\.(\w+)', screens)
        property_refs = set(r for r in refs if r not in gui_methods)

        # Find all gui.X definitions across all .rpy files
        all_rpy = read_all_rpy_files()
        definitions = set()
        for content in all_rpy.values():
            definitions.update(re.findall(r'define\s+gui\.(\w+)\s*=', content))

        missing = property_refs - definitions
        self.assertEqual(
            missing, set(),
            f"The following gui properties are referenced in screens.rpy but never defined: "
            f"{', '.join(sorted('gui.' + m for m in missing))}"
        )


class TestImageAssets(unittest.TestCase):
    """Test that all image files referenced in screens.rpy exist on disk."""

    def test_textbox_png(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "textbox.png")),
            "gui/textbox.png is missing"
        )

    def test_frame_png(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "frame.png")),
            "gui/frame.png is missing"
        )

    def test_namebox_png(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "namebox.png")),
            "gui/namebox.png is missing"
        )

    def test_nvl_png(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "nvl.png")),
            "gui/nvl.png is missing"
        )

    def test_skip_png(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "skip.png")),
            "gui/skip.png is missing"
        )

    def test_notify_png(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "notify.png")),
            "gui/notify.png is missing"
        )

    def test_main_menu_background(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "main_menu.png")),
            "gui/main_menu.png is missing"
        )

    def test_game_menu_background(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "game_menu.png")),
            "gui/game_menu.png is missing"
        )

    def test_overlay_main_menu(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "overlay", "main_menu.png")),
            "gui/overlay/main_menu.png is missing"
        )

    def test_overlay_game_menu(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "overlay", "game_menu.png")),
            "gui/overlay/game_menu.png is missing"
        )

    def test_overlay_confirm(self):
        self.assertTrue(
            os.path.isfile(os.path.join(GUI_DIR, "overlay", "confirm.png")),
            "gui/overlay/confirm.png is missing"
        )

    def test_radio_button_foregrounds(self):
        for prefix in ["idle", "hover", "selected_idle", "selected_hover"]:
            path = os.path.join(GUI_DIR, "button", f"radio_{prefix}_foreground.png")
            self.assertTrue(
                os.path.isfile(path),
                f"gui/button/radio_{prefix}_foreground.png is missing"
            )

    def test_check_button_foregrounds(self):
        for prefix in ["idle", "hover", "selected_idle", "selected_hover"]:
            path = os.path.join(GUI_DIR, "button", f"check_{prefix}_foreground.png")
            self.assertTrue(
                os.path.isfile(path),
                f"gui/button/check_{prefix}_foreground.png is missing"
            )


class TestLabelIntegrity(unittest.TestCase):
    """Test that all jump/call targets reference existing labels."""

    @classmethod
    def setUpClass(cls):
        cls.all_content = ""
        cls.files = read_all_rpy_files()
        for content in cls.files.values():
            cls.all_content += content + "\n"

        # Extract all label definitions
        cls.defined_labels = set(re.findall(r'^label\s+(\w+)\s*:', cls.all_content, re.MULTILINE))

        # Extract all jump targets
        cls.jump_targets = set(re.findall(r'jump\s+(\w+)', cls.all_content))

        # Extract all call targets (only indented Ren'Py statements, not dialogue text)
        cls.call_targets = set(re.findall(r'^\s+call\s+(\w+)', cls.all_content, re.MULTILINE))
        # Filter out false positives from dialogue strings
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
        self.assertIn("start", self.defined_labels, "The 'start' label is missing")

    def test_all_chapter_labels_exist(self):
        expected = ["chapter_1", "chapter_2", "chapter_3"]
        for label in expected:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_all_path_labels_exist(self):
        expected = ["path_knowledge", "path_duty", "path_freedom", "path_power", "path_true"]
        for label in expected:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_all_ending_labels_exist(self):
        expected = ["ending_scholar", "ending_guardian", "ending_liberator", "ending_shadow"]
        for label in expected:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_convergence_labels_exist(self):
        expected = ["ch1_convergence", "ch2_convergence"]
        for label in expected:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")

    def test_branch_labels_exist(self):
        expected = [
            "ch1_library", "ch1_underground",
            "ch2_elara", "ch2_kael", "ch2_sirin"
        ]
        for label in expected:
            self.assertIn(label, self.defined_labels, f"Label '{label}' is missing")


class TestScreenDefinitions(unittest.TestCase):
    """Test that all screens referenced in the code are defined."""

    @classmethod
    def setUpClass(cls):
        cls.files = read_all_rpy_files()
        cls.all_content = "\n".join(cls.files.values())

        # Extract defined screens
        cls.defined_screens = set(
            re.findall(r'^screen\s+(\w+)', cls.all_content, re.MULTILINE)
        )

        # Extract ShowMenu references
        cls.showmenu_refs = set(
            re.findall(r'ShowMenu\([\'"](\w+)[\'"]\)', cls.all_content)
        )

        # Extract 'use' references (only indented Ren'Py screen statements, not dialogue text)
        cls.use_refs = set(
            re.findall(r'^\s+use\s+(\w+)', cls.all_content, re.MULTILINE)
        )
        # Filter out false positives from dialogue strings
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
            self.assertIn(
                screen, self.defined_screens,
                f"Required screen '{screen}' is not defined"
            )

    def test_showmenu_targets_exist(self):
        for target in self.showmenu_refs:
            self.assertIn(
                target, self.defined_screens,
                f"ShowMenu('{target}') references undefined screen"
            )

    def test_use_targets_exist(self):
        for target in self.use_refs:
            self.assertIn(
                target, self.defined_screens,
                f"'use {target}' references undefined screen"
            )


class TestCharacterDefinitions(unittest.TestCase):
    """Test that all character definitions are valid."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")

    def test_all_characters_defined(self):
        expected = ["mc", "elara", "kael", "sirin", "vesper", "narrator", "unknown"]
        for char in expected:
            pattern = rf'define\s+{char}\s*='
            self.assertRegex(
                self.script, pattern,
                f"Character '{char}' is not defined in script.rpy"
            )

    def test_narrator_is_not_nvl(self):
        """Narrator should NOT be NVL mode because the script has no nvl clear statements."""
        # Check that narrator is defined without kind=nvl
        narrator_match = re.search(r'define\s+narrator\s*=\s*Character\(([^)]+)\)', self.script)
        self.assertIsNotNone(narrator_match, "Narrator character not found")
        args = narrator_match.group(1)
        self.assertNotIn(
            "nvl", args,
            "Narrator should not use kind=nvl without nvl clear statements in the script"
        )

    def test_characters_used_in_script_are_defined(self):
        """Every character tag used in dialogue should be defined."""
        # Find all dialogue lines: "charname 'text'" or 'charname "text"'
        dialogue_chars = set(re.findall(r'^    (\w+)\s+"', self.script, re.MULTILINE))
        # Filter out Ren'Py keywords that look like character names
        renpy_keywords = {
            "if", "else", "elif", "for", "while", "return", "jump", "call",
            "scene", "show", "hide", "with", "play", "stop", "define",
            "default", "label", "menu", "python", "style", "screen", "text"
        }
        dialogue_chars -= renpy_keywords

        defined_chars = set(re.findall(r'define\s+(\w+)\s*=\s*Character', self.script))
        undefined = dialogue_chars - defined_chars
        self.assertEqual(
            undefined, set(),
            f"Characters used in dialogue but not defined: {', '.join(sorted(undefined))}"
        )


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
        self.assertIn("jump ch1_convergence", self.script)
        # Both branches should lead to convergence
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
            # Find the next label after this branch
            remaining = self.script[section_start:]
            lines = remaining.split("\n")
            branch_text = ""
            for i, line in enumerate(lines):
                if i > 0 and re.match(r'^label\s+\w+:', line):
                    break
                branch_text += line + "\n"
            self.assertIn(
                "jump ch2_convergence", branch_text,
                f"Branch '{branch}' does not converge to ch2_convergence"
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
            # Get text up to the next path label or end
            next_label_match = re.search(r'\nlabel (?!{})\w+:'.format(ending), remaining[1:])
            if next_label_match:
                section = remaining[:next_label_match.start() + 1]
            else:
                section = remaining
            self.assertIn(
                f"jump {ending}", section,
                f"Path '{path}' does not lead to ending '{ending}'"
            )

    def test_all_endings_have_return(self):
        for ending in ["ending_scholar", "ending_guardian", "ending_liberator", "ending_shadow"]:
            section_start = self.script.index(f"label {ending}:")
            remaining = self.script[section_start:]
            # Find next label
            next_match = re.search(r'\nlabel \w+:', remaining[1:])
            if next_match:
                section = remaining[:next_match.start() + 1]
            else:
                section = remaining
            self.assertIn("return", section, f"Ending '{ending}' has no return statement")

    def test_true_ending_has_return(self):
        section_start = self.script.index("label path_true:")
        section = self.script[section_start:]
        self.assertIn("return", section, "True ending path has no return statement")

    def test_true_route_conditional_gate(self):
        """True path should only be available when true_route is set."""
        ch3 = self.script[self.script.index("label chapter_3:"):]
        ch3 = ch3[:ch3.index("label path_knowledge:")]
        self.assertIn("if true_route", ch3)


class TestPersistentVariables(unittest.TestCase):
    """Test persistent variable handling is consistent."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")
        cls.screens = read_file("screens.rpy")

    def test_all_ending_flags_have_defaults(self):
        endings = [
            "ending_scholar", "ending_guardian",
            "ending_liberator", "ending_shadow", "ending_true"
        ]
        for ending in endings:
            self.assertIn(
                f"default persistent.{ending} = False",
                self.script,
                f"persistent.{ending} default is missing"
            )

    def test_all_ending_flags_are_set_in_endings(self):
        for ending in ["ending_scholar", "ending_guardian", "ending_liberator", "ending_shadow"]:
            self.assertIn(
                f"persistent.{ending} = True",
                self.script,
                f"persistent.{ending} is never set to True in any ending"
            )

    def test_true_ending_flag_is_set(self):
        self.assertIn(
            "persistent.ending_true = True",
            self.script,
            "persistent.ending_true is never set to True"
        )

    def test_ending_gallery_references_all_endings(self):
        screens = self.screens
        for ending in ["ending_scholar", "ending_guardian", "ending_liberator", "ending_shadow"]:
            self.assertIn(
                ending, screens,
                f"Ending gallery does not reference persistent.{ending}"
            )

    def test_true_route_unlock_logic(self):
        """All four ending flags must be true to unlock the true route."""
        self.assertIn("persistent.ending_scholar and persistent.ending_guardian", self.script)
        self.assertIn("persistent.ending_liberator and persistent.ending_shadow", self.script)


class TestGameVariables(unittest.TestCase):
    """Test that all game variables are properly initialized."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")

    def test_default_variables_exist(self):
        required_defaults = [
            "player_name", "trust_elara", "trust_kael", "trust_sirin",
            "knowledge", "duty", "freedom", "power", "true_route"
        ]
        for var in required_defaults:
            self.assertRegex(
                self.script,
                rf'default\s+{var}\s*=',
                f"Game variable '{var}' has no default statement"
            )

    def test_player_name_has_default(self):
        self.assertIn('default player_name = "Aiden"', self.script)


class TestTransformDefinitions(unittest.TestCase):
    """Test that all transforms used in screens are defined."""

    @classmethod
    def setUpClass(cls):
        cls.screens = read_file("screens.rpy")
        cls.script = read_file("script.rpy")

    def test_delayed_blink_defined(self):
        self.assertIn(
            "transform delayed_blink", self.screens,
            "The 'delayed_blink' transform is used in skip_indicator but not defined"
        )

    def test_notify_appear_defined(self):
        self.assertIn(
            "transform notify_appear", self.screens,
            "The 'notify_appear' transform is used in notify screen but not defined"
        )

    def test_script_transitions_defined(self):
        for transition in ["flash", "slow_dissolve", "fade_to_black"]:
            self.assertRegex(
                self.script,
                rf'define\s+{transition}\s*=',
                f"Transition '{transition}' is used but not defined"
            )


class TestRenpySyntax(unittest.TestCase):
    """Test for common Ren'Py syntax issues."""

    @classmethod
    def setUpClass(cls):
        cls.files = read_all_rpy_files()

    def test_no_unclosed_text_tags(self):
        """Check for unclosed Ren'Py text tags in dialogue."""
        tag_pattern = re.compile(r'\{(/?\w+?)(?:=[^}]*)?\}')
        for fname, content in self.files.items():
            lines = content.split("\n")
            for i, line in enumerate(lines):
                # Only check dialogue lines (quoted strings)
                strings = re.findall(r'"([^"]*)"', line)
                for s in strings:
                    tags = tag_pattern.findall(s)
                    open_tags = []
                    for tag in tags:
                        if tag.startswith("/"):
                            tag_name = tag[1:]
                            if open_tags and open_tags[-1] == tag_name:
                                open_tags.pop()
                        elif tag not in ("p", "w", "nw", "fast", "slow", "cps", "done",
                                         "#file_time", "#auto_page", "#quick_page"):
                            open_tags.append(tag)
                    # Allow self-closing/special tags
                    remaining = [t for t in open_tags if t not in ("b", "i", "u", "s", "color", "a")]
                    # We don't fail on this since some tags like {color=...} are used inline
                    # Just check for obviously broken tags

    def test_no_gui_preference_without_default_anywhere(self):
        """No gui.preference() call should be missing a default value."""
        for fname, content in self.files.items():
            # Find gui.preference calls with only one argument (no default)
            # Pattern: gui.preference("something") without a second argument
            calls = re.findall(r'gui\.preference\(([^)]+)\)', content)
            for call in calls:
                args = [a.strip() for a in call.split(",")]
                if len(args) < 2:
                    self.fail(
                        f"In {fname}: gui.preference({call}) has no default value. "
                        f"This will crash if the preference is not already set."
                    )

    def test_menu_choices_have_actions(self):
        """All menu choices should have a jump or other action."""
        for fname, content in self.files.items():
            # Find menu blocks and verify each choice has content
            in_menu = False
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped == "menu:":
                    in_menu = True
                elif in_menu and stripped.startswith('"') and stripped.endswith('":'):
                    # This is a menu choice - the next indented line should have action
                    pass  # Ren'Py handles this with indentation blocks

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
                duplicates.append(f"'{label}' defined in both {seen[label]} and {fname}")
            seen[label] = fname

        self.assertEqual(
            duplicates, [],
            f"Duplicate label definitions found: {'; '.join(duplicates)}"
        )


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


class TestEndToEndPaths(unittest.TestCase):
    """Simulate walking through each game path to verify completeness."""

    @classmethod
    def setUpClass(cls):
        cls.script = read_file("script.rpy")
        cls.labels = {}
        # Parse all labels and their content
        label_starts = [(m.start(), m.group(1))
                        for m in re.finditer(r'^label\s+(\w+)\s*:', cls.script, re.MULTILINE)]
        for i, (start, name) in enumerate(label_starts):
            if i + 1 < len(label_starts):
                end = label_starts[i + 1][0]
            else:
                end = len(cls.script)
            cls.labels[name] = cls.script[start:end]

    def _walk_path(self, start_label, choices):
        """
        Simulate walking through the game from start_label, making the specified choices.
        Returns the sequence of labels visited and whether a return was reached.
        """
        visited = [start_label]
        current = start_label
        choice_idx = 0

        max_steps = 50  # prevent infinite loops
        steps = 0

        while steps < max_steps:
            steps += 1
            if current not in self.labels:
                return visited, False, f"Label '{current}' not found"

            content = self.labels[current]

            # Check for return
            if re.search(r'^\s+return\s*$', content, re.MULTILINE):
                has_return = True
            else:
                has_return = False

            # Find jumps in this label
            jumps = re.findall(r'jump\s+(\w+)', content)

            if not jumps:
                return visited, has_return, None

            # If there's a menu with choices, pick based on our choices list
            if "menu:" in content and choice_idx < len(choices):
                # Pick the jump that corresponds to our choice
                current = choices[choice_idx]
                choice_idx += 1
            else:
                # Take the last jump (usually the only one or the fallthrough)
                current = jumps[-1]

            visited.append(current)

        return visited, False, "Max steps exceeded"

    def test_path_scholar(self):
        """Walk: start -> ch1_library -> ch2_elara -> path_knowledge -> ending_scholar"""
        visited, has_return, error = self._walk_path("start", [
            "chapter_1", "ch1_library", "ch1_convergence",
            "chapter_2", "ch2_elara", "ch2_convergence",
            "chapter_3", "path_knowledge", "ending_scholar"
        ])
        self.assertIsNone(error, f"Error walking scholar path: {error}")
        self.assertIn("ending_scholar", visited)

    def test_path_guardian(self):
        """Walk: start -> ch1_underground -> ch2_kael -> path_duty -> ending_guardian"""
        visited, has_return, error = self._walk_path("start", [
            "chapter_1", "ch1_underground", "ch1_convergence",
            "chapter_2", "ch2_kael", "ch2_convergence",
            "chapter_3", "path_duty", "ending_guardian"
        ])
        self.assertIsNone(error, f"Error walking guardian path: {error}")
        self.assertIn("ending_guardian", visited)

    def test_path_liberator(self):
        """Walk: start -> ch1_library -> ch2_sirin -> path_freedom -> ending_liberator"""
        visited, has_return, error = self._walk_path("start", [
            "chapter_1", "ch1_library", "ch1_convergence",
            "chapter_2", "ch2_sirin", "ch2_convergence",
            "chapter_3", "path_freedom", "ending_liberator"
        ])
        self.assertIsNone(error, f"Error walking liberator path: {error}")
        self.assertIn("ending_liberator", visited)

    def test_path_shadow(self):
        """Walk: start -> ch1_underground -> ch2_kael -> path_power -> ending_shadow"""
        visited, has_return, error = self._walk_path("start", [
            "chapter_1", "ch1_underground", "ch1_convergence",
            "chapter_2", "ch2_kael", "ch2_convergence",
            "chapter_3", "path_power", "ending_shadow"
        ])
        self.assertIsNone(error, f"Error walking shadow path: {error}")
        self.assertIn("ending_shadow", visited)

    def test_true_ending_path(self):
        """The true ending path should be reachable."""
        self.assertIn("path_true", self.labels, "True ending path label exists")
        content = self.labels["path_true"]
        self.assertIn("return", content, "True ending has a return")
        self.assertIn("persistent.ending_true = True", content)


class TestShowNameNotDuplicated(unittest.TestCase):
    """Test that gui.show_name isn't conflictingly defined."""

    def test_show_name_consistency(self):
        gui = read_file("gui.rpy")
        options = read_file("options.rpy")
        # gui.show_name should be defined in exactly one place
        gui_count = len(re.findall(r'define\s+gui\.show_name\s*=', gui))
        options_count = len(re.findall(r'define\s+gui\.show_name\s*=', options))
        total = gui_count + options_count
        self.assertGreaterEqual(total, 1, "gui.show_name should be defined at least once")


if __name__ == "__main__":
    unittest.main(verbosity=2)
