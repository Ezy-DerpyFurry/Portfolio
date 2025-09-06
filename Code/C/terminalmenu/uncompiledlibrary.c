// This is if you wanna compile it yourself for python
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>
#include <Python.h>

#define clear() printf("\033[2J\033[H");

void print_terminal_menu(const char *list[], int list_length, int num, const char *opening, const char *selector) {
    clear();
    printf("%s\n", opening);
    for (int i = 0; i < list_length; i++) {
        printf("  %s%s\n", (num-1 == i ? selector : ""), list[i]);
    }
}

const char* terminal_menu(const char *list[], int list_length, const char *opening, const char *selector) {
    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    char c;
    int num = 1;

    print_terminal_menu(list, list_length, num, opening, selector);

    while (read(STDIN_FILENO, &c, 1) == 1) {
        if (c == 'q') {
            tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
            return "None";
        }

        if (c == 119 || c == 65) {
            num = (num + list_length - 2) % list_length + 1;
        } else if (c == 115 || c == 66) {
            num = num % list_length + 1;
        } else if (c == 10 || c == 67) {
            tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
            return list[num-1];
        }

        print_terminal_menu(list, list_length, num, opening, selector);
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return "None";
}

static PyObject* py_terminal_menu(PyObject* self, PyObject* args) {
    PyObject *py_list;
    const char *opening;
    const char *selector;

    if (!PyArg_ParseTuple(args, "Oss", &py_list, &opening, &selector)) {
        return NULL;
    }

    if (!PyList_Check(py_list)) {
        PyErr_SetString(PyExc_TypeError, "First argument must be a list of strings");
        return NULL;
    }

    int list_length = PyList_Size(py_list);
    const char **c_list = malloc(list_length * sizeof(char*));
    if (!c_list) {
        PyErr_NoMemory();
        return NULL;
    }

    for (int i = 0; i < list_length; i++) {
        PyObject *item = PyList_GetItem(py_list, i);
        if (!PyUnicode_Check(item)) {
            free(c_list);
            PyErr_SetString(PyExc_TypeError, "List must only have strings");
            return NULL;
        }
        c_list[i] = PyUnicode_AsUTF8(item);
    }

    const char *result = terminal_menu(c_list, list_length, opening, selector);
    free(c_list);

    return PyUnicode_FromString(result);
}

static PyMethodDef MenuMethods[] = {
    {"terminal_menu", py_terminal_menu, METH_VARARGS, "Show a terminal menu and return selection"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef menumodule = {
    PyModuleDef_HEAD_INIT,
    "mymenu",
    "Terminal menu module",
    -1,
    MenuMethods
};

PyMODINIT_FUNC PyInit_mymenu(void) {
    return PyModule_Create(&menumodule);
}
