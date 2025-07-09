import os

from components import ThemedOptionCardPlane
from icons import IconDictionary
from PyQt5.Qt import QColor, QPoint
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QTimer
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QTextEdit, QSystemTrayIcon, QMenu, QAction, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from settings_parser import SettingsParser
from todos_parser import TODOParser

from siui.components.widgets import (
    SiCheckBox,
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiSimpleButton,
    SiSvgLabel,
    SiSwitch,
    SiToggleButton,
)
from siui.core.animation import SiExpAnimation
from siui.core.color import Color
from siui.core.globals import NewGlobal, SiGlobal
from siui.gui.tooltip import ToolTipWindow

# 创建删除队列
SiGlobal.todo_list = NewGlobal()
SiGlobal.todo_list.delete_pile = []

# 创建锁定位置变量
SiGlobal.todo_list.position_locked = False

# 创建设置文件解析器并写入全局变量
SiGlobal.todo_list.settings_parser = SettingsParser("./options.ini")
SiGlobal.todo_list.todos_parser = TODOParser("./todos.ini")

def lock_position(state):
    SiGlobal.todo_list.position_locked = state


# 主题颜色
def load_colors(is_dark=True):
    if is_dark is True:  # 深色主题
        # 加载图标
        SiGlobal.siui.icons.update(IconDictionary(color="#e1d9e8").icons)

        # 设置颜色
        SiGlobal.siui.colors["THEME"] = "#e1d9e8"
        SiGlobal.siui.colors["PANEL_THEME"] = "#0F85D3"
        SiGlobal.siui.colors["BACKGROUND_COLOR"] = "#252229"
        SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"] = SiGlobal.siui.colors["INTERFACE_BG_A"]
        SiGlobal.siui.colors["BORDER_COLOR"] = "#3b373f"
        SiGlobal.siui.colors["TOOLTIP_BG"] = "ef413a47"
        SiGlobal.siui.colors["SVG_A"] = SiGlobal.siui.colors["THEME"]

        SiGlobal.siui.colors["THEME_TRANSITION_A"] = "#52389a"
        SiGlobal.siui.colors["THEME_TRANSITION_B"] = "#9c4e8b"

        SiGlobal.siui.colors["TEXT_A"] = "#FFFFFF"
        SiGlobal.siui.colors["TEXT_B"] = "#e1d9e8"
        SiGlobal.siui.colors["TEXT_C"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.75)
        SiGlobal.siui.colors["TEXT_D"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.6)
        SiGlobal.siui.colors["TEXT_E"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.5)

        SiGlobal.siui.colors["SWITCH_DEACTIVATE"] = "#D2D2D2"
        SiGlobal.siui.colors["SWITCH_ACTIVATE"] = "#100912"

        SiGlobal.siui.colors["BUTTON_HOVER"] = "#10FFFFFF"
        SiGlobal.siui.colors["BUTTON_FLASH"] = "#20FFFFFF"

        SiGlobal.siui.colors["SIMPLE_BUTTON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

        SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0)
        SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

    else:  # 亮色主题
        # 加载图标
        SiGlobal.siui.icons.update(IconDictionary(color="#0F85D3").icons)

        # 设置颜色
        SiGlobal.siui.colors["THEME"] = "#0F85D3"
        SiGlobal.siui.colors["PANEL_THEME"] = "#0F85D3"
        SiGlobal.siui.colors["BACKGROUND_COLOR"] = "#F3F3F3"
        SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"] = "#e8e8e8"
        SiGlobal.siui.colors["BORDER_COLOR"] = "#d0d0d0"
        SiGlobal.siui.colors["TOOLTIP_BG"] = "#F3F3F3"
        SiGlobal.siui.colors["SVG_A"] = SiGlobal.siui.colors["THEME"]

        SiGlobal.siui.colors["THEME_TRANSITION_A"] = "#2abed8"
        SiGlobal.siui.colors["THEME_TRANSITION_B"] = "#2ad98e"

        SiGlobal.siui.colors["TEXT_A"] = "#1f1f2f"
        SiGlobal.siui.colors["TEXT_B"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.85)
        SiGlobal.siui.colors["TEXT_C"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.75)
        SiGlobal.siui.colors["TEXT_D"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.6)
        SiGlobal.siui.colors["TEXT_E"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.5)

        SiGlobal.siui.colors["SWITCH_DEACTIVATE"] = "#bec1c7"
        SiGlobal.siui.colors["SWITCH_ACTIVATE"] = "#F3F3F3"

        SiGlobal.siui.colors["BUTTON_HOVER"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.0625)
        SiGlobal.siui.colors["BUTTON_FLASH"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.43)

        SiGlobal.siui.colors["SIMPLE_BUTTON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.6)

        SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0)
        SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

    SiGlobal.siui.reloadAllWindowsStyleSheet()
    
    # 更新托盘菜单样式
    main_window = SiGlobal.siui.windows.get("MAIN_WINDOW")
    if main_window and hasattr(main_window, 'tray_icon'):
        main_window.tray_icon.refreshTrayMenu()


# 加载主题颜色
load_colors(is_dark=False)


class SingleSettingOption(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSpacing(2)

        self.title = SiLabel(self)
        self.title.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.title.setAutoAdjustSize(True)

        self.description = SiLabel(self)
        self.description.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.description.setAutoAdjustSize(True)

        self.addWidget(self.title)
        self.addWidget(self.description)
        self.addPlaceholder(4)

    def setTitle(self, title: str, description: str):
        self.title.setText(title)
        self.description.setText(description)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        self.description.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_D"]))


class SingleTODOOption(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setShrinking(True)

        self.check_box = SiCheckBox(self)
        self.check_box.resize(12, 12)
        self.check_box.setText(" ")
        self.check_box.toggled.connect(self._onChecked)

        self.text_label = SiLabel(self)
        self.text_label.resize(500 - 48 - 48 - 32, 32)
        self.text_label.setWordWrap(True)
        self.text_label.setAutoAdjustSize(True)
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_label.setFixedStyleSheet("padding-top: 2px; padding-bottom: 2px")

        self.addWidget(self.check_box)
        self.addWidget(self.text_label)

        # 初始化时自动载入样式表
        self.reloadStyleSheet()

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.text_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))

    def _onChecked(self, state):
        if state is True:
            SiGlobal.todo_list.delete_pile.append(self)
            # 延迟1秒自动刷新
            QTimer.singleShot(1000, self._delayed_refresh)
        else:
            index = SiGlobal.todo_list.delete_pile.index(self)
            SiGlobal.todo_list.delete_pile.pop(index)

    def _delayed_refresh(self):
        # 自动清除已完成项
        parent_panel = self.parent()
        # 向上查找 TODOListPanel
        from ui import TODOListPanel  # 局部导入避免循环
        while parent_panel and not isinstance(parent_panel, TODOListPanel):
            parent_panel = parent_panel.parent()
        if parent_panel:
            parent_panel.clearCompletedTODOs()

    def setText(self, text: str):
        self.text_label.setText(text)

    def adjustSize(self):
        self.setFixedHeight(self.text_label.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.text_label.setFixedWidth(event.size().width() - 48)
        self.text_label.adjustSize()
        self.adjustSize()


class AppHeaderPanel(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background_label = SiLabel(self)
        self.background_label.setFixedStyleSheet("border-radius: 8px")



        self.container_h = SiDenseHContainer(self)
        self.container_h.setAlignCenter(True)
        self.container_h.setFixedHeight(48)
        self.container_h.setSpacing(0)

        self.icon = SiSvgLabel(self)
        self.icon.resize(32, 32)
        self.icon.setSvgSize(16, 16)

        self.unfold_button = SiToggleButton(self)
        self.unfold_button.setFixedHeight(32)
        self.unfold_button.attachment().setText("0个待办事项")
        self.unfold_button.setChecked(True)

        self.settings_button = SiToggleButton(self)
        self.settings_button.resize(32, 32)
        self.settings_button.setHint("设置")
        self.settings_button.setChecked(False)

        self.add_todo_button = SiToggleButton(self)
        self.add_todo_button.resize(32, 32)
        self.add_todo_button.setHint("添加新待办")
        self.add_todo_button.setChecked(False)

        self.exit_button = SiSimpleButton(self)
        self.exit_button.resize(32, 32)
        self.exit_button.setHint("退出")

        self.container_h.addPlaceholder(16)
        self.container_h.addWidget(self.icon)
        self.container_h.addPlaceholder(4)
        self.container_h.addWidget(self.unfold_button)

        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.exit_button, "right")
        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.settings_button, "right")
        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.add_todo_button, "right")

        # 按钮加入全局变量
        SiGlobal.todo_list.todo_list_unfold_button = self.unfold_button
        SiGlobal.todo_list.add_todo_unfold_button = self.add_todo_button
        SiGlobal.todo_list.settings_unfold_button = self.settings_button

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.resize(event.size().width(), 48)
        self.container_h.resize(event.size().width(), 48)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        # 按钮颜色
        self.unfold_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                         SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])
        self.settings_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                           SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])
        self.add_todo_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                           SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])

        # svg 图标
        self.settings_button.attachment().load(SiGlobal.siui.icons["fi-rr-menu-burger"])
        self.add_todo_button.attachment().load(SiGlobal.siui.icons["fi-rr-apps-add"])
        self.exit_button.attachment().load(SiGlobal.siui.icons["fi-rr-cross-small"])
        self.icon.load('<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" '
                       'data-name="Layer 1" viewBox="0 0 24 24" width="512" height="512"><path d="M0,8v-1C0,4.243,'
                       '2.243,2,5,2h1V1c0-.552,.447-1,1-1s1,.448,1,1v1h8V1c0-.552,.447-1,1-1s1,.448,1,1v1h1c2.757,0,'
                       '5,2.243,5,5v1H0Zm24,2v9c0,2.757-2.243,5-5,5H5c-2.757,0-5-2.243-5-5V10H24Zm-6.168,'
                       '3.152c-.384-.397-1.016-.409-1.414-.026l-4.754,4.582c-.376,.376-1.007,'
                       '.404-1.439-.026l-2.278-2.117c-.403-.375-1.035-.354-1.413,.052-.376,.404-.353,1.037,.052,'
                       '1.413l2.252,2.092c.566,.567,1.32,.879,2.121,.879s1.556-.312,2.108-.866l4.74-4.568c.397-.383,'
                       '.409-1.017,.025-1.414Z" fill="{}" /></svg>'.format(SiGlobal.siui.colors["SVG_A"]).encode())

        self.background_label.setStyleSheet("""background-color: {}; border: 1px solid {}""".format(
            SiGlobal.siui.colors["BACKGROUND_COLOR"], SiGlobal.siui.colors["BORDER_COLOR"]))
        self.unfold_button.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))




class TODOListPanel(ThemedOptionCardPlane):
    todoAmountChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("全部待办")
        self.setUseSignals(True)

        self.no_todo_label = SiLabel(self)
        self.no_todo_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.no_todo_label.setAutoAdjustSize(True)
        self.no_todo_label.setText("当前没有待办哦")
        self.no_todo_label.setAlignment(Qt.AlignCenter)
        self.no_todo_label.hide()

        self.body().setUseMoveTo(False)
        self.body().setShrinking(True)
        self.body().setAdjustWidgetsSize(True)

        self.footer().setFixedHeight(64)
        self.footer().setSpacing(8)
        self.footer().setAlignCenter(True)

        self.complete_all_button = SiSimpleButton(self)
        self.complete_all_button.resize(32, 32)
        self.complete_all_button.setHint("全部完成")
        self.complete_all_button.clicked.connect(self._onCompleteAllButtonClicked)

        self.footer().addWidget(self.complete_all_button, "right")

        # 全局方法
        SiGlobal.todo_list.addTODO = self.addTODO

    def updateTODOAmount(self):
        todo_amount = len(self.body().widgets_top)
        self.todoAmountChanged.emit(todo_amount)

        if todo_amount == 0:
            self.no_todo_label.show()
        else:
            self.no_todo_label.hide()

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()

        self.no_todo_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_E"]))
        self.complete_all_button.attachment().load(SiGlobal.siui.icons["fi-rr-list-check"])

    def _onCompleteAllButtonClicked(self):
        for obj in self.body().widgets_top:
            if isinstance(obj, SingleTODOOption):
                obj.check_box.setChecked(True)

    def addTODO(self, text):
        new_todo = SingleTODOOption(self)
        self.body().addWidget(new_todo)

        new_todo.setText(text)
        new_todo.show()
        new_todo.adjustSize()

        SiGlobal.todo_list.todo_list_unfold_button.setChecked(True)
        self.adjustSize()
        self.updateTODOAmount()

        # 立即写入 todos.ini
        todos = [widget.text_label.text() for widget in self.body().widgets_top]
        SiGlobal.todo_list.todos_parser.todos = todos
        SiGlobal.todo_list.todos_parser.write()

    def adjustSize(self):
        self.body().adjustSize()
        super().adjustSize()

    def leaveEvent(self, event):
        super().leaveEvent(event)

        for index, obj in enumerate(SiGlobal.todo_list.delete_pile):
            self.body().removeWidget(obj)
            obj.close()

        SiGlobal.todo_list.delete_pile = []

        if SiGlobal.todo_list.todo_list_unfold_button.isChecked() is True:
            self.adjustSize()
            self.updateTODOAmount()

    def showEvent(self, a0):
        super().showEvent(a0)
        self.updateTODOAmount()
        self.setForceUseAnimations(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.no_todo_label.resize(event.size().width(), 150)

    def clearCompletedTODOs(self):
        for obj in list(SiGlobal.todo_list.delete_pile):
            self.body().removeWidget(obj)
            obj.close()
        SiGlobal.todo_list.delete_pile = []
        self.adjustSize()
        self.updateTODOAmount()


class AddNewTODOPanel(ThemedOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("添加新待办")
        self.setUseSignals(True)

        self.confirm_button = SiSimpleButton(self)
        self.confirm_button.resize(32, 32)
        self.confirm_button.setHint("确认并添加")

        self.cancel_button = SiSimpleButton(self)
        self.cancel_button.resize(32, 32)
        self.cancel_button.setHint("取消")

        self.header().addWidget(self.cancel_button, "right")
        self.header().addWidget(self.confirm_button, "right")

        self.instruction = SiLabel(self)
        self.instruction.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.instruction.setText("请输入待办内容")

        self.text_edit = QTextEdit(self)
        self.text_edit.setFixedHeight(70)
        self.text_edit.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.text_edit.lineWrapMode()

        self.body().setAdjustWidgetsSize(True)
        self.body().setSpacing(4)
        self.body().addWidget(self.instruction)
        self.body().addWidget(self.text_edit)

    def adjustSize(self):
        self.resize(self.width(), 200)

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()

        self.confirm_button.attachment().load(SiGlobal.siui.icons["fi-rr-check"])
        self.cancel_button.attachment().load(SiGlobal.siui.icons["fi-rr-cross"])
        self.instruction.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        self.text_edit.setStyleSheet(
            """
            border: 1px solid {};
            background-color: {};
            border-radius: 4px;
            padding-left: 8px; padding-right: 8px;
            color: {}
            """.format(SiGlobal.siui.colors["BORDER_COLOR"],
                       SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"],
                       SiGlobal.siui.colors["TEXT_B"])
        )

    def showEvent(self, a0):
        super().showEvent(a0)
        self.setForceUseAnimations(True)


class SettingsPanel(ThemedOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("设置")
        self.setUseSignals(True)

        # 启用深色模式
        self.use_dark_mode = SingleSettingOption(self)
        self.use_dark_mode.setTitle("深色模式", "在深色主题的计算机上提供更佳的视觉效果")

        self.button_use_dark_mode = SiSwitch(self)
        self.button_use_dark_mode.setFixedHeight(32)
        self.button_use_dark_mode.toggled.connect(load_colors)
        self.button_use_dark_mode.toggled.connect(
            lambda b: (SiGlobal.todo_list.settings_parser.modify("USE_DARK_MODE", b),
                       SiGlobal.todo_list.settings_parser.write()))
        self.button_use_dark_mode.setChecked(SiGlobal.todo_list.settings_parser.options["USE_DARK_MODE"])

        self.use_dark_mode.addWidget(self.button_use_dark_mode)
        self.use_dark_mode.addPlaceholder(16)

        # 锁定位置
        self.fix_position = SingleSettingOption(self)
        self.fix_position.setTitle("锁定位置", "阻止拖动窗口以保持位置不变")

        self.button_fix_position = SiSwitch(self)
        self.button_fix_position.setFixedHeight(32)
        self.button_fix_position.toggled.connect(lock_position)
        self.button_fix_position.toggled.connect(
            lambda b: (SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION", b),
                       SiGlobal.todo_list.settings_parser.write()))
        self.button_fix_position.setChecked(SiGlobal.todo_list.settings_parser.options["FIXED_POSITION"])

        self.fix_position.addWidget(self.button_fix_position)
        self.fix_position.addPlaceholder(16)

        # 窗口透明度
        self.window_opacity = SingleSettingOption(self)
        self.window_opacity.setTitle("窗口透明度", "调整窗口的透明度，范围从50%到100%")
        # ------------------------------ 改为按钮控制 ------------------------------
        self.current_opacity = SiGlobal.todo_list.settings_parser.options.get("WINDOW_OPACITY", 95)
 
        # 创建横向容器以单行显示，并保持居中
        self.opacity_control_bar = SiDenseHContainer(self)
        self.opacity_control_bar.setSpacing(6)
        self.opacity_control_bar.setAlignCenter(True)

        self.opacity_minus_button = SiSimpleButton(self)
        self.opacity_minus_button.setFixedSize(32, 32)
        self.opacity_minus_button.attachment().setText("-")
        self.opacity_minus_button.clicked.connect(lambda: self._changeOpacity(-5))

        self.opacity_value_label = SiLabel(self)
        self.opacity_value_label.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.opacity_value_label.setText(f"{self.current_opacity}%")
        self.opacity_value_label.setAlignment(Qt.AlignCenter)
        self.opacity_value_label.setFixedSize(60, 32)  # 与按钮同高，保证文字垂直居中

        self.opacity_plus_button = SiSimpleButton(self)
        self.opacity_plus_button.setFixedSize(32, 32)
        self.opacity_plus_button.attachment().setText("+")
        self.opacity_plus_button.clicked.connect(lambda: self._changeOpacity(5))

        # 将控件加入横向容器
        self.opacity_control_bar.addWidget(self.opacity_minus_button)
        self.opacity_control_bar.addWidget(self.opacity_value_label)
        self.opacity_control_bar.addWidget(self.opacity_plus_button)

        # 将横向容器加入设置项
        self.window_opacity.addWidget(self.opacity_control_bar)
        self.window_opacity.addPlaceholder(16)

        # 第三方资源
        self.third_party_res = SingleSettingOption(self)
        self.third_party_res.setTitle("第三方资源", "本项目使用了 FlatIcon 提供的图标")

        self.button_to_flaticon = SiSimpleButton(self)
        self.button_to_flaticon.setFixedHeight(32)
        self.button_to_flaticon.attachment().setText("前往 FlatIcon")
        self.button_to_flaticon.clicked.connect(lambda: os.system("start https://flaticon.com/"))
        self.button_to_flaticon.adjustSize()

        self.third_party_res.addWidget(self.button_to_flaticon)
        self.third_party_res.addPlaceholder(16)

        # 许可
        self.license = SingleSettingOption(self)
        self.license.setTitle("开源许可证", "本项目采用 GNU General Public License v3.0")

        self.button_license = SiSimpleButton(self)
        self.button_license.setFixedHeight(32)
        self.button_license.attachment().setText("在 Github 上查看")
        self.button_license.clicked.connect(
            lambda: os.system("start https://github.com/ChinaIceF/My-TODOs/blob/main/LICENSE"))
        self.button_license.adjustSize()

        self.license.addWidget(self.button_license)
        self.license.addPlaceholder(16)

        # 关于
        self.about = SingleSettingOption(self)
        self.about.setTitle("关于此软件", "制作者 霏泠Ice 保留所有权利")

        about_button_set = SiDenseHContainer(self)
        about_button_set.setFixedHeight(32)

        self.button_github = SiSimpleButton(self)
        self.button_github.setFixedHeight(32)
        self.button_github.attachment().setText("Github 主页")
        self.button_github.clicked.connect(lambda: os.system("start https://github.com/ChinaIceF"))
        self.button_github.adjustSize()

        self.button_bilibili = SiSimpleButton(self)
        self.button_bilibili.setFixedHeight(32)
        self.button_bilibili.attachment().setText("哔哩哔哩 主页")
        self.button_bilibili.clicked.connect(lambda: os.system("start https://space.bilibili.com/390832893"))
        self.button_bilibili.adjustSize()

        about_button_set.addWidget(self.button_github)
        about_button_set.addWidget(self.button_bilibili)

        self.about.addWidget(about_button_set)
        self.about.addPlaceholder(16)

        # 赞助
        self.donation = SingleSettingOption(self)
        self.donation.setTitle("赞助作者", "为爱发电，您的支持是我最大的动力")

        self.button_donation = SiSimpleButton(self)
        self.button_donation.setFixedHeight(32)
        self.button_donation.attachment().setText("在 Github 上扫码赞助")
        self.button_donation.clicked.connect(lambda: os.system("start https://github.com/ChinaIceF/My-TODOs?tab=readme-ov-file#%E8%B5%9E%E5%8A%A9"))
        self.button_donation.adjustSize()

        self.donation.addWidget(self.button_donation)
        self.donation.addPlaceholder(16)

        # SiliconUI
        self.silicon_ui = SiDenseVContainer(self)
        self.silicon_ui.setAlignCenter(True)

        self.button_silicon_ui = SiSimpleButton(self)
        self.button_silicon_ui.attachment().setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.button_silicon_ui.attachment().setText("基于 PyQt-SiliconUI 编写")
        self.button_silicon_ui.adjustSize()
        self.button_silicon_ui.clicked.connect(lambda: os.system("start https://github.com/ChinaIceF/PyQt-SiliconUI"))

        self.silicon_ui.addWidget(self.button_silicon_ui)

        # 添加到body
        self.body().setAdjustWidgetsSize(True)
        self.body().addWidget(self.use_dark_mode)
        self.body().addWidget(self.fix_position)
        self.body().addWidget(self.window_opacity)
        self.body().addWidget(self.third_party_res)
        self.body().addWidget(self.license)
        self.body().addWidget(self.about)
        self.body().addWidget(self.donation)
        self.body().addWidget(self.silicon_ui)
        self.body().addPlaceholder(16)

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()

        self.button_to_flaticon.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_license.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_github.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_bilibili.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_donation.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_silicon_ui.attachment().setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_E"]))

        # 更新新的透明度控件样式
        btn_color = SiGlobal.siui.colors["SIMPLE_BUTTON_BG"]
        self.opacity_minus_button.setColor(btn_color)
        self.opacity_plus_button.setColor(btn_color)
        self.opacity_value_label.setStyleSheet(
            "color: {}; font-weight: 600;".format(SiGlobal.siui.colors["TEXT_B"]))

    def _changeOpacity(self, diff: int):
        """通过按钮增减透明度 (diff 可以为 ±5)"""
        new_value = max(50, min(100, self.current_opacity + diff))
        if new_value == self.current_opacity:
            return

        self.current_opacity = new_value
        self.opacity_value_label.setText(f"{new_value}%")
        self.opacity_value_label.adjustSize()
        self._applyOpacity(new_value)

    def _applyOpacity(self, value: int):
        """真正执行透明度变更并保存设置"""
        opacity = value / 100.0
        main_window = SiGlobal.siui.windows.get("MAIN_WINDOW")
        if main_window:
            main_window.setWindowOpacity(opacity)

        SiGlobal.todo_list.settings_parser.modify("WINDOW_OPACITY", value)
        SiGlobal.todo_list.settings_parser.write()
        # 强制立即写入，可选
        # SiGlobal.todo_list.settings_parser.write()


class SystemTrayIcon(QSystemTrayIcon):
    """系统托盘图标类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.parent_window = parent
        self.createTrayIcon()
        self.createTrayMenu()
        
        # 连接托盘图标的激活信号
        self.activated.connect(self.onTrayIconActivated)
        
        # 监听主题变化
        self.updateMenuOnThemeChange()
        
    def createTrayIcon(self):
        """创建托盘图标"""
        # 使用与主窗口左上角相同的SVG日历图标
        svg_data = '<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" ' \
                   'data-name="Layer 1" viewBox="0 0 24 24" width="512" height="512"><path d="M0,8v-1C0,4.243,' \
                   '2.243,2,5,2h1V1c0-.552,.447-1,1-1s1,.448,1,1v1h8V1c0-.552,.447-1,1-1s1,.448,1,1v1h1c2.757,0,' \
                   '5,2.243,5,5v1H0Zm24,2v9c0,2.757-2.243,5-5,5H5c-2.757,0-5-2.243-5-5V10H24Zm-6.168,' \
                   '3.152c-.384-.397-1.016-.409-1.414-.026l-4.754,4.582c-.376,.376-1.007,' \
                   '.404-1.439-.026l-2.278-2.117c-.403-.375-1.035-.354-1.413,.052-.376,.404-.353,1.037,.052,' \
                   '1.413l2.252,2.092c.566,.567,1.32,.879,2.121,.879s1.556-.312,2.108-.866l4.74-4.568c.397-.383,' \
                   '.409-1.017,.025-1.414Z" fill="{}" /></svg>'.format(SiGlobal.siui.colors["SVG_A"])
        
        # 创建32x32的图标
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        # 使用SVG渲染器渲染图标
        from PyQt5.QtSvg import QSvgRenderer
        renderer = QSvgRenderer(svg_data.encode())
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 在中心位置渲染SVG，留出一些边距
        margin = 4
        from PyQt5.QtCore import QRectF
        render_rect = QRectF(pixmap.rect().adjusted(margin, margin, -margin, -margin))
        renderer.render(painter, render_rect)
        
        painter.end()
        
        icon = QIcon(pixmap)
        self.setIcon(icon)
        
    def createTrayMenu(self):
        """创建托盘右键菜单"""
        self.tray_menu = QMenu()
        
        # 设置菜单的现代化样式
        self.setupMenuStyle()
        
        # 显示主窗口
        self.show_action = QAction("显示主窗口", self)
        self.show_action.triggered.connect(self.showMainWindow)
        self.tray_menu.addAction(self.show_action)
        
        self.tray_menu.addSeparator()
        
        # 打开设置
        self.settings_action = QAction("打开设置", self)
        self.settings_action.triggered.connect(self.openSettings)
        self.tray_menu.addAction(self.settings_action)
        
        self.tray_menu.addSeparator()
        
        # 退出程序
        self.exit_action = QAction("退出程序", self)
        self.exit_action.triggered.connect(self.exitApplication)
        self.tray_menu.addAction(self.exit_action)
        
        self.setContextMenu(self.tray_menu)
        

    def setupMenuStyle(self):
        """设置菜单的现代化样式"""
        # 获取当前主题颜色
        theme_color = SiGlobal.siui.colors["THEME"]
        bg_color = SiGlobal.siui.colors["BACKGROUND_COLOR"]
        border_color = SiGlobal.siui.colors["BORDER_COLOR"]
        text_color = SiGlobal.siui.colors["TEXT_B"]
        hover_color = SiGlobal.siui.colors["BUTTON_HOVER"]
        
        # 现代化的菜单样式
        menu_style = f"""
        QMenu {{
            background-color: {bg_color};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 6px 0px;
            font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
            font-size: 13px;
            font-weight: 400;
            min-width: 140px;
            max-width: 160px;
        }}
        
        QMenu::item {{
            background-color: transparent;
            color: {text_color};
            padding: 8px 16px;
            margin: 1px 4px;
            border-radius: 4px;
            min-height: 20px;
            font-weight: 400;
        }}
        
        QMenu::item:selected {{
            background-color: {hover_color};
            color: {text_color};
        }}
        
        QMenu::item:pressed {{
            background-color: {theme_color};
            color: {bg_color};
        }}
        
        QMenu::separator {{
            height: 1px;
            background-color: {border_color};
            margin: 4px 8px;
        }}
        
        QMenu::item:disabled {{
            color: #888888;
            background-color: transparent;
        }}
        """
        
        self.tray_menu.setStyleSheet(menu_style)
        
    def updateMenuOnThemeChange(self):
        """当主题变化时更新菜单样式"""
        # 这个方法可以在主题切换时被调用
        if hasattr(self, 'tray_menu'):
            self.setupMenuStyle()
            
    def refreshTrayMenu(self):
        """刷新托盘菜单样式"""
        self.setupMenuStyle()
        
        # 更新托盘图标本身
        self.createTrayIcon()
        
    def onTrayIconActivated(self, reason):
        """处理托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            # 双击托盘图标显示/隐藏主窗口
            if self.parent_window.isVisible():
                self.parent_window.hide()
            else:
                self.showMainWindow()
        elif reason == QSystemTrayIcon.Trigger:
            # 单击托盘图标显示主窗口
            self.showMainWindow()
            
    def showMainWindow(self):
        """显示主窗口"""
        if self.parent_window:
            self.parent_window.show()
            self.parent_window.raise_()
            self.parent_window.activateWindow()
            
    def openSettings(self):
        """打开设置面板"""
        if self.parent_window:
            self.showMainWindow()
            # 打开设置面板
            self.parent_window.header_panel.settings_button.setChecked(True)
            
    def exitApplication(self):
        """退出应用程序"""
        if self.parent_window:
            self.parent_window.reallyClose()


class TODOApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 窗口周围留白，供阴影使用
        self.padding = 48
        
        # 窗口拖动相关变量
        self._is_dragging_window = False
        self._drag_start_pos = QPoint()  # 鼠标按下时的位置
        self._window_start_pos = QPoint()  # 窗口拖动开始时的位置
        
        self.fixed_position = QPoint(SiGlobal.todo_list.settings_parser.options["FIXED_POSITION_X"],
                                     SiGlobal.todo_list.settings_parser.options["FIXED_POSITION_Y"])

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 初始化工具提示窗口
        SiGlobal.siui.windows["TOOL_TIP"] = ToolTipWindow()
        SiGlobal.siui.windows["TOOL_TIP"].show()
        SiGlobal.siui.windows["TOOL_TIP"].hide_()
        SiGlobal.siui.windows["MAIN_WINDOW"] = self

        # 创建移动动画
        self.move_animation = SiExpAnimation(self)
        self.move_animation.setFactor(1 / 4)
        self.move_animation.setBias(1)
        self.move_animation.setCurrent([self.x(), self.y()])
        self.move_animation.ticked.connect(self._onMoveAnimationTicked)

        # 创建垂直容器
        self.container_v = SiDenseVContainer(self)
        # 让内部容器比窗口左右各缩进 self.padding，以便为阴影留出空间
        self.container_v.setFixedWidth(500 - 2 * self.padding)
        self.container_v.setSpacing(0)
        self.container_v.setShrinking(True)
        self.container_v.setAlignCenter(True)

        # 构建界面
        # 头
        self.header_panel = AppHeaderPanel(self)
        self.header_panel.setFixedWidth(500 - 2 * self.padding)
        self.header_panel.setFixedHeight(48 + 12)

        # 设置面板
        self.settings_panel = SettingsPanel(self)
        self.settings_panel.setFixedWidth(500 - 2 * self.padding)
        self.settings_panel.adjustSize()

        self.settings_panel_placeholder = SiLabel(self)
        self.settings_panel_placeholder.setFixedHeight(12)
        self._onSettingsButtonToggled(False)

        # 添加新待办面板
        self.add_todo_panel = AddNewTODOPanel(self)
        self.add_todo_panel.setFixedWidth(500 - 2 * self.padding)
        self.add_todo_panel.adjustSize()

        self.add_todo_panel_placeholder = SiLabel(self)
        self.add_todo_panel_placeholder.setFixedHeight(12)
        self._onAddTODOButtonToggled(False)

        # 全部待办面板
        self.todo_list_panel = TODOListPanel(self)
        self.todo_list_panel.setFixedWidth(500 - 2 * self.padding)

        self.todo_list_panel_placeholder = SiLabel(self)
        self.todo_list_panel_placeholder.setFixedHeight(12)
        self._onShowTODOButtonToggled(True)

        # <- 添加到垂直容器
        self.container_v.addWidget(self.header_panel)
        self.container_v.addWidget(self.settings_panel)
        self.container_v.addWidget(self.settings_panel_placeholder)
        self.container_v.addWidget(self.add_todo_panel)
        self.container_v.addWidget(self.add_todo_panel_placeholder)
        self.container_v.addWidget(self.todo_list_panel)
        self.container_v.addWidget(self.todo_list_panel_placeholder)

        # 绑定界面信号
        self.header_panel.unfold_button.toggled.connect(self._onShowTODOButtonToggled)
        self.header_panel.add_todo_button.toggled.connect(self._onAddTODOButtonToggled)
        self.header_panel.settings_button.toggled.connect(self._onSettingsButtonToggled)
        self.header_panel.exit_button.clicked.connect(self.reallyClose)

        self.settings_panel.resized.connect(self._onTODOWindowResized)
        self.add_todo_panel.resized.connect(self._onTODOWindowResized)
        self.todo_list_panel.resized.connect(self._onTODOWindowResized)

        self.add_todo_panel.confirm_button.clicked.connect(self._onAddTODOConfirmButtonClicked)
        self.add_todo_panel.cancel_button.clicked.connect(self._onAddTODOCancelButtonClicked)

        self.todo_list_panel.todoAmountChanged.connect(self._onTODOAmountChanged)

        # 创建阴影效果，但要小心处理以避免分层窗口错误
        try:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setColor(QColor(0, 0, 0, 60))  # 降低透明度避免冲突
            shadow.setOffset(0, 2)  # 轻微偏移
            shadow.setBlurRadius(24)  # 减小模糊半径
            # 仅对内部容器应用阴影，避免阴影区域超出窗口导致 UpdateLayeredWindowIndirect 失败
            self.container_v.setGraphicsEffect(shadow)
        except Exception as e:
            print(f"无法设置阴影效果: {e}")
            # 如果阴影设置失败，继续运行但不使用阴影

        self.resize(500, 800)
        
        # 确保初始位置有效
        init_x, init_y = self._constrainToScreen(self.fixed_position.x(), self.fixed_position.y())
        self.move(init_x, init_y)
        # 如果位置被约束了，更新固定位置
        if (init_x, init_y) != (self.fixed_position.x(), self.fixed_position.y()):
            self.fixed_position = QPoint(init_x, init_y)
        
        # 设置初始透明度
        initial_opacity = SiGlobal.todo_list.settings_parser.options.get("WINDOW_OPACITY", 95)
        self.setWindowOpacity(initial_opacity / 100.0)
        
        SiGlobal.siui.reloadAllWindowsStyleSheet()

        # 读取 todos.ini 添加到待办
        for todo in SiGlobal.todo_list.todos_parser.todos:
            self.todo_list_panel.addTODO(todo)
            
        # 创建系统托盘
        self.setupSystemTray()

    def setupSystemTray(self):
        """设置系统托盘"""
        # 检查系统是否支持托盘
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("系统托盘不可用")
            return
            
        # 创建系统托盘图标
        self.tray_icon = SystemTrayIcon(self)
        
        # 设置托盘图标工具提示
        self.tray_icon.setToolTip("My TODOs - 待办事项管理")
        
        # 显示托盘图标
        self.tray_icon.show()

    def adjustSize(self):
        h = (self.header_panel.height() + 12 +
             self.settings_panel.height() + 12 +
             self.add_todo_panel.height() + 12 +
             self.todo_list_panel.height() +
             2 * self.padding)
        self.resize(self.width(), h)
        # 更新内部容器宽度，确保阴影始终有足够留白
        self.container_v.setFixedWidth(self.width() - 2 * self.padding)
        self.container_v.adjustSize()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        # 保持容器在窗口内居中，并为阴影留边距
        self.container_v.move(self.padding, self.padding)
        # 根据窗口大小同步调整内部容器宽度
        self.container_v.setFixedWidth(self.width() - 2 * self.padding)
        
        # 窗口大小改变后，检查位置是否仍然有效
        try:
            current_pos = self.pos()
            new_x, new_y = self._constrainToScreen(current_pos.x(), current_pos.y())
            if (new_x, new_y) != (current_pos.x(), current_pos.y()):
                self.move(new_x, new_y)
        except Exception as e:
            print(f"窗口大小调整后的位置检查失败: {e}")

    def _onTODOWindowResized(self, size):
        w, h = size
        self.adjustSize()

    def _onShowTODOButtonToggled(self, state):
        if state is True:
            self.todo_list_panel_placeholder.setFixedHeight(12)
            self.todo_list_panel.adjustSize()
        else:
            self.todo_list_panel_placeholder.setFixedHeight(0)
            self.todo_list_panel.resize(self.todo_list_panel.width(), 0)

    def _onAddTODOButtonToggled(self, state):
        if state is True:
            self.add_todo_panel_placeholder.setFixedHeight(12)
            self.add_todo_panel.adjustSize()
        else:
            self.add_todo_panel_placeholder.setFixedHeight(0)
            self.add_todo_panel.resize(self.add_todo_panel.width(), 0)

    def _onSettingsButtonToggled(self, state):
        if state is True:
            self.settings_panel_placeholder.setFixedHeight(12)
            self.settings_panel.adjustSize()
        else:
            self.settings_panel_placeholder.setFixedHeight(0)
            self.settings_panel.resize(self.settings_panel.width(), 0)

    def _onTODOAmountChanged(self, amount):
        if amount == 0:
            self.header_panel.unfold_button.attachment().setText("没有待办")
        else:
            self.header_panel.unfold_button.attachment().setText(f"{amount}个待办事项")
        self.header_panel.unfold_button.adjustSize()

    def _onAddTODOConfirmButtonClicked(self):
        text = self.add_todo_panel.text_edit.toPlainText()
        self.add_todo_panel.text_edit.setText("")
        self.header_panel.add_todo_button.setChecked(False)

        while text[-1:] == "\n":
            text = text[:-1]

        if text == "":
            return

        self.todo_list_panel.addTODO(text)

    def _onAddTODOCancelButtonClicked(self):
        self.add_todo_panel.text_edit.setText("")
        self.header_panel.add_todo_button.setChecked(False)

    def _constrainToScreen(self, x, y):
        """
        约束窗口位置在屏幕边界内
        :param x: 目标x坐标
        :param y: 目标y坐标
        :return: 约束后的(x, y)坐标
        """
        # 获取屏幕几何信息
        desktop = QDesktopWidget()
        screen_rect = desktop.availableGeometry()
        
        # 计算最小和最大允许位置
        min_x = screen_rect.left()
        min_y = screen_rect.top()
        max_x = screen_rect.right() - self.width()
        max_y = screen_rect.bottom() - self.height()
        
        # 约束坐标
        constrained_x = max(min_x, min(max_x, x))
        constrained_y = max(min_y, min(max_y, y))
        
        return constrained_x, constrained_y

    def moveTo(self, x, y, use_animation=True):
        """
        移动窗口到指定位置
        :param x: 目标x坐标
        :param y: 目标y坐标
        :param use_animation: 是否使用动画，拖动时应该设为False
        """
        # 约束位置在屏幕边界内
        x, y = self._constrainToScreen(x, y)
        
        if use_animation and not self._is_dragging_window:
            self.move_animation.setTarget([x, y])
            self.move_animation.try_to_start()
        else:
            # 直接移动，不使用动画（用于拖动时）
            try:
                self.move(x, y)
            except Exception as e:
                print(f"窗口移动失败: {e}")
                # 重试一次，但忽略异常
                try:
                    super().move(x, y)
                except:
                    pass

    def moveEvent(self, a0):
        super().moveEvent(a0)
        x, y = a0.pos().x(), a0.pos().y()
        self.move_animation.setCurrent([x, y])

    def _onMoveAnimationTicked(self, pos):
        # 仅在非拖动状态下更新位置
        if not self._is_dragging_window:
            try:
                x, y = int(pos[0]), int(pos[1])
                # 先约束坐标再移动
                x, y = self._constrainToScreen(x, y)
                self.move(x, y)
                if not SiGlobal.todo_list.position_locked:
                    self.fixed_position = self.pos()
            except Exception as e:
                print(f"动画移动失败: {e}")
                # 停止动画以避免持续错误
                self.move_animation.stop()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            # 检查位置锁定状态
            if SiGlobal.todo_list.position_locked:
                return
                
            # 仅当点击在标题栏区域（包含顶部留白和头部面板）时，才允许拖动窗口，
            # 以避免与滑条等可交互控件的拖动冲突。
            header_bottom = self.padding + self.header_panel.height()
            if event.pos().y() <= header_bottom:
                self._is_dragging_window = True
                self._drag_start_pos = event.globalPos()  # 记录全局鼠标位置
                self._window_start_pos = self.pos()  # 记录窗口当前位置
            else:
                self._is_dragging_window = False
            event.accept()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not (event.buttons() & Qt.LeftButton):
            return

        # 仅在拖动窗口状态下移动窗口
        if self._is_dragging_window:
            # 计算鼠标移动的偏移量
            mouse_offset = event.globalPos() - self._drag_start_pos
            # 计算新的窗口位置
            new_pos = self._window_start_pos + mouse_offset
            x, y = new_pos.x(), new_pos.y()
            # 直接移动窗口，不使用动画
            self.moveTo(x, y, use_animation=False)

    def mouseReleaseEvent(self, a0):
        # 结束窗口拖动
        if self._is_dragging_window:
            self._is_dragging_window = False
            
            # 如果位置被锁定，恢复到固定位置
            if SiGlobal.todo_list.position_locked:
                self.moveTo(self.fixed_position.x(), self.fixed_position.y(), use_animation=True)
            else:
                # 更新固定位置为当前位置
                self.fixed_position = self.pos()

    def closeEvent(self, a0):
        # 如果有系统托盘，隐藏到托盘而不是退出
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            # 显示托盘消息提示
            self.tray_icon.showMessage(
                "My TODOs",
                "应用程序已最小化到系统托盘",
                QSystemTrayIcon.Information,
                2000
            )
            a0.ignore()
            return
            
        # 如果没有托盘或者是真正的退出，执行正常的关闭流程
        self.reallyClose()
        
    def reallyClose(self):
        """真正的关闭程序"""
        # 获取当前待办，并写入 todos.ini
        todos = [widget.text_label.text() for widget in self.todo_list_panel.body().widgets_top]
        SiGlobal.todo_list.todos_parser.todos = todos
        SiGlobal.todo_list.todos_parser.write()

        # 写入设置到 options.ini
        SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION_X", self.fixed_position.x())
        SiGlobal.todo_list.settings_parser.write()
        SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION_Y", self.fixed_position.y())
        SiGlobal.todo_list.settings_parser.write()

        # 隐藏托盘图标
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()

        SiGlobal.siui.windows["TOOL_TIP"].close()
        QCoreApplication.quit()
