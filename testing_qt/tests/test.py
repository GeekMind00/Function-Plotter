import pytest

from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import plotterTest


@pytest.fixture
def app(qtbot):
    testApp = plotterTest.Window()
    qtbot.addWidget(testApp)

    return testApp


def test_inputArray_pass_after_click(app, qtbot):
    app.equation.setText("3*x**3+6*x**2+x")
    app.minInput.setText("0")
    app.maxInput.setText("10")

    x = np.linspace(0, 10, 100)
    y = 3*x**3+6*x**2+x

    qtbot.mouseClick(app.plotButton, Qt.LeftButton)
    assert sum(x == app.x) == len(x) and sum(y == app.y) == len(y)


def test_inputArray_fail_after_click(app, qtbot):
    app.equation.setText("3*x**3+6*x**2+x")
    app.minInput.setText("0")
    app.maxInput.setText("10")

    x = np.linspace(0, 10, 100)
    y = 3*x**3+6*x**4+x

    qtbot.mouseClick(app.plotButton, Qt.LeftButton)
    assert sum(x == app.x) == len(x) and sum(y == app.y) != len(y)
