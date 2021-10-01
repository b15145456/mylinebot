from app_core import socketio

def sentData(id, num):
    socketio.emit('new data', {
        'clinic_id': id,
        'num': num
        })

