/****************************************************************************
** Meta object code from reading C++ file 'clientwindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../client/src/http_client/clientwindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'clientwindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_ClientWindow_t {
    QByteArrayData data[12];
    char stringdata0[229];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_ClientWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_ClientWindow_t qt_meta_stringdata_ClientWindow = {
    {
QT_MOC_LITERAL(0, 0, 12), // "ClientWindow"
QT_MOC_LITERAL(1, 13, 23), // "openCreateStudentWindow"
QT_MOC_LITERAL(2, 37, 0), // ""
QT_MOC_LITERAL(3, 38, 20), // "createStudentRequest"
QT_MOC_LITERAL(4, 59, 21), // "openUploadPhotoWindow"
QT_MOC_LITERAL(5, 81, 18), // "uploadPhotoRequest"
QT_MOC_LITERAL(6, 100, 22), // "openReadStudentsWindow"
QT_MOC_LITERAL(7, 123, 19), // "readStudentsRequest"
QT_MOC_LITERAL(8, 143, 21), // "openReadStudentWindow"
QT_MOC_LITERAL(9, 165, 18), // "readStudentRequest"
QT_MOC_LITERAL(10, 184, 23), // "openDeleteStudentWindow"
QT_MOC_LITERAL(11, 208, 20) // "deleteStudentRequest"

    },
    "ClientWindow\0openCreateStudentWindow\0"
    "\0createStudentRequest\0openUploadPhotoWindow\0"
    "uploadPhotoRequest\0openReadStudentsWindow\0"
    "readStudentsRequest\0openReadStudentWindow\0"
    "readStudentRequest\0openDeleteStudentWindow\0"
    "deleteStudentRequest"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_ClientWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      10,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   64,    2, 0x08 /* Private */,
       3,    0,   65,    2, 0x08 /* Private */,
       4,    0,   66,    2, 0x08 /* Private */,
       5,    0,   67,    2, 0x08 /* Private */,
       6,    0,   68,    2, 0x08 /* Private */,
       7,    0,   69,    2, 0x08 /* Private */,
       8,    0,   70,    2, 0x08 /* Private */,
       9,    0,   71,    2, 0x08 /* Private */,
      10,    0,   72,    2, 0x08 /* Private */,
      11,    0,   73,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void ClientWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<ClientWindow *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->openCreateStudentWindow(); break;
        case 1: _t->createStudentRequest(); break;
        case 2: _t->openUploadPhotoWindow(); break;
        case 3: _t->uploadPhotoRequest(); break;
        case 4: _t->openReadStudentsWindow(); break;
        case 5: _t->readStudentsRequest(); break;
        case 6: _t->openReadStudentWindow(); break;
        case 7: _t->readStudentRequest(); break;
        case 8: _t->openDeleteStudentWindow(); break;
        case 9: _t->deleteStudentRequest(); break;
        default: ;
        }
    }
    (void)_a;
}

QT_INIT_METAOBJECT const QMetaObject ClientWindow::staticMetaObject = { {
    QMetaObject::SuperData::link<QWidget::staticMetaObject>(),
    qt_meta_stringdata_ClientWindow.data,
    qt_meta_data_ClientWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *ClientWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *ClientWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_ClientWindow.stringdata0))
        return static_cast<void*>(this);
    return QWidget::qt_metacast(_clname);
}

int ClientWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 10)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 10;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 10)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 10;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
