__author__ = 'martino'
Generic_Ui = 'background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #333, stop:0.5 #333, stop:1 #555);' \
             'color: #fff;' \
             'border: 1px solid #ddd;' \
             'border-radius: 4px;'
Button_Ui = 'QPushButton{' \
            + Generic_Ui + \
            '\n' \
            '}' \
            'QPushButton:pressed{ ' \
            'background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #222, stop:0.5 #222, stop:1 #333);' \
            'color: #ccc;' \
            'border: 1px solid #fff;' \
            'border-radius: 4px;' \
            '}'
