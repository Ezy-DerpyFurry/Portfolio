#include <Python.h>
#include <iostream>
#include <vector>
#include <string>
#include <termios.h>
#include <unistd.h>
#include <cstdlib>
#include <memory>
#include <utility>
#include <fcntl.h>

inline void clear() {
    std::cout << "\033[2J\033[H";
}

// Start of selector menu \\.
struct menuOptions {
    const std::vector<std::pair<std::string, std::string>> list{};
    int index = 0;
    const std::string title = "";
    const std::string selector = "";
    const std::string type = "";
    int min = 0;
    int max = 0;
};

class TerminalInput {
public:
    TerminalInput() {
        tcgetattr(STDIN_FILENO, &oldArgs);
        newArgs = oldArgs;
        newArgs.c_lflag &= ~(ICANON | ECHO);
        tcsetattr(STDIN_FILENO, TCSANOW, &newArgs);

        old_flags_ = fcntl(STDIN_FILENO, F_GETFL, 0);
        fcntl(STDIN_FILENO, F_SETFL, old_flags_ | O_NONBLOCK);
    }

    ~TerminalInput() {
        tcsetattr(STDIN_FILENO, TCSANOW, &oldArgs);
        fcntl(STDIN_FILENO, F_SETFL, old_flags_);
    }

    int getKey() {
        char c;
        int n = read(STDIN_FILENO, &c, 1);
        if (n == 1) return (int)c;
        return -1;
    }

private:
    struct termios oldArgs, newArgs;
    int old_flags_;
};

class TerminalRawMode {
public:
    TerminalRawMode() {
        tcgetattr(STDIN_FILENO, &oldArgs);
        newArgs = oldArgs;
        newArgs.c_lflag &= ~(ICANON | ECHO);
        tcsetattr(STDIN_FILENO, TCSANOW, &newArgs);
    }

    ~TerminalRawMode() {
        tcsetattr(STDIN_FILENO, TCSANOW, &oldArgs);
    }

private:
    struct termios oldArgs, newArgs;
};

void printMenu(const menuOptions& options) {
    clear();
    std::cout << options.title << "\n";

    if (options.type == "list") {
        for (int i = 0; i < options.list.size(); ++i) {
            if (i == options.index)
                std::cout << options.selector << options.list[i].first << options.list[i].second << "\n";
            else
                std::cout << "  " << options.list[i].first << "\n";
        }
    } else if (options.type == "slider") {
        std::string slider;
        for (int i = options.min; i <= options.max; i++) {
            if (i == options.index)
                slider += "#";
            else {
                if (i < options.index)
                    slider += '#';
                else
                    slider += '-';
            }
        }
        std::cout << "||" << slider << "|| " << options.index << '\n';
    } else if (options.type == "buttons") {
        std::string buttonDisplay;
        for (int i = 0; i < options.list.size(); i++) {
            if (i == options.index) 
                buttonDisplay += " [" + options.list[i].first + "] ";
            else
                buttonDisplay += " " + options.list[i].first + " ";
        }
        std::cout << buttonDisplay << options.list[options.index].second << '\n';
    }
}

std::string terminalButtons(const std::vector<std::pair<std::string, std::string>>& buttons, const std::string& title) {
    TerminalRawMode termGuard;

    int index = 0;
    char c;

    printMenu({.list=buttons, .index=index, .title=title, .type="buttons"});

    while (read(STDIN_FILENO, &c, 1) == 1) {
        if (c == 'q') return "None";

        if (c == 'a' || c == 68) {
            index = (index - 1 + buttons.size()) % buttons.size();
        }
        else if (c == 'd' || c == 67) {
            index = (index + 1) % buttons.size();
        }
        else if (c == '\n') {
            return buttons[index].first;
        }

        printMenu({.list=buttons, .index=index, .title=title, .type="buttons"});
    }

    return "None";
}

int terminalSlider(int& min, int& max, std::string& title) {
    if (max < min) max = min;

    TerminalRawMode termGuard;

    int index = 0;
    char c;

    printMenu({.index=index, .title=title, .type="slider", .min=min, .max=max});

    while (read(STDIN_FILENO, &c, 1) == 1) {
        if (c == 'q') return -1;

        if (c == 'd' || c == 67) {
            index = ((index - min + 1) % (max - min + 1)) + min;
        }
        else if (c == 'a' || c == 68) {
            index = ((index - min - 1 + (max - min + 1)) % (max - min + 1)) + min;
        }
        else if (c == '\n') {
            return index;
        }

        printMenu({.index=index, .title=title, .type="slider", .min=min, .max=max});
    }
    
    return -1;
}

std::string terminalMenu(const std::vector<std::pair<std::string, std::string>>& list, const std::string& title, const std::string& selector) {
    TerminalRawMode termGuard;

    int index = 0;
    char c;

    printMenu({.list=list, .index=index, .title=title, .selector=selector, .type="list"});

    while (read(STDIN_FILENO, &c, 1) == 1) {

        if (c == 'q') {
            return "None";
        }
        if (c == 'w' || c == 65) {
            index = (index - 1 + list.size()) % list.size();
        }
        else if (c == 's' || c == 66) {
            index = (index + 1) % list.size();
        }
        else if (c == '\n' || c == 67) {
            return list[index].first;
        }

        printMenu({.list=list, .index=index, .title=title, .selector=selector, .type="list"});
    }

    return "None";
}
// End of selector menu \\.

static PyObject* executeCommand(PyObject* self, PyObject* args) {
    const char* baseCommand;

    if (!PyArg_ParseTuple(args, "s", &baseCommand)) return nullptr;

    FILE* pipe = popen(baseCommand, "r");
    if (!pipe) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to run");
        return nullptr;
    }

    std::string result;
    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        result += buffer;
    }

    pclose(pipe);
    return PyUnicode_FromString(result.c_str());
}

static TerminalInput* terminalInput = nullptr;
bool inputBypass = false;

static PyObject* createSlider(PyObject* self, PyObject* args) {
    int min;
    int max;
    const char* baseTitle;

    if (!PyArg_ParseTuple(args, "iis", &min, &max, &baseTitle)) return nullptr;

    if (terminalInput && !inputBypass) {
        PyErr_SetString(PyExc_RuntimeError, "You cannot use widgets while startInput add the line (terminalui.bypassInputBlock(True)) at the top of your code.");
        return nullptr;
    }

    std::string title(baseTitle);
    return PyLong_FromLong(terminalSlider(min, max, title));
}

static PyObject* createSelector(PyObject* self, PyObject* args) {
    PyObject* pyOptions;
    const char* baseTitle;
    const char* baseSelector;

    if (!PyArg_ParseTuple(args, "Oss", &pyOptions, &baseTitle, &baseSelector)) return nullptr;

    if (terminalInput && !inputBypass) {
        PyErr_SetString(PyExc_RuntimeError, "You cannot use widgets while startInput add the line (terminalui.bypassInputBlock(True)) at the top of your code.");
        return nullptr;
    }

    if (!PyDict_Check(pyOptions)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return nullptr;
    }

    std::vector<std::pair<std::string, std::string>> options;

    PyObject *key, *value;
    Py_ssize_t pos = 0;

    while (PyDict_Next(pyOptions, &pos, &key, &value)) {
        if (!PyUnicode_Check(key) || !PyUnicode_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "Dictionary keys and values must be strings");
            return nullptr;
        }
        std::string keyStr = PyUnicode_AsUTF8(key); 
        std::string valueStr = PyUnicode_AsUTF8(value);
        options.push_back(std::make_pair(keyStr, valueStr));
    }

    std::string title(baseTitle);
    std::string selector(baseSelector);
    std::string choice = terminalMenu(options, title.c_str(), selector.c_str());

    return PyUnicode_FromString(choice.c_str());
}

static PyObject* createButtons(PyObject* self, PyObject* args) {
    PyObject* pyOptions;
    const char* baseTitle;

    if (!PyArg_ParseTuple(args, "Os", &pyOptions, &baseTitle)) return nullptr;

    if (terminalInput && !inputBypass) {
        PyErr_SetString(PyExc_RuntimeError, "You cannot use widgets while startInput add the line (terminalui.bypassInputBlock(True)) at the top of your code.");
        return nullptr;
    }

    if (!PyDict_Check(pyOptions)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return nullptr;
    }

    std::vector<std::pair<std::string, std::string>> options;

    PyObject *key, *value;
    Py_ssize_t pos = 0;

    while (PyDict_Next(pyOptions, &pos, &key, &value)) {
        if (!PyUnicode_Check(key) || !PyUnicode_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "Dictionary keys and values must be strings");
            return nullptr;
        }
        std::string keyStr = PyUnicode_AsUTF8(key); 
        std::string valueStr = PyUnicode_AsUTF8(value);
        options.push_back(std::make_pair(keyStr, valueStr));
    }

    std::string title(baseTitle);
    std::string choice = terminalButtons(options, title.c_str());

    return PyUnicode_FromString(choice.c_str());
}

static PyObject* startInput(PyObject* self, PyObject* args) {
    if (!terminalInput) terminalInput = new TerminalInput();
    Py_RETURN_NONE;
}

static PyObject* stopInput(PyObject* self, PyObject* args) {
    if (terminalInput) {
        delete terminalInput;
        terminalInput = nullptr;
    }
    Py_RETURN_NONE;
}

static PyObject* getKey(PyObject* self, PyObject* args) {
    bool characters = false;

    if (!PyArg_ParseTuple(args, "|p", &characters)) return nullptr;

    if (!terminalInput) {
        PyErr_SetString(PyExc_RuntimeError, "Terminal input must be started. Use (terminalui.startInput())");
        return nullptr;
    }

    int key = terminalInput->getKey();
    if (key == -1) Py_RETURN_NONE;

    if (characters) {
        char str[2] = { static_cast<char>(key), 0 };
        return PyUnicode_FromString(str);
    } else return PyLong_FromLong(key);
}

static PyObject* bypassInputBlock(PyObject* self, PyObject* args) {
    int bypass = 0;

    if (!PyArg_ParseTuple(args, "p", &bypass)) return nullptr;

    inputBypass = (bypass != 0);
    Py_RETURN_NONE;
}

static PyObject* clearTerminal(PyObject* self, PyObject* args) {
    clear();
    Py_RETURN_NONE;
}

static PyMethodDef Methods[] = {
    {"clearTerminal", clearTerminal, METH_VARARGS, "Creates a fake clear terminal by hiding previous text"},
    {"createSelector", createSelector, METH_VARARGS, "Makes a option selector in terminal"},
    {"createButtons", createButtons, METH_VARARGS, "Creates buttons in terminal"},
    {"createSlider", createSlider, METH_VARARGS, "Create a slider in terminal"},
    {"executeCommand", executeCommand, METH_VARARGS, "Execute a command in console"},
    {"startInput", startInput, METH_VARARGS, "Starts a non-blocking input reader"},
    {"stopInput", stopInput, METH_VARARGS, "Stops the non-blocking input reader"},
    {"getKey", getKey, METH_VARARGS, "Gets terminal inputs"},
    {"bypassInputBlock", bypassInputBlock, METH_VARARGS, "Bypasses input block"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "terminalui",
    "Test Module",
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_terminalui(void) {
    return PyModule_Create(&moduledef);
}
