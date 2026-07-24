import os
import sys
import shutil
from pathlib import Path

import _patch_env  # noqa: F401
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QGroupBox, QFormLayout,
    QDoubleSpinBox, QComboBox, QLineEdit, QLabel, QRadioButton,
    QButtonGroup, QWidget
)
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QIcon
from log_window import LogWindow
from worker import Worker
from audio_separator_runner import run_separator
from basicpitch_runner import run_basicpitch

class Converter(QWidget):
    LANGUAGE_CODES = ("zh", "en", "ja")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio 2 MIDI v0.1.0 (DirectML)")
        resource_base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
        self.setWindowIcon(QIcon(str(resource_base / "icon.ico")))
        layout = QVBoxLayout()

        self.translations = {
            "en": {
                "language": "Language", "input_group": "Input File", "mode": "Mode:",
                "separate_midi": "Separate + MIDI", "separate": "Separate only",
                "midi": "MIDI only", "separator_group": "Audio Separator (Stem Separation)",
                "model": "Model:", "stem": "Stem to convert:", "vocals": "Vocals",
                "instrumental": "Instrumental", "pitch_group": "Basic Pitch (Audio → MIDI)",
                "sonify": "Generate audio preview", "save_midi": "Save MIDI file",
                "save_notes": "Save notes as CSV", "save_outputs": "Save model outputs",
                "advanced": "Basic Pitch Advanced", "onset": "Onset threshold",
                "frame": "Frame threshold", "min_note": "Minimum note length (ms)",
                "min_freq": "Minimum frequency (Hz)", "max_freq": "Maximum frequency (Hz)", "merge_thresh": "Merge notes (ms)",
                "onset_hint": "Many soft notes are missed: lower Onset\nToo many noise notes: raise Onset",
                "frame_hint": "Long notes are cut short: lower Frame\nNote tails are too long: raise Frame",
                "merge_hint": "Merge consecutive same-pitch notes with gap ≤ this value. Set to 0 to disable.",
                "start": "Start Processing", "stop": "Stop Processing", "log": "Logs",
                "log_title": "Log Output", "clear": "Clear",
                "select_audio": "Select audio file", "audio_filter": "Audio files (*.wav *.mp3 *.ogg *.flac *.m4a)",
                "warning": "Warning", "select_input": "Please select an input file first",
                "stopped": "Stopped", "stopped_message": "Processing has been stopped.",
                "complete": "Complete", "saved_to": "Files saved to:\n{path}",
                "status_processing": "Processing...", "status_downloading": "Downloading model...",
                "status_separating": "Separating audio...", "status_loading": "Loading model...",
                "status_loaded": "Model loaded", "status_separate_done": "Separate done",
                "status_pitch": "Basic Pitch processing...", "status_done": "Done",
                "status_stopped": "Stopped", "status_stopping": "Stopping...", "status_error": "Error:"
            },
            "zh": {
                "language": "语言", "input_group": "输入文件", "mode": "模式：",
                "separate_midi": "分离 + MIDI", "separate": "仅分离", "midi": "仅 MIDI",
                "separator_group": "音频分离（音轨分离）", "model": "模型：", "stem": "要转换的音轨：",
                "vocals": "人声", "instrumental": "伴奏", "pitch_group": "Basic Pitch（音频 → MIDI）",
                "sonify": "生成音频预览", "save_midi": "保存 MIDI 文件", "save_notes": "保存音符为 CSV",
                "save_outputs": "保存模型输出", "advanced": "Basic Pitch 高级设置", "onset": "起始阈值",
                "frame": "帧阈值", "min_note": "最短音符长度（毫秒）", "min_freq": "最低频率（Hz）",
                "max_freq": "最高频率（Hz）", "merge_thresh": "合并音符（毫秒）", "start": "开始处理", "stop": "停止处理", "log": "日志",
                "onset_hint": "漏掉很多轻音符：降低 Onset\n出现很多杂音音符：提高 Onset",
                "frame_hint": "长音被切成一截一截：降低 Frame\n音符尾巴拖得太长：提高 Frame",
                "merge_hint": "合并同音高且间隔 ≤ 该值的连续音符。设为 0 关闭合并。",
                "log_title": "日志输出", "clear": "清除",
                "select_audio": "选择音频文件", "audio_filter": "音频文件 (*.wav *.mp3 *.ogg *.flac *.m4a)",
                "warning": "警告", "select_input": "请先选择输入文件", "stopped": "已停止",
                "stopped_message": "处理已停止。", "complete": "完成", "saved_to": "文件已保存到：\n{path}",
                "status_processing": "处理中...", "status_downloading": "正在下载模型...", "status_separating": "正在分离音频...",
                "status_loading": "正在加载模型...", "status_loaded": "模型已加载", "status_separate_done": "分离完成",
                "status_pitch": "Basic Pitch 处理中...", "status_done": "完成", "status_stopped": "已停止", "status_stopping": "正在停止...", "status_error": "错误："
            },
            "ja": {
                "language": "言語", "input_group": "入力ファイル", "mode": "モード：",
                "separate_midi": "分離 + MIDI", "separate": "分離のみ", "midi": "MIDI のみ",
                "separator_group": "Audio Separator（音源分離）", "model": "モデル：", "stem": "変換する音源：",
                "vocals": "ボーカル", "instrumental": "伴奏", "pitch_group": "Basic Pitch（音声 → MIDI）",
                "sonify": "音声プレビューを生成", "save_midi": "MIDI ファイルを保存", "save_notes": "ノートを CSV で保存",
                "save_outputs": "モデル出力を保存", "advanced": "Basic Pitch 詳細設定", "onset": "オンセット閾値",
                "frame": "フレーム閾値", "min_note": "最小音符長（ms）", "min_freq": "最低周波数（Hz）",
                "max_freq": "最高周波数（Hz）", "merge_thresh": "ノートを結合（ms）", "start": "処理開始", "stop": "処理停止", "log": "ログ",
                "onset_hint": "小さい音符が抜ける：Onset を下げる\nノイズ音符が多い：Onset を上げる",
                "frame_hint": "長い音が短く切れる：Frame を下げる\n音符の余韻が長すぎる：Frame を上げる",
                "merge_hint": "同じ高さで連続する音符を、間隔がこの値以下の場合に結合。0 で無効。",
                "log_title": "ログ出力", "clear": "クリア",
                "select_audio": "音声ファイルを選択", "audio_filter": "音声ファイル (*.wav *.mp3 *.ogg *.flac *.m4a)",
                "warning": "警告", "select_input": "先に入力ファイルを選択してください", "stopped": "停止",
                "stopped_message": "処理を停止しました。", "complete": "完了", "saved_to": "ファイルの保存先：\n{path}",
                "status_processing": "処理中...", "status_downloading": "モデルをダウンロード中...", "status_separating": "音声を分離中...",
                "status_loading": "モデルを読み込み中...", "status_loaded": "モデルを読み込みました", "status_separate_done": "分離完了",
                "status_pitch": "Basic Pitch 処理中...", "status_done": "完了", "status_stopped": "停止", "status_stopping": "停止中...", "status_error": "エラー："
            }
        }
        self.language = "en"

        language_layout = QHBoxLayout()
        self.language_label = QLabel()
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("中文", "zh")
        self.language_combo.addItem("日本語", "ja")
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        layout.addLayout(language_layout)

        if getattr(sys, 'frozen', False):
            settings_path = Path(sys.executable).parent / "settings.ini"
        else:
            settings_path = Path(__file__).parent / "settings.ini"
        self.settings = QSettings(str(settings_path), QSettings.Format.IniFormat)

        # File selection
        self.file_group = QGroupBox()
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_button = QPushButton("...")
        self.file_button.clicked.connect(self.open_file)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.file_button)
        self.file_group.setLayout(file_layout)
        layout.addWidget(self.file_group)

        # Mode selection
        mode_layout = QHBoxLayout()
        self.mode_label = QLabel()
        mode_layout.addWidget(self.mode_label)
        self.mode_group = QButtonGroup(self)
        self.rb_separate_midi = QRadioButton("Separate + MIDI")
        self.rb_separate = QRadioButton("Separate only")
        self.rb_midi = QRadioButton("MIDI only")
        self.rb_separate_midi.setProperty("mode_key", "Separate + MIDI")
        self.rb_separate.setProperty("mode_key", "Separate only")
        self.rb_midi.setProperty("mode_key", "MIDI only")
        self.rb_separate_midi.setChecked(True)
        self.mode_group.addButton(self.rb_separate_midi)
        self.mode_group.addButton(self.rb_separate)
        self.mode_group.addButton(self.rb_midi)
        self.mode_group.buttonToggled.connect(self.on_mode_changed)
        mode_layout.addWidget(self.rb_separate_midi)
        mode_layout.addWidget(self.rb_separate)
        mode_layout.addWidget(self.rb_midi)
        layout.addLayout(mode_layout)

        # Audio Separator controls
        self.sep_group = QGroupBox()
        sep_layout = QVBoxLayout()
        model_layout = QHBoxLayout()
        self.model_label = QLabel()
        model_layout.addWidget(self.model_label)
        self.separator_model = QComboBox()
        self.separator_model.addItems([
            "UVR-MDX-NET-Inst HQ 5.onnx",
            "UVR-MDX-NET-Inst HQ 3.onnx",
            "UVR MDXNET KARA 2.onnx",
            "htdemucs_ft.yaml",
            "htdemucs.yaml",
            "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
            "model mel band roformer_ep_3005_sdr_11.4360.ckpt",
        ])
        model_layout.addWidget(self.separator_model)
        sep_layout.addLayout(model_layout)
        stem_layout = QHBoxLayout()
        self.stem_label = QLabel()
        stem_layout.addWidget(self.stem_label)
        self.separator_stem = QComboBox()
        self.separator_stem.addItem("Vocals", "Vocals")
        self.separator_stem.addItem("Instrumental", "Instrumental")
        stem_layout.addWidget(self.separator_stem)
        sep_layout.addLayout(stem_layout)
        self.sep_group.setLayout(sep_layout)
        layout.addWidget(self.sep_group)

        # Basic Pitch controls
        self.bp_group = QGroupBox()
        bp_layout = QVBoxLayout()
        self.sonify_cb = QCheckBox("Generate audio preview")
        self.save_midi_cb = QCheckBox("Save MIDI file")
        self.save_midi_cb.setChecked(True)
        self.save_notes_cb = QCheckBox("Save notes as CSV")
        self.save_outputs_cb = QCheckBox("Save model outputs")
        bp_layout.addWidget(self.sonify_cb)
        bp_layout.addWidget(self.save_midi_cb)
        bp_layout.addWidget(self.save_notes_cb)
        bp_layout.addWidget(self.save_outputs_cb)
        self.bp_group.setLayout(bp_layout)
        layout.addWidget(self.bp_group)

        # Advanced parameters
        self.adv_group = QGroupBox()
        self.adv_layout = QFormLayout()
        self.onset_threshold = QDoubleSpinBox()
        self.frame_threshold = QDoubleSpinBox()
        self.min_note_length = QDoubleSpinBox()
        self.min_freq = QDoubleSpinBox()
        self.max_freq = QDoubleSpinBox()
        self.onset_threshold.setRange(0.0, 1.0)
        self.onset_threshold.setValue(0.0)
        self.onset_threshold.setSingleStep(0.1)
        self.frame_threshold.setRange(0.0, 1.0)
        self.frame_threshold.setValue(0.6)
        self.frame_threshold.setSingleStep(0.1)
        self.min_note_length.setRange(0.0, 1000.0)
        self.min_note_length.setValue(127.7)
        self.min_freq.setRange(20.0, 20000.0)
        self.min_freq.setValue(50.0)
        self.max_freq.setRange(20.0, 20000.0)
        self.max_freq.setValue(5000.0)
        self.onset_label = QLabel()
        self.frame_label = QLabel()
        self.min_note_label = QLabel()
        self.min_freq_label = QLabel()
        self.max_freq_label = QLabel()
        self.merge_thresh_label = QLabel()
        self.onset_help = QLabel("?")
        self.frame_help = QLabel("?")
        self.merge_help = QLabel("?")
        for help_label in (self.onset_help, self.frame_help, self.merge_help):
            help_label.setFixedWidth(18)
            help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            help_label.setStyleSheet("color: #666; font-weight: bold;")

        onset_control = QWidget()
        onset_layout = QHBoxLayout(onset_control)
        onset_layout.setContentsMargins(0, 0, 0, 0)
        onset_layout.addWidget(self.onset_threshold)
        onset_layout.addWidget(self.onset_help)
        frame_control = QWidget()
        frame_layout = QHBoxLayout(frame_control)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.frame_threshold)
        frame_layout.addWidget(self.frame_help)
        self.merge_threshold = QDoubleSpinBox()
        self.merge_threshold.setRange(0.0, 10000.0)
        self.merge_threshold.setValue(50.0)
        self.merge_threshold.setSingleStep(10.0)
        merge_control = QWidget()
        merge_layout = QHBoxLayout(merge_control)
        merge_layout.setContentsMargins(0, 0, 0, 0)
        merge_layout.addWidget(self.merge_threshold)
        merge_layout.addWidget(self.merge_help)

        self.adv_layout.addRow(self.onset_label, onset_control)
        self.adv_layout.addRow(self.frame_label, frame_control)
        self.adv_layout.addRow(self.merge_thresh_label, merge_control)
        self.adv_layout.addRow(self.min_note_label, self.min_note_length)
        self.adv_layout.addRow(self.min_freq_label, self.min_freq)
        self.adv_layout.addRow(self.max_freq_label, self.max_freq)
        self.adv_group.setLayout(self.adv_layout)
        layout.addWidget(self.adv_group)

        # Convert button
        btn_layout = QHBoxLayout()
        self.button = QPushButton()
        self.button.clicked.connect(self.toggle_processing)
        self.is_running = False
        btn_layout.addWidget(self.button, 3)
        self.log_btn = QPushButton()
        self.log_btn.clicked.connect(self.open_log)
        btn_layout.addWidget(self.log_btn, 1)
        layout.addLayout(btn_layout)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_text = ""
        layout.addWidget(self.progress)

        self.setLayout(layout)

        self._stop_flag = False
        self._stop_requested = False
        self._last_error = False
        self.on_mode_changed()
        self.load_settings()
        self._apply_language()

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

    def _t(self, key):
        return self.translations[self.language][key]

    def _on_language_changed(self):
        language = self.language_combo.currentData()
        if language in self.LANGUAGE_CODES:
            self.language = language
            self._apply_language()

    def _apply_language(self):
        self.language_label.setText(self._t("language") + ":")
        self.file_group.setTitle(self._t("input_group"))
        self.mode_label.setText(self._t("mode"))
        self.rb_separate_midi.setText(self._t("separate_midi"))
        self.rb_separate.setText(self._t("separate"))
        self.rb_midi.setText(self._t("midi"))
        self.sep_group.setTitle(self._t("separator_group"))
        self.model_label.setText(self._t("model"))
        self.stem_label.setText(self._t("stem"))
        self.separator_stem.setItemText(0, self._t("vocals"))
        self.separator_stem.setItemText(1, self._t("instrumental"))
        self.bp_group.setTitle(self._t("pitch_group"))
        self.sonify_cb.setText(self._t("sonify"))
        self.save_midi_cb.setText(self._t("save_midi"))
        self.save_notes_cb.setText(self._t("save_notes"))
        self.save_outputs_cb.setText(self._t("save_outputs"))
        self.adv_group.setTitle(self._t("advanced"))
        self.onset_label.setText(self._t("onset"))
        self.frame_label.setText(self._t("frame"))
        self.min_note_label.setText(self._t("min_note"))
        self.min_freq_label.setText(self._t("min_freq"))
        self.max_freq_label.setText(self._t("max_freq"))
        self.merge_thresh_label.setText(self._t("merge_thresh"))
        self.onset_help.setToolTip(self._t("onset_hint"))
        self.frame_help.setToolTip(self._t("frame_hint"))
        self.merge_help.setToolTip(self._t("merge_hint"))
        self.button.setText(self._t("stop") if self.is_running else self._t("start"))
        self.log_btn.setText(self._t("log"))
        if self._status_text:
            self.progress.setFormat(self._translate_status(self._status_text))
        if hasattr(self, "_log_window") and self._log_window is not None:
            self._log_window.set_language_texts(
                self._t("log_title"), self._t("clear")
            )

    def _translate_status(self, text):
        status_keys = (
            ("Downloading model...", "status_downloading"),
            ("Separating audio...", "status_separating"),
            ("Loading model...", "status_loading"),
            ("Model loaded", "status_loaded"),
            ("Separate done", "status_separate_done"),
            ("Basic Pitch processing...", "status_pitch"),
            ("Processing...", "status_processing"),
            ("Done", "status_done"),
            ("Stopped", "status_stopped"),
            ("Stopping...", "status_stopping"),
            ("Error:", "status_error"),
        )
        for prefix, key in status_keys:
            if text.startswith(prefix):
                return self._t(key) + text[len(prefix):]
        return text

    def load_settings(self):
        s = self.settings
        language = s.value("language", "en")
        if language not in self.LANGUAGE_CODES:
            language = "en"
        language_index = self.language_combo.findData(language)
        self.language_combo.setCurrentIndex(language_index)
        self.language = language

        mode = s.value("mode", "Separate + MIDI")
        self.rb_separate_midi.setChecked(mode == "Separate + MIDI")
        self.rb_separate.setChecked(mode == "Separate only")
        self.rb_midi.setChecked(mode == "MIDI only")
        self.separator_model.setCurrentText(s.value("separator_model", "UVR-MDX-NET-Inst_HQ_5.onnx"))
        stem_index = self.separator_stem.findData(s.value("separator_stem", "Vocals"))
        self.separator_stem.setCurrentIndex(max(0, stem_index))
        self.sonify_cb.setChecked(s.value("sonify", False, type=bool))
        self.save_midi_cb.setChecked(s.value("save_midi", True, type=bool))
        self.save_notes_cb.setChecked(s.value("save_notes", False, type=bool))
        self.save_outputs_cb.setChecked(s.value("save_outputs", False, type=bool))
        self.onset_threshold.setValue(float(s.value("onset_threshold", 0.0)))
        self.frame_threshold.setValue(float(s.value("frame_threshold", 0.6)))
        self.min_note_length.setValue(float(s.value("min_note_length", 127.7)))
        self.min_freq.setValue(float(s.value("min_freq", 50.0)))
        self.max_freq.setValue(float(s.value("max_freq", 5000.0)))
        self.merge_threshold.setValue(float(s.value("merge_threshold", 50.0)))

    def save_settings(self):
        s = self.settings
        s.setValue("language", self.language)
        if self.rb_separate_midi.isChecked():
            s.setValue("mode", "Separate + MIDI")
        elif self.rb_separate.isChecked():
            s.setValue("mode", "Separate only")
        elif self.rb_midi.isChecked():
            s.setValue("mode", "MIDI only")
        s.setValue("separator_model", self.separator_model.currentText())
        s.setValue("separator_stem", self.separator_stem.currentData())
        s.setValue("sonify", self.sonify_cb.isChecked())
        s.setValue("save_midi", self.save_midi_cb.isChecked())
        s.setValue("save_notes", self.save_notes_cb.isChecked())
        s.setValue("save_outputs", self.save_outputs_cb.isChecked())
        s.setValue("onset_threshold", self.onset_threshold.value())
        s.setValue("frame_threshold", self.frame_threshold.value())
        s.setValue("min_note_length", self.min_note_length.value())
        s.setValue("min_freq", self.min_freq.value())
        s.setValue("max_freq", self.max_freq.value())
        s.setValue("merge_threshold", self.merge_threshold.value())
        s.sync()

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, self._t("select_audio"), "", self._t("audio_filter")
        )
        if file:
            self.file_input.setText(file)

    def on_mode_changed(self):
        mode = self._current_mode()
        if mode == "MIDI only":
            self.sep_group.setEnabled(False)
            self.bp_group.setEnabled(True)
        elif mode == "Separate only":
            self.sep_group.setEnabled(True)
            self.bp_group.setEnabled(False)
        else:
            self.sep_group.setEnabled(True)
            self.bp_group.setEnabled(True)

    def _current_mode(self):
        return self.mode_group.checkedButton().property("mode_key")

    def toggle_processing(self):
        if self.is_running:
            self._stop_flag = True
            self._stop_requested = True
            self.button.setEnabled(False)
            self._status_text = "Stopping..."
            self.progress.setFormat(self._translate_status(self._status_text))
        else:
            self.run_conversion()

    def on_processing_done(self):
        stopped = self._stop_requested
        failed = self._last_error
        self.is_running = False
        self._stop_flag = False
        self._stop_requested = False
        self._last_error = False
        self.button.setEnabled(True)
        self.button.setText(self._t("start"))
        self.button.setStyleSheet("")
        if stopped:
            self.progress.setValue(0)
            self._status_text = "Stopped"
            self.progress.setFormat(self._translate_status(self._status_text))
            QMessageBox.warning(self, self._t("stopped"), self._t("stopped_message"))
        elif failed:
            self.progress.repaint()

    def run_conversion(self):
        input_file = self.file_input.text().strip()
        if not input_file:
            QMessageBox.warning(self, self._t("warning"), self._t("select_input"))
            return
        output_dir = str(Path(input_file).parent)
        output_path = Path(output_dir)

        options = {
            "sonify": self.sonify_cb.isChecked(),
            "save_midi": self.save_midi_cb.isChecked(),
            "save_outputs": self.save_outputs_cb.isChecked(),
            "save_notes": self.save_notes_cb.isChecked(),
            "onset_threshold": self.onset_threshold.value(),
            "frame_threshold": self.frame_threshold.value(),
            "min_note_length": self.min_note_length.value(),
            "min_freq": self.min_freq.value(),
            "max_freq": self.max_freq.value(),
            "merge_threshold": self.merge_threshold.value()
        }

        mode = self._current_mode()
        save_dir = str(output_path)

        # The custom completion signal is emitted just before QThread.run()
        # returns. Reap the previous thread before replacing its reference.
        previous_worker = getattr(self, "worker", None)
        if previous_worker is not None and previous_worker.isRunning():
            previous_worker.wait()

        def _sig(value, text):
            self.worker.progress_signal.emit(value, text)

        def _wrap_bp(base, weight):
            def wrapped(internal_pct, text):
                _sig(base + int(internal_pct * weight / 100), text)
            return wrapped

        self._stop_flag = False
        self._stop_requested = False
        self._last_error = False
        self.worker = Worker()
        self.worker.progress_signal.connect(self.update_progress)

        if mode == "Separate only":
            model = self.separator_model.currentText()
            stem_choice = self.separator_stem.currentData()

            def task():
                result = run_separator(input_file, output_path, model, stem_choice, _sig,
                                       separate_only_mode=True, stop_check=lambda: self._stop_flag)
                shutil.move(str(result), str(output_path / result.name))

            self.worker.func = task
        elif mode == "MIDI only":
            self.update_progress(50, "Processing...")

            def task():
                run_basicpitch([Path(input_file)], output_path, options,
                               _wrap_bp(50, 0), original_name=None,
                               merge_threshold_ms=options["merge_threshold"])

            self.worker.func = task
            self.worker.finished_signal.connect(lambda: self.update_progress(100, "Done"))
        else:
            model = self.separator_model.currentText()
            stem_choice = self.separator_stem.currentData()

            def task():
                chosen_file = run_separator(input_file, output_path, model, stem_choice, _sig,
                                            stop_check=lambda: self._stop_flag)
                if not self._stop_flag and chosen_file:
                    run_basicpitch([chosen_file], output_path, options,
                                   _wrap_bp(80, 20), original_name=Path(input_file).stem,
                                   merge_threshold_ms=options["merge_threshold"])

            self.worker.func = task

        self.worker.finished_signal.connect(lambda: self.show_done(save_dir))
        self.worker.finished_signal.connect(self.on_processing_done)
        self.worker.start()
        self.is_running = True
        self.button.setText(self._t("stop"))

    def show_done(self, path):
        if self._stop_requested or self._last_error:
            return
        QMessageBox.information(
            self, self._t("complete"), self._t("saved_to").format(path=path)
        )

    def open_log(self):
        if not hasattr(self, '_log_window') or self._log_window is None:
            self._log_window = LogWindow(self)
        self._log_window.set_language_texts(
            self._t("log_title"), self._t("clear")
        )
        self._log_window.show()
        self._log_window.raise_()

    def update_progress(self, value, text):
        self.progress.setValue(value)
        is_error = text.startswith("Error:")
        self._status_text = text
        self.progress.setFormat(self._translate_status(text))
        if is_error:
            self._last_error = True
        self.progress.repaint()
