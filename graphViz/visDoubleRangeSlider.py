# -*- coding: utf-8 -*-
import qtpy
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

# Avoid error and crash in qt5
if qtpy.PYQT5:
    import cgitb

    cgitb.enable(format="text")


class RangeSlider(QtWidgets.QSlider):
    """ A slider for ranges.
    
        This class provides a dual-slider for ranges, where there is a defined
        maximum and minimum, as is a normal slider, but instead of having a
        single slider value, there are 2 slider values.
        
        This class emits the same signals as the QSlider base class, with the 
        exception of valueChanged. 

        In addition, two new signals are emitted to catch the movement of 
        each handle, lowValueChanged(int) and highValueChanged(int).
    """

    lowValueChanged = QtCore.Signal(float)
    highValueChanged = QtCore.Signal(float)
    rangeValueChanged = QtCore.Signal(float, float)

    def __init__(self, stylestr=None, stylestr2=None, parent=None):
        super(RangeSlider, self).__init__(parent=None)

        self._low = self.minimum()
        self._high = self.maximum()
        if stylestr is None and stylestr2 is None:
            self.setObjectName("rangeSlider")
            self.stylestr = """
            QSlider {
                border: 0px solid #3A3939;
            }
            QSlider#rangeSlider::groove:horizontal {
                border: 1px solid #3A3939;
                height: 8px;
                background: #201F1F;
                margin: 2px 0;
                border-radius: 4px;
            }

            QSlider#rangeSlider::handle:horizontal {
                
                border: 0px solid #3A3939;
                background: QConicalGradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(255, 255, 255, 255), stop:0.373979 rgba(255, 255, 255, 255), stop:0.373991 rgba(33, 30, 255, 255), stop:0.624018 rgba(33, 30, 255, 255), stop:0.624043 rgba(255, 0, 0, 255), stop:1 rgba(255, 0, 0, 255));
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }

            QSlider#rangeSlider::groove:vertical {
                border: 1px solid #3A3939;
                width: 8px;
                background: #201F1F;
                margin: 0 0px;
                border-radius: 4px;
            }

            QSlider#rangeSlider::handle:vertical {
                background: QConicalGradient(cx:1, cy:0.5, angle:0,
                stop:0 rgba(255, 255, 255, 0),
                stop:0.373979 rgba(255, 255, 255, 0),
                stop:0.373991 rgba(33, 30, 255, 255),
                stop:0.624018 rgba(33, 30, 255, 255),
                stop:0.624043 rgba(255, 0, 0, 0), stop:1 rgba(255, 0, 0, 0));
                
                border: 0px solid #3A3939;
                width: 14px;
                height: 14px;
                margin: 0 -4px;
                border-radius: 0px;
            }
            /*QWidget#rangeSlider{background:transparent;border:opx;};*/
            """

            self.stylestr2 = """
            QSlider {
                border: 0px solid #3A3939;
            }
            QSlider#rangeSlider::groove:horizontal {
                border: 1px solid #3A3939;
                height: 8px;
                background: #201F1F;
                margin: 2px 0;
                border-radius: 4px;
            }

            QSlider#rangeSlider::handle:horizontal {
                
                border: 0px solid #3A3939;
                background: QConicalGradient(cx:0.5, cy:0.5, angle:180, stop:0 rgba(255, 255, 255, 255),
                stop:0.373979 rgba(255, 255, 255, 255),
                stop:0.373991 rgba(33, 30, 255, 255),
                stop:0.624018 rgba(33, 30, 255, 255),
                stop:0.624043 rgba(255, 0, 0, 255),
                stop:1 rgba(255, 0, 0, 255));
                
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }

            QSlider#rangeSlider::groove:vertical {
                border: 1px solid #3A3939;
                width: 8px;
                background: #201F1F;
                margin: 0 0px;
                border-radius: 4px;
            }

            QSlider#rangeSlider::handle:vertical {
                background: QConicalGradient(cx:1, cy:0.5, angle:0,
                stop:0 rgba(255, 255, 255, 0),
                stop:0.373979 rgba(255, 255, 255, 0),
                stop:0.373991 rgba(33, 30, 255, 255),
                stop:0.624018 rgba(33, 30, 255, 255),
                stop:0.624043 rgba(255, 0, 0, 0), stop:1 rgba(255, 0, 0, 0));
                
                border: 0px solid #3A3939;
                width: 14px;
                height: 14px;
                margin: 0 -4px;
                border-radius: 0px;
            }
            /*QWidget#rangeSlider{background:transparent;border:opx;};*/
            """
        else:
            self.setObjectName("rangeSlider")
            self.stylestr = stylestr
            self.stylestr2 = stylestr2
        # self.setStyleSheet('''''')
        # self.setStyleSheet(self.stylestr)
        self.pressed_control = QtWidgets.QStyle.SC_None
        self.hover_control = QtWidgets.QStyle.SC_None
        self.click_offset = 0

        # -1 for the low, 1 for the high, 0 for both
        self.active_slider = -1

    def lowValue(self):
        return self._low

    def setLowValue(self, low):
        if low < self.minimum():
            low = self.minimum()
        if low == self._low:
            return

        self._low = low
        self.update()

        if self.hasTracking():
            # self.lowValueChanged.emit(self._low)
            self.rangeValueChanged.emit(self._low, self._high)

    def highValue(self):
        return self._high

    def setHighValue(self, high):
        if high > self.maximum():
            high = self.maximum()
        if high == self._high:
            return

        self._high = high
        self.update()

        if self.hasTracking():
            # self.highValueChanged.emit(self._high)
            self.rangeValueChanged.emit(self._low, self._high)

    def paintEvent(self, event):
        # based on http://qt.gitorious.org/qt/qt/blobs/master/src/gui/widgets/qslider.cpp

        painter = QtGui.QPainter(self)
        style = QtWidgets.QApplication.style()

        for i, value in enumerate([self._low, self._high]):
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            gr = style.subControlRect(style.CC_Slider, opt, style.SC_SliderGroove, self)
            sr = style.subControlRect(style.CC_Slider, opt, style.SC_SliderHandle, self)

            if self.orientation() == QtCore.Qt.Horizontal:
                handle_length = sr.width()
                slider_length = gr.width()
                slider_min = gr.x()
                slider_max = gr.right() - handle_length + 1
            else:
                handle_length = sr.height()
                slider_length = gr.height()
                slider_min = gr.y()
                slider_max = gr.bottom() - handle_length + 1

            # print "min/max", self.minimum(), self.maximum()
            # print "slider", slider_max, slider_min, handle_length
            # print "value", value

            opt.subControls = (
                QtWidgets.QStyle.SC_SliderGroove | QtWidgets.QStyle.SC_SliderHandle
            )

            # draw the first slider with inverted appearance, then the second
            # slider drawn on top of the existing ones
            if i == 0:
                if self.orientation() == QtCore.Qt.Horizontal:
                    opt.upsideDown = not self.invertedAppearance()
                else:
                    opt.upsideDown = self.invertedAppearance()

                if self.orientation() == QtCore.Qt.Horizontal:
                    opt.sliderValue = value - self.minimum()
                    opt.sliderPosition = self.minimum() + (self.maximum() - value)

                    # print ("old", opt.rect.x(), opt.rect.width())
                    opt.rect.setX(slider_min)
                    opt.rect.setWidth(slider_length)
                    # print "new", opt.rect.x(), opt.rect.width()

                else:
                    opt.sliderValue = value - self.minimum()
                    opt.sliderPosition = self.minimum() + (self.maximum() - value)
                    # print "old", opt.rect.y(), opt.rect.height()
                    opt.rect.setY(slider_min)
                    opt.rect.setHeight(slider_length)
                    # print "new", opt.rect.y(), opt.rect.height()
                self.setStyleSheet(self.stylestr)
                # print "opt", opt.sliderValue, opt.sliderPosition, opt.upsideDown

            else:
                # do not highlight the second part when has focus to avoid
                # drawing of partially overlapped semi-transparent backgrounds
                opt.state &= ~QtWidgets.QStyle.State_HasFocus

                opt.sliderValue = 0
                opt.sliderPosition = self.minimum()

                if self.orientation() == QtCore.Qt.Horizontal:
                    opt.upsideDown = self.invertedAppearance()

                    pos = style.sliderPositionFromValue(
                        0,
                        self.maximum() - self.minimum(),
                        value - self.minimum(),
                        slider_max - slider_min - 4,
                        opt.upsideDown,
                    )

                    # print "pos", pos
                    # print "old", opt.rect.x(), opt.rect.width()
                    opt.rect.setX(pos + 3)
                    opt.rect.setWidth(slider_max - pos + handle_length - 3)
                    # print "new", opt.rect.x(), opt.rect.width()

                else:
                    opt.upsideDown = not self.invertedAppearance()

                    pos = style.sliderPositionFromValue(
                        0,
                        self.maximum() - self.minimum(),
                        self.maximum() - value,
                        slider_max - slider_min - 4,
                        opt.upsideDown,
                    )

                    # print "pos", pos
                    # print "old", opt.rect.y(), opt.rect.height()
                    opt.rect.setY(slider_min - 1)
                    opt.rect.setHeight(slider_min + slider_length - pos - 2)
                    # print "new", opt.rect.y(), opt.rect.height()

                # print "opt", opt.sliderValue, opt.sliderPosition, opt.upsideDown
                self.setStyleSheet(self.stylestr2)

            if self.tickPosition() != self.NoTicks:
                opt.subControls |= QtWidgets.QStyle.SC_SliderTickmarks

            if self.pressed_control:
                opt.activeSubControls = self.pressed_control
                opt.state |= QtWidgets.QStyle.State_Sunken
            else:
                opt.activeSubControls = self.hover_control

            style.drawComplexControl(QtWidgets.QStyle.CC_Slider, opt, painter, self)

    def mousePressEvent(self, event):
        event.accept()

        style = QtWidgets.QApplication.style()
        button = event.button()

        # In a normal slider control, when the user clicks on a point in the
        # slider's total range, but not on the slider part of the control the
        # control would jump the slider value to where the user clicked.
        # For this control, clicks which are not direct hits will slide both
        # slider parts

        if button:
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            self.active_slider = 0
            mid = (self.maximum() - self.minimum()) / 2.0

            for i, value in enumerate([self._low, self._high]):
                opt.sliderPosition = value
                hit = style.hitTestComplexControl(
                    style.CC_Slider, opt, event.pos(), self
                )

                if hit == style.SC_SliderHandle:
                    self.pressed_control = hit

                    # if both handles are close together, avoid locks
                    # choosing the one with more empty space near it
                    if self._low + 2 >= self._high:
                        self.active_slider = 1 if self._high < mid else -1
                    else:
                        self.active_slider = -1 if i == 0 else 1
                    self.triggerAction(self.SliderMove)
                    self.setRepeatAction(self.SliderNoAction)
                    self.setSliderDown(True)
                    break

            if self.active_slider == 0:
                self.pressed_control = QtWidgets.QStyle.SC_SliderHandle
                self.click_offset = self.__pixelPosToRangeValue(
                    self.__pick(event.pos())
                )
                self.triggerAction(self.SliderMove)
                self.setRepeatAction(self.SliderNoAction)
                self.setSliderDown(True)
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if self.pressed_control != QtWidgets.QStyle.SC_SliderHandle:
            event.ignore()
            return

        self.setSliderDown(False)
        return QtWidgets.QSlider.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.pressed_control != QtWidgets.QStyle.SC_SliderHandle:
            event.ignore()
            return

        event.accept()
        new_pos = self.__pixelPosToRangeValue(self.__pick(event.pos()))
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)

        old_click_offset = self.click_offset
        self.click_offset = new_pos

        if self.active_slider == 0:
            offset = new_pos - old_click_offset
            new_low = self._low + offset
            new_high = self._high + offset

            if new_low < self.minimum():
                diff = self.minimum() - new_low
                new_low += diff
                new_high += diff
            if new_high > self.maximum():
                diff = self.maximum() - new_high
                new_low += diff
                new_high += diff

            self.setLowValue(new_low)
            self.setHighValue(new_high)

        elif self.active_slider < 0:
            if new_pos > self._high:
                new_pos = self._high
            self.setLowValue(new_pos)

        else:
            if new_pos < self._low:
                new_pos = self._low
            self.setHighValue(new_pos)

        # if self.hasTracking():
        #    self.emit(QtCore.SIGNAL('sliderMoved(int)'), new_pos)

    def __pick(self, pt):
        if self.orientation() == QtCore.Qt.Horizontal:
            return pt.x()
        else:
            return pt.y()

    def __pixelPosToRangeValue(self, pos):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        style = QtWidgets.QApplication.style()

        gr = style.subControlRect(style.CC_Slider, opt, style.SC_SliderGroove, self)
        sr = style.subControlRect(style.CC_Slider, opt, style.SC_SliderHandle, self)

        if self.orientation() == QtCore.Qt.Horizontal:
            handle_length = sr.width()
            slider_min = gr.x() + handle_length / 2
            slider_max = gr.right() - handle_length / 2 + 1
        else:
            handle_length = sr.height()
            slider_min = gr.y() + handle_length / 2
            slider_max = gr.bottom() - handle_length / 2 + 1

        return self.minimum() + style.sliderValueFromPosition(
            0,
            self.maximum() - self.minimum(),
            pos - slider_min,
            slider_max - slider_min,
            opt.upsideDown,
        )
