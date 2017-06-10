import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QComboBox, QListView
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QItemSelection, QItemSelectionModel
from PyQt5 import uic

from spotipy import oauth2


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.testButton = QPushButton()

        #self.playback_devices_comboBox = QComboBox()
        #self.album_list = QListView()
        #self.move_up_button = QPushButton()

        uic.loadUi('main.ui', self)

        self.testButton.clicked.connect(self.test_button_clicked)

        # self.playback_devices_comboBox
        #self.playback_devices_comboBox.addItems(['A', 'B', 'C'])
        #self.playback_devices_comboBox.currentIndexChanged.connect(self.playback_devices_comboBox_selection_changed)
        #self.testButton.clicked.connect(self.test_button_clicked)

        # Album list
        #albums_model = QStandardItemModel()
        #albums = ['OK computer', 'Hello', 'Nog een album']
        #for album in albums:
        #    item = QStandardItem(album)
        #    item.setCheckState(Qt.Checked)
        #    item.setCheckable(True)
        #    albums_model.appendRow(item)
        #self.album_list.setModel(albums_model)
        #self.album_list.selectionModel().selectionChanged.connect(self.album_list_selection_changed)

        # Move up button
        #self.move_up_button.clicked.connect(self.move_up_button_clicked)

        # Move down button
        #self.move_down_button.clicked.connect(self.move_down_button_clicked)

    def album_list_selection_changed(window, newSelection, oldSelection):
        window.move_up_button.setEnabled(not newSelection.isEmpty())
        window.move_down_button.setEnabled(not newSelection.isEmpty())

    def move_up_button_clicked(window, *args):
        selection_model = window.album_list.selectionModel()
        selection_index = selection_model.selectedIndexes()[0].row()

        if selection_index == 0:
            # Item already at the top
            return

        model = window.album_list.model()
        item = model.takeRow(selection_index)
        model.insertRow(selection_index - 1, item)

        #Now select the item again
        index = model.index(selection_index, 0)
        selection_model.setCurrentIndex(index, QItemSelectionModel.Clear)
        index = model.index(selection_index-1, 0)
        selection_model.setCurrentIndex(index, QItemSelectionModel.SelectCurrent)

    def move_down_button_clicked(window, *args):
        selection_model = window.album_list.selectionModel()
        selection_index = selection_model.selectedIndexes()[0].row()

        model = window.album_list.model()
        if selection_index == model.rowCount()-1:
            # Item already at the bottom
            return

        item = model.takeRow(selection_index)
        model.insertRow(selection_index + 1, item)

    @staticmethod
    def test_button_clicked(*args):
        print 'test button clicked'

    @staticmethod
    def playback_devices_comboBox_selection_changed(*args):
        print args

def get_token(web_engine_view):
    username = None
    client_id = None
    client_secret = None
    redirect_uri = None
    with open('./albumcut_config.json', 'rb') as config_file:
        config = json.loads(config_file.read())
        username = config['username']
        client_id = config['client_id']
        client_secret = config['client_secret']
        redirect_uri = config['redirect_uri']

    scopes = [
        'user-read-playback-state', 'user-modify-playback-state', 'user-library-read'
    ]

    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                   scope=scopes, cache_path=".cache-" + username)
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        web_engine_view.url = auth_url
        response = None  # Should be the redirect URL
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)


    if token_info:
        return token_info['access_token']
    else:
        return None

app = QApplication(sys.argv)
window = MyWindow()





window.show()

token = get_token(window.webEngineView)

sys.exit(app.exec_())