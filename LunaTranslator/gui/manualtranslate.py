from qtsymbols import *
import qtawesome
from myutils.config import globalconfig
from myutils.utils import all_langs, getlangsrc, getlangtgt
from gui.usefulwidget import getsimplecombobox, getIconButton


class CtrlEnterTextEdit(QPlainTextEdit):
    enterpressed = pyqtSignal()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return or e.key() == Qt.Key.Key_Enter:
            if (
                e.modifiers() == Qt.KeyboardModifier.ControlModifier
                or e.modifiers() == Qt.KeyboardModifier.ShiftModifier
                or e.modifiers() == Qt.KeyboardModifier.AltModifier
            ):
                self.insertPlainText("\n")
            else:
                self.enterpressed.emit()
        elif e.key() == Qt.Key.Key_Escape:
            self.clear()
        else:
            super().keyPressEvent(e)


class ManualTranslatePanel(QFrame):
    translate_requested = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("manual_translate_panel")
        self._last_translated = ""
        self._init_config()
        self._setup_ui()
        self._apply_style()
        self._setup_debounce()

    def _init_config(self):
        if "manual_srclang" not in globalconfig:
            globalconfig["manual_srclang"] = "zh"
        if "manual_tgtlang" not in globalconfig:
            tgt = getlangtgt()
            globalconfig["manual_tgtlang"] = tgt.code if tgt.code != "zh" else "en"
        if "manual_panel_height" not in globalconfig:
            globalconfig["manual_panel_height"] = 140

    def _setup_debounce(self):
        self._debounce_timer = QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(800)
        self._debounce_timer.timeout.connect(self._auto_translate)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 2, 4, 2)
        main_layout.setSpacing(3)

        lang_row = QHBoxLayout()
        lang_row.setSpacing(4)

        src_names, src_codes = all_langs(src=True)
        self.src_combo = getsimplecombobox(
            src_names,
            globalconfig,
            "manual_srclang",
            internal=src_codes,
            sizeX=True,
        )

        self.swap_btn = getIconButton(
            callback=self._swap_langs,
            icon="fa.exchange",
            tips="交换语言",
        )
        self.swap_btn.setFixedWidth(28)

        tgt_names, tgt_codes = all_langs(src=False)
        self.tgt_combo = getsimplecombobox(
            tgt_names,
            globalconfig,
            "manual_tgtlang",
            internal=tgt_codes,
            sizeX=True,
        )

        lang_row.addWidget(self.src_combo)
        lang_row.addWidget(self.swap_btn)
        lang_row.addWidget(self.tgt_combo)
        main_layout.addLayout(lang_row)

        self.text_input = CtrlEnterTextEdit(self)
        self.text_input.setPlaceholderText("输入要翻译的文本...")
        self.text_input.enterpressed.connect(self._do_translate)
        self.text_input.textChanged.connect(self._on_text_changed)
        main_layout.addWidget(self.text_input, 1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(4)

        self.translate_btn = getIconButton(
            callback=self._do_translate,
            icon="fa.search",
            tips="翻译 (Enter)",
        )
        self.clear_btn = getIconButton(
            callback=self._clear_all,
            icon="fa.times",
            tips="清空 (Esc)",
        )

        btn_row.addStretch()
        btn_row.addWidget(self.translate_btn)
        btn_row.addWidget(self.clear_btn)
        main_layout.addLayout(btn_row)

    def _swap_langs(self):
        src = globalconfig.get("manual_srclang", "zh")
        tgt = globalconfig.get("manual_tgtlang", "en")
        if src == "auto":
            return
        globalconfig["manual_srclang"] = tgt
        globalconfig["manual_tgtlang"] = src
        self.src_combo.setCurrentData(tgt)
        self.tgt_combo.setCurrentData(src)

    def _on_text_changed(self):
        self._debounce_timer.start()

    def _auto_translate(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            return
        if text == self._last_translated:
            return
        self._do_translate()

    def _do_translate(self):
        text = self.text_input.toPlainText().strip()
        if text:
            self._last_translated = text
            self.translate_requested.emit(text)

    def _clear_all(self):
        self.text_input.clear()
        self._last_translated = ""

    def _apply_style(self):
        self.setStyleSheet("""
            QFrame#manual_translate_panel {
                background-color: rgba(0, 0, 0, 30);
                border: 1px solid rgba(128, 128, 128, 60);
            }
        """)
        self.text_input.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(30, 30, 30, 200);
                color: white;
                border: 1px solid rgba(128, 128, 128, 80);
                padding: 4px;
            }
        """)
